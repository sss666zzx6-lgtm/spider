import json
import os
import time

import requests
from bs4 import BeautifulSoup


def extract_poweric_category(soup) :

    # 1. 初始化结果列表
    poweric_category = []

    # 2. 定位核心节点 div.poweric03-box
    poweric_box = soup.select_one("div.poweric03-box")
    if not poweric_box:
        print("未找到 div.poweric03-box 节点")
        return poweric_category

    # 3. 遍历所有 a.poweric03-list 链接
    poweric_links = poweric_box.select("a.poweric03-list")
    for link in poweric_links:
        # 提取URL（href属性）
        url = link.get("href", "").strip()
        # 提取文本（span.poweric03-list-p 的内容）
        name_span = link.select_one("span.poweric03-list-p")
        family_name = name_span.get_text(strip=True) if name_span else ""

        # 4. 过滤空值（URL或文本为空则跳过）
        if not url or not family_name:
            continue

        # 5. 构建指定格式的节点
        category_node = {
            "url": url,
            "familyName": family_name,
            "level": 1,  # 按需求指定level为1
            "children": []  # 无下级节点，children为空
        }
        poweric_category.append(category_node)

    return poweric_category


def fetch_level2_urls(category_result: list) -> list:
    # 遍历每个Level1项
    for level1_item in category_result:
        level1_url = level1_item['url'].strip()
        level1_name = level1_item['familyName']

        if not level1_url:
            print(f"跳过空URL的一级分类：{level1_name}")
            continue

        try:
            # 请求Level1页面
            response = requests.get(url=level1_url)
            if response.status_code != 200:
                print(f"[{level1_name}] 请求失败：HTTP状态码 {response.status_code}")
                continue

            # 解析页面
            response.encoding = response.apparent_encoding or 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')

            # 提取div.kindLinks下的Level2子项
            kind_links = soup.select_one("div.kindLinks")
            if kind_links:
                level2_links = kind_links.select("a.les1")
                for level2_link in level2_links:
                    # 提取Level2的URL和文本
                    level2_url = level2_link.get("href", "").strip()
                    level2_name = level2_link.get_text(strip=True)

                    if level2_url and level2_name:
                        # 构建Level2节点
                        level2_node = {
                            "url": level2_url,
                            "familyName": level2_name,
                            "level": 2,
                            "children": []  # 无更深层级则为空
                        }
                        # 填充到Level1的children中
                        level1_item['children'].append(level2_node)

                print(f"[{level1_name}] 提取到 {len(level1_item['children'])} 个二级分类")
            else:
                print(f"[{level1_name}] 未找到 div.kindLinks 节点")

            # 延时，避免请求过快
            time.sleep(0.3)

        except Exception as e:
            print(f"[{level1_name}] 请求失败：未知错误 - {str(e)[:50]}")

    return category_result


def extract_leaf_nodes_with_category(result: list) -> list:
    """
    遍历分类树，提取叶子节点（children为空），按规则生成category字段
    :param result: 完整的分类树（包含Level1/Level2）
    :return: 叶子节点列表，格式为 [{"url": "", "category": ""}, ...]
    """
    leaf_nodes = []  # 存储最终叶子节点

    def recursive_traverse(node, parent_path: list):
        """
        递归遍历节点，记录层级路径并处理category拼接
        :param node: 当前遍历的节点（Level1/Level2）
        :param parent_path: 从根到当前节点的父层级名称列表
        """
        # 1. 将当前节点名称加入路径
        current_path = parent_path + [node['familyName']]

        # 2. 判断是否是叶子节点（children为空）
        if not node['children']:
            # 3. 处理category拼接规则
            if len(current_path) >= 2 and current_path[-1] == current_path[-2]:
                # 父级名称和叶子节点名称相同 → 仅保留叶子节点名称
                category = current_path[-1]
            else:
                # 否则按层级用^拼接
                category = "^".join(current_path)

            # 4. 生成叶子节点
            leaf_node = {
                "url": node['url'],
                "category": category
            }
            leaf_nodes.append(leaf_node)
        else:
            # 非叶子节点 → 递归遍历子节点
            for child in node['children']:
                recursive_traverse(child, current_path)

    # 5. 遍历所有Level1节点，启动递归
    for level1_node in result:
        recursive_traverse(level1_node, parent_path=[])

    return leaf_nodes

if __name__ == "__main__":
    url = "https://www.fitipower.com/en/product/power-ic"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    # print(soup.prettify())

    category_result = extract_poweric_category(soup)
    result = fetch_level2_urls(category_result)
    print(json.dumps(result, indent=4, ensure_ascii=False))

    leaf_nodes = extract_leaf_nodes_with_category(result)

    base_path = "./seed_json"
    file_path = os.path.join(base_path, "fitipower.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(leaf_nodes, f, indent=2, ensure_ascii=False)