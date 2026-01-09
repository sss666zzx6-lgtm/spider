import requests
import json
import os
from typing import List, Dict, Any





def convert_category_format(node: Dict[str, Any], current_level: int) -> Dict[str, Any]:
    """
    递归转换单个分类节点为指定格式
    :param node: 原始分类节点（含id、pId、nameEn、children等）
    :param current_level: 当前节点的层级（根节点为1）
    :return: 转换后的节点字典
    """
    # 转换当前节点的基础信息
    converted_node = {
        "ID": str(node["id"]),  # 转为字符串，与示例格式一致
        "familyName": node.get("nameEn", ""),
        "level": str(current_level),  # level转为字符串，与示例格式一致
        "children": []
    }

    # 递归处理子节点（层级+1）
    if "children" in node and isinstance(node["children"], list):
        for child in node["children"]:
            converted_child = convert_category_format(child, current_level + 1)
            converted_node["children"].append(converted_child)

    return converted_node


def process_category_data(raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    处理原始分类列表，生成最终的指定格式列表
    :param raw_data: API返回的data列表（根节点pId=0）
    :return: 转换后的分类列表
    """
    final_result = []
    # 遍历根节点（pId=0），层级从1开始
    for root_node in raw_data:
        converted_root = convert_category_format(root_node, current_level=1)
        final_result.append(converted_root)
    return final_result


def extract_leaf_nodes(converted_result: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    遍历转换后的层级结构，提取叶子节点（无children），生成指定格式列表
    :param converted_result: process_category_data返回的转换后结果
    :return: 叶子节点列表，格式为[{"url": "", "category": ""}, ...]
    """
    leaf_nodes = []
    BASE_URL_TEMPLATE = "https://www.dioo.com/admin/api/api/product/info?id={}"
    "".format()

    # 递归遍历函数，记录当前层级的familyName路径
    def recursive_extract(node: Dict[str, Any], path: List[str]):
        # 将当前节点的familyName加入路径
        current_path = path + [node["familyName"]]

        # 判断是否是叶子节点（children为空列表）
        if not node.get("children", []):
            # 拼接URL：替换模板中的id为当前节点的ID
            leaf_url = node["ID"]
            # 拼接category：层级familyName用^分隔
            leaf_category = "^".join(current_path)
            # 添加到结果列表
            leaf_nodes.append({
                "url": leaf_url,
                "category": leaf_category
            })
        else:
            # 非叶子节点，递归处理子节点
            for child in node["children"]:
                recursive_extract(child, current_path)

    # 遍历所有根节点，开始递归提取
    for root_node in converted_result:
        recursive_extract(root_node, path=[])

    return leaf_nodes

if __name__ == "__main__":
    # 1. 请求API获取原始数据
    url = "https://www.dioo.com/admin/api/api/productfl/tree?s_show=1"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()  # 触发HTTP异常（404/500等）
        raw_data = response.json()["data"]

        # 2. 转换为指定格式
        converted_result = process_category_data(raw_data)


        print(json.dumps(converted_result, indent=4, ensure_ascii=False))

        print(f"共转换 {len(converted_result)} 个根分类节点")

        leaf_node_result = extract_leaf_nodes(converted_result)

        base_path = "./seed_json"
        file_path = os.path.join(base_path, "dioo.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(leaf_node_result, f, indent=2, ensure_ascii=False)




    except Exception as e:
        print(f"转换失败：{str(e)}")