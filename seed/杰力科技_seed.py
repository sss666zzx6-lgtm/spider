import json
import os
import re
import requests
from bs4 import BeautifulSoup
import time


def extract_categories_from_html(soup):
    category_list = []

    target_li_list = soup.select("ul.menu ul.submenu li.hasSecondMenu")

    if not target_li_list:
        print("未匹配到任何符合条件的li.hasSecondMenu元素")
    else:
        print(f"一次性匹配到{len(target_li_list)}个li.hasSecondMenu元素")
        # 遍历所有匹配到的li
        for li in target_li_list:
            # 提取一级分类（level=2）
            main_a = li.find('a')
            if not main_a:
                continue
            primary_cate = {
                "familyName": main_a.get_text(strip=True),
                "level": 2,
                "url": main_a.get('href', ''),
                "children": []
            }

            # 提取二级分类（level=3）
            second_menu_ul = li.find('ul', class_='secondMenu')
            if second_menu_ul:
                for sec_li in second_menu_ul.find_all('li'):
                    sec_a = sec_li.find('a')
                    if not sec_a:
                        continue
                    secondary_cate = {
                        "familyName": sec_a.get_text(strip=True),
                        "level": 3,
                        "url": sec_a.get('href', ''),
                        "children": []
                    }
                    primary_cate['children'].append(secondary_cate)

            category_list.append(primary_cate)
    return category_list


def extract_leaf_nodes_with_rules(category_list):

    leaf_nodes = []

    def recursive_traverse(nodes, current_path):
        for node in nodes:
            # 1. 提取节点核心信息，容错处理
            family_name = node.get("familyName", "").strip()
            node_url = node.get("url", "").strip()
            children = node.get("children", [])
            node_level = node.get("level", 0)

            # 2. 跳过规则：二级节点（level=2）且familyName为Financial
            if node_level == 2 and family_name == "Financial":
                print(f"【跳过】二级节点：{family_name}")
                continue

            # 3. 处理路径：如果当前familyName和路径最后一个元素相同，仅保留后续（去重）
            new_path = current_path.copy()
            if new_path:
                # 若当前名称和路径最后一个重复，替换/不重复添加（保留后面的）
                if new_path[-1] == family_name:
                    new_path = new_path[:-1]  # 移除重复的前一个，保留当前
            new_path.append(family_name)  # 添加当前层级名称

            # 4. 判断是否是叶子节点（children为空）
            if not children:
                # 拼接category：层级用^连接
                category = "^".join(new_path)
                # 构造叶子节点字典
                leaf_node = {
                    "url": node_url,
                    "category": category
                }
                leaf_nodes.append(leaf_node)
                print(f"【提取叶子节点】category: {category} → url: {node_url}")
            else:
                # 非叶子节点，递归遍历下一级
                recursive_traverse(children, new_path)

    recursive_traverse(category_list, [])

    return leaf_nodes

if __name__ == "__main__":

    url = "https://www.excelliancemos.com/en/"
    response = requests.get(url)

    # print(response.text)

    soup = BeautifulSoup(response.text, "lxml")
    # print(soup.prettify())
    category_list = extract_categories_from_html(soup)

    leaf_nodes = extract_leaf_nodes_with_rules(category_list)
    print(json.dumps(leaf_nodes, indent=4, ensure_ascii=False))

    base_path = "./seed_json"
    file_path = os.path.join(base_path, "excelliancemos.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(leaf_nodes, f, indent=2, ensure_ascii=False)
