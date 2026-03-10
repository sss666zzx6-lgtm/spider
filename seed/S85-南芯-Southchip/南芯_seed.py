import requests
from bs4 import BeautifulSoup
import os
import json
import re


def parse_category_leaf_nodes(category_data):
    """
    解析分类数据，提取所有叶子节点的分类名（层级用^拼接）和对应URL
    :param category_data: 原始分类数据（列表结构）
    :return: 叶子节点列表，每个元素格式 {"url": "", "category": ""}
    """
    result = []
    base_url = "https://www.southchip.com/en"

    # ------------------- 修正后的路径解析（逐字符匹配你的数据结构） -------------------
    navs = None
    try:
        # 1. 取header核心字典（category_data[3]）
        if not isinstance(category_data, list) or len(category_data) < 4:
            raise Exception("category_data不是有效列表，或长度不足4")
        header_dict = category_data[3]
        if not isinstance(header_dict, dict) or 'children' not in header_dict:
            raise Exception("header_dict不是有效字典，或无children字段")

        # 2. 取header的第一个children → first_div_node（['$', 'div', None, div1_attr]）
        header_children = header_dict['children']
        if not isinstance(header_children, list) or len(header_children) < 1:
            raise Exception("header_children不是有效列表，或长度不足1")
        first_div_node = header_children[0]
        if not isinstance(first_div_node, list) or len(first_div_node) < 4:
            raise Exception(f"first_div_node结构异常：{first_div_node}")
        div1_attr = first_div_node[3]  # div1的属性字典（bg-white）
        if not isinstance(div1_attr, dict) or 'children' not in div1_attr:
            raise Exception("div1_attr不是有效字典，或无children字段")

        # div1_attr['children'] 直接是second_div_node，不是列表包含列表
        second_div_node = div1_attr['children']  # 直接取第二层div节点（['$', 'div', None, div2_attr]）
        if not isinstance(second_div_node, list) or len(second_div_node) < 4:
            raise Exception(f"second_div_node结构异常：{second_div_node}")
        div2_attr = second_div_node[3]  # div2的属性字典（content_container）
        if not isinstance(div2_attr, dict) or 'children' not in div2_attr:
            raise Exception("div2_attr不是有效字典，或无children字段")

        # div2_attr['children'] 直接是third_div_node，不是列表包含列表
        third_div_node = div2_attr['children']  # 直接取第三层div节点（['$', 'div', None, div3_attr]）
        if not isinstance(third_div_node, list) or len(third_div_node) < 4:
            raise Exception(f"third_div_node结构异常：{third_div_node}")
        div3_attr = third_div_node[3]  # div3的属性字典（relative flex）
        if not isinstance(div3_attr, dict) or 'children' not in div3_attr:
            raise Exception("div3_attr不是有效字典，或无children字段")

        # 3. 取div3的children（包含$L15/$L17/$L1a的列表）
        div3_children = div3_attr['children']
        if not isinstance(div3_children, list) or len(div3_children) < 4:
            raise Exception(f"div3_children长度不足4：{len(div3_children)}")
        l1a_node = div3_children[3]  # 第四个元素是$L1a节点（['$', '$L1a', None, l1a_attr]）
        if not isinstance(l1a_node, list) or len(l1a_node) < 4:
            raise Exception(f"l1a_node结构异常：{l1a_node}")
        l1a_attr = l1a_node[3]  # $L1a的属性字典
        if not isinstance(l1a_attr, dict) or 'navs' not in l1a_attr:
            raise Exception("l1a_attr无navs字段")

        # 4. 最终拿到navs数组
        navs = l1a_attr['navs']
        if not isinstance(navs, list):
            raise Exception("navs不是列表")

    except Exception as e:
        print(f"⚠️ 核心分类数据定位失败：{e}")
        return result

    # ------------------- 递归遍历提取叶子节点（逻辑不变） -------------------
    def _recursive_traverse(node, current_level):
        if not isinstance(node, dict):
            return
        node_title = node.get("title", "").strip()
        node_url = node.get("href", "").strip()
        if not node_title:
            return

        new_level = current_level + [node_title]
        children = node.get("children", [])
        valid_children = [c for c in children if isinstance(c, dict) and c.get("title", "").strip()]

        if len(valid_children) == 0:
            result.append({
                "url": base_url+ node_url,
                "category": "^".join(new_level)
            })
        else:
            for child in valid_children:
                _recursive_traverse(child, new_level)

    # 遍历一级分类
    for root_node in navs:
        _recursive_traverse(root_node, [])

    return result


def parse_only_products_leaf(category_data):
    result = []

    # ------------------- 逐层级拆解路径（带调试） -------------------
    try:
        # 步骤1：取header的核心属性字典
        header_attr = category_data[3]
        print(f"✅ 步骤1：拿到header_attr: {type(header_attr)}")

        # 步骤2：取header下第一个div节点（['$', 'div', None, div1_attr]）
        first_div_node = header_attr['children'][0]
        print(f"✅ 步骤2：拿到first_div_node: {type(first_div_node)}, 长度: {len(first_div_node)}")

        # 步骤3：取第一个div的属性字典（bg-white）
        div1_attr = first_div_node[3]
        print(f"✅ 步骤3：拿到div1_attr: {type(div1_attr)}")

        # 步骤4：取div1的children → 第二层div节点（['$', 'div', None, div2_attr]）
        second_div_node = div1_attr['children']
        print(f"✅ 步骤4：拿到second_div_node: {type(second_div_node)}, 长度: {len(second_div_node)}")

        # 步骤5：取第二层div的属性字典（content_container）
        div2_attr = second_div_node[3]
        print(f"✅ 步骤5：拿到div2_attr: {type(div2_attr)}")

        # 步骤6：取div2的children → 第三层div节点（['$', 'div', None, div3_attr]）
        third_div_node = div2_attr['children']
        print(f"✅ 步骤6：拿到third_div_node: {type(third_div_node)}, 长度: {len(third_div_node)}")

        # 步骤7：取第三层div的属性字典（relative flex）
        div3_attr = third_div_node[3]
        print(f"✅ 步骤7：拿到div3_attr: {type(div3_attr)}")

        # 步骤8：取div3的children → 包含$L1a的列表（第4个元素是$L1a）
        div3_children = div3_attr['children']
        print(f"✅ 步骤8：拿到div3_children: 长度 {len(div3_children)}")

        # 步骤9：取$L1a节点（['$', '$L1a', None, l1a_attr]）
        l1a_node = div3_children[3]
        print(f"✅ 步骤9：拿到l1a_node: {type(l1a_node)}, 长度: {len(l1a_node)}")

        # 步骤10：取$L1a的属性字典 → 最终拿到navs
        l1a_attr = l1a_node[3]
        navs = l1a_attr['navs']
        print(f"✅ 步骤10：成功拿到navs，长度: {len(navs)}")

    except Exception as e:
        print(f"❌ navs匹配失败：{e}")
        return result

    # ------------------- 只提取Products下的叶子节点 -------------------
    # 1. 找到Products节点
    products_node = None
    for item in navs:
        if item.get("title") == "Products":
            products_node = item
            break
    if not products_node:
        print("❌ 未找到Products节点")
        return result
    print(f"✅ 找到Products节点，子节点数: {len(products_node.get('children', []))}")

    # 2. 递归遍历Products的子节点（Products不算一级）
    def traverse(node, path):
        title = node.get("title", "").strip()
        href = node.get("href", "").strip()
        if not title:
            return

        # 过滤有效子节点（仅字典+有标题）
        children = node.get("children", [])
        valid_children = [c for c in children if isinstance(c, dict) and c.get("title", "").strip()]

        # 叶子节点：无有效子节点
        if not valid_children:
            result.append({
                "url": "https://www.southchip.com/en" + href,
                "category": "^".join(path + [title])
            })
        else:
            # 非叶子节点：递归
            for child in valid_children:
                traverse(child, path + [title])

    # 遍历Products的子节点（Automotive Products等作为一级）
    for child in products_node.get("children", []):
        traverse(child, [])

    return result
if __name__ == "__main__":
    url = "https://www.southchip.com/en/product-category/pd-dpdm-controller"
    # base_url = "https://www.southchip.com/en"

    response = requests.get(url,headers={
        "cookie":"LOCAL_LOCALE=en"
    })
    # print(response.text)

    category_str = re.search( r"\.push\(\[1,\"a:(.*?)\\n", response.text)
    category_data = None
    if category_str:
        raw_str = category_str.group(1)
        print(f"匹配到的原始字符串（带转义符）：\n{raw_str[:100]}...")

        # 清理转义符：把 \\" 替换成 "（实际是把 \" 换成 "）
        clean_str = raw_str.replace('\\"', '"')
        print(f"清理后的字符串（无多余转义符）：\n{clean_str[:100]}...")

        # 3. 解析JSON
        try:
            category_data = json.loads(clean_str)
            # print("✅ JSON解析成功，格式化结果：")
            # print(json.dumps(category_data, indent=4, ensure_ascii=False))
            print(category_data)
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败：{e}")
    else:
        print("未找到分类字符串")

    if category_data:
        leaf_nodes = parse_only_products_leaf(category_data)

        # 打印结果（格式化输出）
        print("✅ 解析出的叶子节点分类：")
        print(json.dumps(leaf_nodes, indent=4, ensure_ascii=False))
        print(len(leaf_nodes))
        file_path = "southchip.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(leaf_nodes, f, indent=2, ensure_ascii=False)



