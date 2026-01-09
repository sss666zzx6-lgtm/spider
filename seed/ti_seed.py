import os
import requests
import json
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import time

base_url = "https://www.ti.com/"



def extract_category_data():
    """
    从HTML中提取指定格式的分类数据
    :param html: 原始HTML文本
    :return: 符合格式的分类列表
    """
    response = requests.get(base_url)

    # print(response.text)
    # print(response)

    soup = BeautifulSoup(response.text, "lxml")
    # 存储结果的列表
    result_list = []

    # 1. 找到所有class包含"ti_p-megaMenu-page js-megaMenu-page"的div
    menu_pages = soup.find_all('div', class_='ti_p-megaMenu-page js-megaMenu-page')
    for page in menu_pages:
        # 2. 提取data-family-id：找页面内带有data-family-id属性的ul标签
        family_id_ul = page.find('ul', attrs={'data-family-id': True})
        if not family_id_ul:  # 没有data-family-id则跳过
            continue
        family_id = family_id_ul.get('data-family-id', '')

        # 3. 提取一级分类文本：h4下的a标签（排除quick-parametric-link里的a）
        title_a = page.select_one('h4.ti_p-megaMenu-title > a:not(.ti_p-megaMenu-quick-parametric-link a)')
        if title_a:
            # 清理文本（去掉多余空格、换行、span标签内容）
            family_name = title_a.get_text(strip=True)
        else:
            family_name = ''  # 无文本时置空

        # 4. 构造指定格式的字典
        category_dict = {
            "familyID": family_id,
            "familyName": family_name,
            "level": "1",
            "children": []
        }
        result_list.append(category_dict)

    return result_list


# -------------------------- 1. 核心请求函数：修复数据结构提取 --------------------------
def fetch_category_json(url: str, timeout: int = 15) -> List[Dict[str, Any]]:
    """
    请求URL，提取ProductTree中的分类列表（关键修复：适配实际返回结构）
    """
    try:
        response = requests.get(url, timeout=timeout)
        print(f"请求URL: {url} | 状态码: {response.status_code}")

        response.raise_for_status()
        raw_json = response.json()  # 实际返回：{"ProductTree": [分类列表]}

        # 关键修复：提取ProductTree对应的列表
        product_tree = raw_json.get("ProductTree", [])
        if not isinstance(product_tree, list):
            print(f"❌ {url} 的ProductTree不是列表，结构：{type(product_tree)}")
            return []

        # 调试信息
        print(f"✅ {url} 提取到分类数据条数: {len(product_tree)}")
        return product_tree

    except requests.exceptions.RequestException as e:
        print(f"❌ 请求URL失败：{url}，错误信息：{str(e)}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析失败：{url}，响应内容前200字符：{response.text[:200]}")
        return []


# -------------------------- 2. 核心处理函数：树形结构构建（无需修改） --------------------------
def build_hierarchical_tree(raw_data: List[Dict[str, Any]], root_family_id: str) -> List[Dict[str, Any]]:
    """将扁平列表构建为树形结构"""
    node_dict = {item["familyID"]: item for item in raw_data}
    parent_children_map = {}

    for item in raw_data:
        parent_id = item["parentId"]
        if parent_id not in parent_children_map:
            parent_children_map[parent_id] = []
        parent_children_map[parent_id].append(item["familyID"])

    def recursive_build(node_id: str) -> Dict[str, Any]:
        node = node_dict.get(node_id, {})
        child_ids = parent_children_map.get(node_id, [])
        children = [recursive_build(child_id) for child_id in child_ids]

        return {
            "familyID": node.get("familyID", ""),
            "parentId": node.get("parentId", ""),
            "familyName": node.get("familyName", ""),
            "level": node.get("level", ""),
            "isLeaf": node.get("isLeaf", ""),
            "url": node.get("url", ""),  # 新增：保留原始url（可选，根据需求决定是否保留）
            "children": children
        }

    root_nodes = [recursive_build(root_family_id)] if root_family_id in node_dict else []
    return root_nodes


# -------------------------- 3. 主函数：批量处理所有分类 --------------------------
def process_all_categories(category_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """处理所有一级分类，生成最终结果"""
    final_result = []

    for idx, category in enumerate(category_list):
        current_family_id = category["familyID"]
        current_family_name = category["familyName"]

        # 拼接请求URL
        request_url = (
            f"https://www.ti.com/hierarchy/gpnfamilytree?lang=en&output=json"
            f"&familyId={current_family_id}&includeGpns=N&includeSecondaryAssocs=Y"
        )

        # 延迟请求，避免IP封禁
        time.sleep(1)
        raw_category_data = fetch_category_json(request_url)

        if not raw_category_data:
            print(f"⏭️ 跳过分类：{current_family_name}（无有效数据）")
            continue

        # 构建树形结构
        category_tree = build_hierarchical_tree(raw_category_data, current_family_id)

        # 组装结果（分类名作为键，树形结构作为值）
        result_item = {current_family_name: category_tree}
        final_result.append(result_item)

    return final_result

if __name__ == "__main__":
    # 执行提取逻辑
    category_list = extract_category_data()

    print(json.dumps(category_list, indent=4, ensure_ascii=False))
    print(len(category_list))

    final_result = process_all_categories(category_list)

    # 格式化输出结果（方便查看）
    print(json.dumps(final_result, indent=4, ensure_ascii=False))

    base_path = "./seed_json"
    file_path = os.path.join(base_path, "ti.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(final_result, f, indent=2, ensure_ascii=False)

# url = "https://www.ti.com/hierarchy/gpnfamilytree?lang=en&output=json&familyId=0&includeGpns=N&includeSecondaryAssocs=Y"
#
# r = requests.get(url)
# data = r.json()["ProductTree"]
# # print(json.dumps(data, indent=2, ensure_ascii=False))
#
#
# def build_hierarchy(data):
#     """
#     构建产品分类的层级结构（保留familyID和parentId）
#     :param data: 原始数据列表
#     :return: 根节点的树形结构列表
#     """
#     # 1. 建立节点字典：key = familyID, value = 节点信息
#     node_dict = {item["familyID"]: item for item in data}
#
#     # 2. 建立父子关系映射：key = parentId, value = 子节点列表
#     parent_children = {}
#     for item in data:
#         parent_id = item["parentId"]
#         if parent_id not in parent_children:
#             parent_children[parent_id] = []
#         parent_children[parent_id].append(item["familyID"])
#
#     # 3. 递归生成树形结构（新增familyID和parentId字段）
#     def build_tree(node_id):
#         node = node_dict[node_id]
#         children_ids = parent_children.get(node_id, [])
#         children = [build_tree(child_id) for child_id in children_ids]
#
#         # 核心规则：仅叶子节点（isLeaf="Y"）保留URL，非叶子节点URL置空
#         url = node["url"] if node["isLeaf"] == "Y" else ""
#
#         return {
#             "familyID": node["familyID"],  # 新增：保留原始familyID
#             "parentId": node["parentId"],  # 新增：保留原始parentId
#             "familyName": node["familyName"],
#             "level": node["level"],
#             "url": url,
#             "children": children
#         }
#
#     # 4. 根节点是 parentId = "0" 的节点
#     root_ids = parent_children.get("0", [])
#     return [build_tree(root_id) for root_id in root_ids]
#
#
# if __name__ == "__main__":
#     # 生成层级结构
#     hierarchy = build_hierarchy(data)
#     # 格式化输出（缩进4个空格，确保中文显示正常）
#     print(json.dumps(hierarchy, indent=4, ensure_ascii=False))
#
    # base_path = "./seed_json"
    # file_path = os.path.join(base_path, "ti.json")
    #
    # with open(file_path, "w", encoding="utf-8") as f:
    #     json.dump(hierarchy, f, indent=2, ensure_ascii=False)