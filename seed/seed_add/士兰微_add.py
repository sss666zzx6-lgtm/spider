import json
import requests
import os
import re

from bs4 import BeautifulSoup

from util.create_darwin_api import create_api


def get_ajax_url(target_url: str) -> str | None:

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7"
    }

    # 2. 发送GET请求获取页面内容
    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        response.raise_for_status()  # 抛出HTTP错误（如404/500）
        page_text = response.text
    except Exception as e:
        print(f"请求URL失败：{str(e)}")
        return None

    # 3. 正则匹配protype和ctype参数值（核心）
    # 匹配模式：匹配 data:{protype: 数字,'ctype':数字} 格式的代码片段
    pattern = r"data:\{protype:\s*(\d+),\s*'ctype':\s*(\d+)\}"
    match = re.search(pattern, page_text)

    if not match:
        print("未匹配到protype和ctype参数",target_url)
        return None

    # 提取匹配到的参数值
    protype = match.group(1)
    ctype = match.group(2)

    # 4. 拼接目标ajax URL
    ajax_base_url = "https://www.silan.com.cn/en/index.php/product/protwo_ajax.html"
    final_ajax_url = f"{ajax_base_url}?protype={protype}&ctype={ctype}"

    return final_ajax_url


def get_ajax_url_id_1(target_url: str) -> str | None:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7"
    }

    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        response.raise_for_status()
        page_text = response.text
    except Exception as e:
        print(f"请求URL失败：{str(e)}")
        return None

    # 核心修复：适配 ?ctype="+"463"+ 这种格式（兼容所有变体）
    # 匹配逻辑：tools.load_page( 开头 → 任意字符 → ?ctype= → 任意引号/加号 → 数字 → 任意引号/加号 → &pro_search=
    pattern = r"tools\.load_page\(.*?\?ctype=([\"\+]+)?(\d+)([\"\+]+)?&pro_search="
    match = re.search(pattern, page_text, re.DOTALL)  # re.DOTALL允许.匹配换行

    if not match:
        print("未匹配到tools.load_page内的ctype参数", target_url)
        return None

    # 提取数字（group2是纯数字，group1/group3是包裹的"+"/"）
    ctype = match.group(2)

    # 拼接目标URL
    ajax_base_url = "https://www.silan.com.cn/en/index.php/product/pro_ajax.html"
    final_ajax_url = f"{ajax_base_url}?ctype={ctype}&pro_search="

    return final_ajax_url

def get_product_data(target_url: str):
    try:
        response = requests.get(target_url, timeout=15)
        response.raise_for_status()
        page_text = response.text
        product_dict = {}
        if "No Related Products" in page_text:
            print("没有产品列表页——2")
            return False
        else:
            print("有产品列表页——1")
            soup = BeautifulSoup(page_text, "lxml")
            tbody= soup.find("tbody")
            if not tbody:
                print("未找到tbody标签")
                return product_dict
            tr_list= tbody.find_all("tr")
            if tr_list:
                for tr in tr_list:
                    first_th = tr.find("th")
                    if not first_th:
                        continue

                    # 找到th内的a标签
                    a_tag = first_th.find("a")
                    if not a_tag:
                        continue  # 无a标签则跳过该tr

                    # 提取型号（去首尾空格）和href
                    product_model = a_tag.get_text(strip=True)
                    product_href = a_tag.get("href", "").strip()

                    # 仅当型号和href都非空时加入字典
                    if product_model and product_href:
                        product_dict[product_model] = product_href
            return product_dict

    except Exception as e:
        print(f"请求URL失败：{str(e)}")
        return None

base_path = "../seed_json"

file_path = os.path.join(base_path, "silan.json")
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        target_url = item["url"]
        ajax_url = get_ajax_url(target_url)
        # print(ajax_url)
        if ajax_url:
            print("找到ajax_url,原始url---",target_url)
            ajax_url_id_1 = get_ajax_url_id_1(target_url)
            print("id==1的ajax_url",ajax_url_id_1)
            path = ajax_url
            category = item["category"]
            custom_map = {"category": category}
            print(category)
            if ajax_url_id_1:
                product_data = get_product_data(ajax_url_id_1)
                if product_data:
                    # print(json.dumps(product_data, ensure_ascii=False))
                    custom_map["data"] = product_data

            create_api(plan_id="fa29a398bf1f641a527b6ad86aaa62fe", path=path, custom_map=custom_map)