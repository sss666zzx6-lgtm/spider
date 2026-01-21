import json
import os
import re

import requests
from bs4 import BeautifulSoup
import time


def get_secondary_categories(primary_categories):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # 遍历每个一级分类
    for idx, primary in enumerate(primary_categories):
        primary_url = primary.get("url", "")
        primary_name = primary.get("familyName", "")

        # 跳过空URL的一级分类
        if not primary_url:
            print(f"【跳过】一级分类{primary_name}的URL为空")
            continue

        if primary_url == "http://www.lowpowersemi.com/Product-series/Protocol":
            primary_url = "http://www.lowpowersemi.com/Product-list/Fast_Charging_Protocol"

        print(f"正在请求一级分类[{idx + 1}/{len(primary_categories)}]：{primary_name} → {primary_url}")

        try:
            # 发送GET请求，设置超时10秒，避免卡死
            response = requests.get(primary_url, headers=headers, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding

            soup = BeautifulSoup(response.text, 'html.parser')

            pro_list_div = soup.find('div', class_='proList')
            if not pro_list_div:
                print(f"【提示】一级分类{primary_name}页面proList下无二级分类节点，尝试正则匹配id...")
                # 无二级分类节点，走正则匹配逻辑
                id_pattern = re.compile(r'var data = {\s*id:\s*"(\d+)"', re.IGNORECASE)
                match = id_pattern.search(response.text)
                # match = re.search(r'var data = {\s*id:\s*"(\d+)"', response.text, re.IGNORECASE)
                if match:
                    id_value = match.group(1)
                    new_url = f"http://www.lowpowersemi.com/good-search?id={id_value}&model="
                    primary['url'] = new_url  # 替换一级分类URL
                    print(f"【成功】正则匹配到id={id_value}，一级分类URL已替换为：{new_url}")
                    continue
                else:
                    print(f"【提示】一级分类{primary_name}页面未匹配到id，URL保持不变")

            secondary_divs = pro_list_div.find_all('div', class_='one')
            if not secondary_divs:
                print(f"【提示】一级分类{primary_name}页面proList下无二级分类节点")
                continue

            # 2. 遍历二级分类节点，提取信息
            secondary_categories = []
            for sec_div in secondary_divs:
                # 提取data-id（容错：无则为空）
                data_id = sec_div.get('data-id', '')
                # 提取分类名称（top标签的文本，去除首尾空格）
                top_tag = sec_div.find('div', class_='top')
                family_name = top_tag.get_text(strip=True) if top_tag else f"未命名_{data_id}"

                # 拼接URL：http://www.lowpowersemi.com/good-search?id=data-id&model=
                sec_url = f"http://www.lowpowersemi.com/good-search?id={data_id}&model=" if data_id else ""

                # 构造二级分类字典（level=2，children为空）
                secondary = {
                    "familyName": family_name,
                    "level": 2,
                    "url": sec_url,
                    "children": []
                }
                secondary_categories.append(secondary)

            # 3. 将二级分类添加到一级分类的children中
            primary['children'] = secondary_categories
            print(f"【成功】一级分类{primary_name}提取到{len(secondary_categories)}个二级分类")

            # 加小延迟，避免请求过快被封IP
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            # 捕获所有请求异常（超时、连接失败、HTTP错误等）
            print(f"【失败】请求一级分类{primary_name}失败：{str(e)}")
            continue

    return primary_categories


def extract_categories_from_html(html):

    categories = []
    pro_menu_div = soup.find('div', class_='proMenu pc')
    if not pro_menu_div:
        print("未找到class='proMenu pc'的div节点")
        return categories

    # 第二步：在pro_menu_div下找到class="block"的div
    block_div = pro_menu_div.find('div', class_='block')
    if not block_div:
        print("未找到class='block'的div节点")
        return categories

    # 第三步：仅提取block_div内class="one"的a标签
    a_tags = block_div.find_all('a', class_='one')

    # 4. 遍历每个a标签，提取信息
    for a_tag in a_tags:
        # 提取分类名称：span标签的文本，去除首尾空格
        family_name = a_tag.find('span').get_text(strip=True)
        # 提取链接：a标签的href属性
        url = a_tag.get('href', '')
        # 构造指定格式的字典
        category = {
            "familyName": family_name,
            "level": 1,  # 这些是一级分类，level设为1
            "url": url,
            "children": []  # 暂无子分类，为空数组
        }
        categories.append(category)

    return categories




def find_leaf_nodes(processed_categories):
    # 存储最终的叶子节点结果
    leaf_nodes = []

    def recursive_traverse(nodes, current_path):
        """
        递归遍历分类节点

        参数:
            nodes: 当前层级的节点列表
            current_path: 记录当前分类层级的路径列表（如["电子产品", "手机"]）
        """
        for node in nodes:
            # 1. 获取当前节点的核心字段，做容错处理
            family_name = node.get("familyName", "")
            node_url = node.get("url", "")
            children = node.get("children", [])

            # 2. 将当前节点的名称加入层级路径
            current_path.append(family_name)

            # 3. 判断是否是叶子节点（children为空列表）
            if not children:
                # 拼接category：层级路径用^连接
                category = "^".join(current_path)
                # 拼接url：前缀 + 节点url + 后缀
                full_url = node_url
                # 添加到结果列表
                leaf_nodes.append({
                    "url": full_url,
                    "category": category
                })
            else:
                # 非叶子节点，递归遍历下一级
                recursive_traverse(children, current_path)

            # 4. 回溯：移除当前节点的名称，处理同层级下一个节点
            current_path.pop()

    # 启动递归遍历（初始路径为空列表）
    recursive_traverse(processed_categories, [])

    return leaf_nodes


if __name__ == "__main__":

    url = "http://www.lowpowersemi.com/"
    response = requests.get(url)

    # print(response.text)

    soup = BeautifulSoup(response.text, "lxml")

    result = extract_categories_from_html(soup)

    full_categories = get_secondary_categories(result)

    # print(json.dumps(full_categories, indent=4, ensure_ascii=False))

    leaf_result = find_leaf_nodes(full_categories)

    base_path = "./seed_json"
    file_path = os.path.join(base_path, "lowpowersemi.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(leaf_result, f, indent=2, ensure_ascii=False)