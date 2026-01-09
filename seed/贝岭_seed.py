import os
import re
import json
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any

url = "https://www.belling.com.cn/en.html"

response = requests.get(url)
print(response.text)

soup = BeautifulSoup(response.text, "lxml")

BASE_DOMAIN = "https://www.belling.com.cn"  # 假设基础域名，可根据实际修改


def extract_category_hierarchy(html_content: str):
    """
    解析HTML内容，提取产品分类的层级关系，生成指定格式的列表
    :param html_content: 网页响应的HTML文本
    :return: 层级分类列表（一级分类level=1，二级分类level=2）
    """
    soup = BeautifulSoup(html_content, "lxml")
    final_result = []

    # 1. 正则匹配showNav(数字)中的数字（提取nav_id）
    nav_id_pattern = re.compile(r'showNav\((\d+)\)')

    # 2. 提取左侧一级分类（<dl>下的<dd>）
    first_level_dds = soup.select("dl > dd")
    for dd in first_level_dds:
        # ---- 提取一级分类信息 ----
        # 一级分类名称（v2类的文本）
        first_level_name = dd.select_one("a.v2").get_text(strip=True) if dd.select_one("a.v2") else ""
        # 提取showNav中的nav_id（用于匹配右侧二级分类）
        onclick_attr = dd.get("onclick", "")
        nav_id_match = nav_id_pattern.search(onclick_attr)
        nav_id = nav_id_match.group(1) if nav_id_match else ""

        # 一级分类的URL（一级分类无直接URL，设为空）
        first_level_url = ""

        # ---- 提取二级分类信息（对应d_nav_{nav_id}的ol-box） ----
        second_level_list = []
        if nav_id:
            # 找到对应的ol-box容器
            ol_box = soup.find("div", id=f"d_nav_{nav_id}")
            if ol_box:
                # 提取二级分类的<li>列表
                second_level_lis = ol_box.select("ol > li")
                for li in second_level_lis:
                    # 二级分类名称
                    second_level_name = li.get_text(strip=True) if li else ""
                    # 二级分类URL（补全基础域名）
                    second_level_href = li.select_one("a").get("href", "") if li.select_one("a") else ""
                    second_level_url = f"{BASE_DOMAIN}{second_level_href}" if second_level_href else ""

                    # 构建二级分类字典（level=2）
                    second_level_item = {
                        "familyName": second_level_name,
                        "level": 2,
                        "url": second_level_url,
                        "children": []  # 二级是叶子节点，children为空
                    }
                    second_level_list.append(second_level_item)

        # ---- 构建一级分类字典（level=1） ----
        first_level_item = {
            "familyName": first_level_name,
            "level": 1,
            "url": first_level_url,
            "children": second_level_list
        }
        final_result.append(first_level_item)

    return final_result


def extract_leaf_nodes_with_category(hierarchy_data: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    遍历层级结构，提取所有叶子节点（无children）的信息：
    - url：叶子节点的url
    - category：层级拼接（一级^二级）
    """
    leaf_nodes = []

    # 递归遍历函数，记录当前层级路径
    def recursive_extract(node: Dict[str, Any], path: List[str]):
        current_path = path + [node["familyName"]]

        # 判断是否是叶子节点（children为空且url非空）
        if not node.get("children", []) and node.get("url"):
            # 拼接category（层级用^分隔）
            category_str = "^".join(current_path)
            leaf_nodes.append({
                "url": node["url"],
                "category": category_str
            })
        else:
            # 非叶子节点，递归处理子节点
            for child in node.get("children", []):
                recursive_extract(child, current_path)

    # 遍历所有一级分类
    for first_level_node in hierarchy_data:
        recursive_extract(first_level_node, path=[])

    return leaf_nodes

if __name__ == "__main__":
    # 示例：替换为实际的目标URL
    target_url = "https://www.belling.com.cn/en/products.html"  # 假设的目标URL，替换为实际地址
    try:
        response = requests.get(target_url, timeout=15)
        response.raise_for_status()

        # 解析层级关系
        category_hierarchy = extract_category_hierarchy(response.text)

        #
        # print(json.dumps(category_hierarchy, indent=4, ensure_ascii=False))

        leaf_node_result = extract_leaf_nodes_with_category(category_hierarchy)

        print(json.dumps(leaf_node_result[:5], indent=4, ensure_ascii=False))



        base_path = "./seed_json"
        file_path = os.path.join(base_path, "beiling.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(leaf_node_result, f, indent=2, ensure_ascii=False)

    except requests.exceptions.RequestException as e:
        print(f"❌ 请求URL失败：{str(e)}")
    except Exception as e:
        print(f"❌ 解析失败：{str(e)}")