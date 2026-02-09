import requests
from bs4 import BeautifulSoup
import json
import re


def parse_product_data_from(url):
    product_list = []
    try:
        # 发起请求，加请求头+超时，避免被拦截/卡死
        response = requests.get(url, timeout=15)
        response.raise_for_status()  # 抛出4xx/5xx状态码异常
        response.encoding = response.apparent_encoding  # 自动适配编码，避免乱码
        page_html = response.text

        # 核心正则：匹配var allData = JSON.parse('[{产品JSON}]'); 提取单引号内的JSON字符串
        # 正则说明：转义\. \(\)，非贪婪匹配.*?，re.S让.匹配换行，适配JSON跨行的情况
        pattern = re.compile(r'var allData = JSON\.parse\(\'(.*?)\'\);', re.S)
        match_result = pattern.search(page_html)  # 搜索第一个匹配项（站点仅一个allData）

        if not match_result:
            print("未匹配到allData的JSON数据，请检查站点格式是否变更")
            return product_list

        # 提取正则分组中的JSON字符串，处理转义符（站点里是\'，需替换为"才能正常解析）
        json_str = match_result.group(1).replace("\\'", "\"")
        # 解析JSON字符串为Python列表（产品列表）
        all_data = json.loads(json_str)

        # 遍历产品列表，提取指定字段
        for item in all_data:
            # 提取字段，用get方法避免KeyError，空值则返回''
            part_number = item.get("part_number", "").strip()
            part_type = item.get("part_type", "").strip()
            # 核心规则：有datasheet取datasheet，无则取id（id也做空值兼容）
            datasheet = item.get("datasheet", "").strip()
            if not datasheet:
                datasheet = str(item.get("id", "")).strip()  # 转字符串，避免id是数字类型

            # 过滤掉part_number为空的无效产品（可选，根据站点情况调整）
            if part_number:
                product_info = {
                    "part_number": part_number,
                    "part_type": part_type,
                    "datasheet": datasheet
                }
                product_list.append(product_info)

    except requests.exceptions.RequestException as e:
        print(f"请求URL失败：{e}")
    except json.JSONDecodeError as e:
        print(f"JSON解析失败（字符串格式异常）：{e}")
    except Exception as e:
        print(f"解析数据时发生未知错误：{e}")

    return product_list

