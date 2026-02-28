import requests
from bs4 import BeautifulSoup
import os
import json

def parse_power_leaf_nodes(divs_elements, base_url=""):

    leaf_nodes = []

    # 遍历每个一级分类的div
    for div in divs_elements:
        # 1. 提取一级分类名称（过滤空字符和多余空格）
        # 找到包含分类名称的span标签（排除glyphicon的span）
        first_level_spans = div.find_all('span', style=True)
        first_level_name = ""
        for span in first_level_spans:
            # 筛选出包含分类名称的span（排除glyphicon的箭头span）
            if "cursor: pointer" in span.get("style", "") and span.text.strip():
                first_level_name = span.text.strip()
                break

        if not first_level_name:  # 跳过无名称的一级分类
            continue

        # 2. 找到一级分类下的下拉列表（ul.dropdown-menu）
        dropdown_ul = div.find('ul', class_='dropdown-menu')
        if not dropdown_ul:  # 无二级节点的情况（当前场景暂无，保留兼容）
            # 一级分类作为叶子节点
            leaf_nodes.append({
                "url": "",  # 无二级节点时URL为空，可根据需求调整
                "category": first_level_name
            })
            continue

        # 3. 遍历二级叶子节点（ul下的li>a）
        second_level_li_list = dropdown_ul.find_all('li')
        for li in second_level_li_list:
            a_tag = li.find('a')
            if not a_tag:
                continue

            # 提取二级分类名称和URL
            second_level_name = a_tag.text.strip()
            second_level_url = a_tag.get('href', '').strip()

            # 拼接完整URL和分类层级
            full_url = f"{base_url}{second_level_url}" if base_url and second_level_url else second_level_url
            full_category = f"{first_level_name}^{second_level_name}"

            # 添加到结果列表
            leaf_nodes.append({
                "url": full_url,
                "category": full_category
            })

    return leaf_nodes


if __name__ == "__main__":
    url = "https://www.analog.com.tw/products.aspx?ID=9"
    base_url = "https://www.analog.com.tw"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    # print(soup.prettify())
    navbar_nav = soup.find_all('ul', class_='nav navbar-nav')
    divs_elements = []
    if navbar_nav:
        for navbar in navbar_nav:
            divs_elements = navbar.find_all('div', class_='linkup-left-menu')

    # print(len(divs_elements))
    # for div in divs_elements:
    #     print(div)

    leaf_nodes = parse_power_leaf_nodes(divs_elements, base_url)

    # 打印结果
    for node in leaf_nodes:
        print(node)
    print(len(leaf_nodes))


    file_path = "analog.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(leaf_nodes, f, indent=2, ensure_ascii=False)
