from curl_cffi import requests
from bs4 import BeautifulSoup
import json
import os
import re

BASE_DOMAIN = "http://www.gmt.com.tw/product/tree.php"


def extract_leaf_nodes(category_table):
    leaf_nodes = []

    for td in category_table.find_all("td"):
        # 跳过分隔线、空白占位格
        if td.get("width") == "2" or td.get("class") == ["tmenu_space"]:
            continue

        # 一级分类
        item1 = td.find("a", class_="item1")
        if not item1:
            continue
        first = item1.get_text(strip=True)

        # ===================== 关键：排除这两个非产品分类 =====================
        if first in ("+Related Info", "+Support"):
            continue
        # =====================================================================

        # 二级分类 & 叶子节点
        section = td.find("div", class_="section")
        if not section:
            continue

        second = ""
        for a in section.find_all("a"):
            cls = a.get("class", [])

            if "item0" in cls:
                second = a.get_text(strip=True)

            elif "item2" in cls and a.has_attr("href"):
                url = a["href"].strip()
                title = a.get_text(strip=True)
                category = f"{first}^{second}^{title}"
                leaf_nodes.append({
                    "url": BASE_DOMAIN + url,
                    "category": category
                })

    return leaf_nodes

if __name__ == '__main__':
    target_url = "https://www.gmt.com.tw/product/tree.php"

    response = requests.get(target_url)

    soup = BeautifulSoup(response.text, "lxml")
    category_table = soup.find("table", id="menu1")
    # print(category_table)

    result = extract_leaf_nodes(category_table)
    print(json.dumps(result, indent=4, ensure_ascii=False))
    print(len(result))

    base_path = "./seed_json"
    file_path = os.path.join(base_path, "gmt.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)