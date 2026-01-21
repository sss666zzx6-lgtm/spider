import json
import os
import requests
from bs4 import BeautifulSoup
BASE_URL = "https://www.anpec.com.tw"

def get_anpec_category_tree(soup):
    # 匹配核心节点：修正后的选择器（后代元素）
    target_panel_box = soup.select_one("li.megaMenu > div.subMenuBox.menu_product .panelBox")
    if not target_panel_box:
        print("未找到目标panelBox节点")
        return []

    category_tree = []

    # 遍历每个panel（level=1分类）
    panels = target_panel_box.find_all('div', class_='panel')
    for panel in panels:
        panel_header = panel.find('div', class_='panel_header')
        if not panel_header:
            continue

        # 清理文本
        level1_name = panel_header.get_text(strip=True)
        level1_a_tag = panel_header.find('a')
        level1_url = ""
        if level1_a_tag:
            level1_url = level1_a_tag.get('href', '').strip()
            if level1_url and not level1_url.startswith('http'):
                level1_url = f"{BASE_URL}{level1_url}"
            level1_name = level1_a_tag.get_text(strip=True) or level1_name

        if not level1_name:
            continue

        # 初始化level1节点（children默认空）
        level1_node = {
            "familyName": level1_name,
            "level": 1,
            "url": level1_url,
            "children": []
        }

        # ===== 提取level2信息（仅当有submenu时才生成）=====
        submenu_ul = panel.find('ul', class_='submenu')
        if submenu_ul:
            # 有submenu → 正常生成level2
            submenu_li_list = submenu_ul.find_all('li')
            for li in submenu_li_list:
                a_tag = li.find('a')
                if not a_tag:
                    continue

                level2_name = a_tag.get_text(strip=True)
                level2_url = a_tag.get('href', '').strip()
                if level2_url and not level2_url.startswith('http'):
                    level2_url = f"{BASE_URL}{level2_url}"

                if level2_name:
                    level2_node = {
                        "familyName": level2_name,
                        "level": 2,
                        "url": level2_url,
                        "children": []
                    }
                    level1_node['children'].append(level2_node)
        # ===== 关键修正：删除else分支，无submenu时children保持为空 =====
        # （不再强行生成level2，level1自身作为叶子节点）

        category_tree.append(level1_node)

    return category_tree


def extract_anpec_leaf_nodes(category_tree: list) -> list:
    """
    遍历分类树，提取所有叶子节点（children为空）
    :param category_tree: 解析后的anpec分类树
    :return: 叶子节点列表，格式为 [{"url": "", "category": ""}, ...]
    """
    leaf_nodes = []  # 存储最终结果

    def recursive_traverse(node, parent_path: list):
        """
        递归遍历节点，拼接层级路径
        :param node: 当前遍历的节点（level1/level2）
        :param parent_path: 父层级的名称列表（用于拼接category）
        """
        # 1. 将当前节点的名称加入路径
        current_path = parent_path + [node['familyName']]

        # 2. 判断是否是叶子节点（children为空）
        if not node['children']:
            # 生成叶子节点：url取当前节点的url，category用^拼接路径
            leaf_node = {
                "url": node['url'],
                "category": "^".join(current_path)
            }
            leaf_nodes.append(leaf_node)
        else:
            # 非叶子节点 → 递归遍历子节点
            for child in node['children']:
                recursive_traverse(child, current_path)

    # 3. 遍历所有level1节点，启动递归
    for level1_node in category_tree:
        recursive_traverse(level1_node, parent_path=[])

    return leaf_nodes

if __name__ == "__main__":
    url = "https://www.anpec.com.tw/en/"

    response = requests.get(url)

    # print(response.text)

    soup = BeautifulSoup(response.text, 'lxml')
    category_tree = get_anpec_category_tree(soup)
    print(json.dumps(category_tree, indent=4, ensure_ascii=False))

    leaf_nodes = extract_anpec_leaf_nodes(category_tree)
    base_path = "./seed_json"
    file_path = os.path.join(base_path, "anpec.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(leaf_nodes, f, indent=2, ensure_ascii=False)