import os
import requests
from curl_cffi import requests
import json
from bs4 import BeautifulSoup
from requests.compat import urljoin


url = "https://www.rohm.com/product-category?p_p_id=com_rohm_portal_header_RohmHeaderPortlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=%2Fheader%2FgetProductForSitemap&p_p_cacheability=cacheLevelPage&menuId=nav-01"
base_url = "https://www.rohm.com"
response = requests.get(url)
print(response.text)
print(response.status_code)

soup = BeautifulSoup(response.text, "lxml")


def extract_category_tree():
    root_ul = soup.find("ul", class_="producttree1")
    if not root_ul:
        return []

    category_tree = []
    first_level_li_list = root_ul.find_all("li", class_="productmegamenu")
    for first_li in first_level_li_list:
        # 排除搜索项
        if "product-menu-search" in first_li.get("class", []):
            continue

        # 【核心修正】只提取一级分类下的直接子元素（a/strong），避免取到子分类的名称
        first_name_elem = first_li.find("a", recursive=False) or first_li.find("strong", recursive=False)
        if not first_name_elem:
            continue
        first_name = first_name_elem.get_text(strip=True)
        if not first_name:
            continue

        # 初始化一级分类
        first_category = {
            "familyName": first_name,
            "level": 1,
            "url": "",
            "children": []
        }

        # 提取二级分类（wrapcol下的group-list/直接a标签）
        wrapcol_list = first_li.find_all("div", class_="wrapcol")
        for wrapcol in wrapcol_list:
            # 处理group-list中的二级分类
            group_list_list = wrapcol.find_all("div", class_="group-list")
            for group_list in group_list_list:
                # 提取二级名称（group-list下的直接a/strong）
                second_name_elem = group_list.find("a", recursive=False) or group_list.find("strong", recursive=False)
                if not second_name_elem:
                    continue
                second_name = second_name_elem.get_text(strip=True)
                if not second_name:
                    continue

                second_category = {
                    "familyName": second_name,
                    "level": 2,
                    "url": "",
                    "children": []
                }

                # 提取三级分类（producttreelevel2下的child）
                third_level_ul = group_list.find("ul", class_="producttreelevel2")
                if third_level_ul:
                    third_level_li_list = third_level_ul.find_all("li", class_="child")
                    for third_li in third_level_li_list:
                        third_name_elem = third_li.find("a")
                        if not third_name_elem:
                            continue
                        third_name = third_name_elem.get_text(strip=True)
                        third_href = third_name_elem.get("href", "").strip()
                        third_url = urljoin(base_url, third_href) if third_href else ""

                        third_category = {
                            "familyName": third_name,
                            "level": 3,
                            "url": third_url,
                            "children": []
                        }
                        second_category["children"].append(third_category)
                else:
                    # 无三级分类，二级是叶子节点
                    second_href = second_name_elem.get("href", "").strip()
                    second_category["url"] = urljoin(base_url, second_href) if second_href else ""

                first_category["children"].append(second_category)

            # 处理wrapcol下直接的a标签（无group-list的二级分类）
            direct_a_list = wrapcol.find_all("a", recursive=False)
            for direct_a in direct_a_list:
                if direct_a.find_parent("div", class_="group-list"):
                    continue
                second_name = direct_a.get_text(strip=True)
                second_href = direct_a.get("href", "").strip()
                second_category = {
                    "familyName": second_name,
                    "level": 2,
                    "url": urljoin(base_url, second_href) if second_href else "",
                    "children": []
                }
                first_category["children"].append(second_category)

        # 一级分类为叶子节点的情况
        if not first_category["children"]:
            first_href = first_name_elem.get("href", "").strip()
            first_category["url"] = urljoin(base_url, first_href) if first_href else ""

        category_tree.append(first_category)

    return category_tree


def collect_url_with_category(category_tree):
    """递归收集非空URL并拼接层级"""
    result_list = []

    def recursive_traverse(node, parent_path):
        current_path = parent_path + [node["familyName"]]
        if node["url"].strip():
            result_list.append({
                "url": node["url"].strip(),
                "category": "^".join(current_path)
            })
        for child in node["children"]:
            recursive_traverse(child, current_path)

    for first_node in category_tree:
        recursive_traverse(first_node, [])

    return result_list


# 执行提取与整理
category_tree = extract_category_tree()
final_result = collect_url_with_category(category_tree)

# 输出结果
print(json.dumps(final_result, indent=4, ensure_ascii=False))


base_path = "./seed_json"
file_path = os.path.join(base_path, "rohm.json")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(final_result, f, indent=2, ensure_ascii=False)