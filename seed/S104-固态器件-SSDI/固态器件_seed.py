from curl_cffi import requests
import json
from bs4 import BeautifulSoup
import re

def parse_category_leaf_nodes(category_li) -> list:
    """
    解析分类li标签，提取所有叶子节点的分类名和URL
    :param category_li: 最外层的分类li标签（soup.find("li", id="menu-item-539")）
    :return: 叶子节点列表，格式为 [{"url": "", "category": ""}, ...]
    """
    # 存储最终结果
    leaf_nodes = []

    def _recursive_parse(current_li, parent_categories: list):
        """
        递归遍历li节点，提取叶子节点
        :param current_li: 当前遍历的li标签
        :param parent_categories: 父级分类名称列表（用于拼接层级）
        """
        # 1. 提取当前li的a标签（核心：分类名和URL都在a标签里）
        a_tag = current_li.find("a", class_="menu-link")
        if not a_tag:
            return

        # 2. 提取分类名（清理多余空格/换行，排除svg标签的文本）
        # 先去掉a标签内的svg等子标签，只保留纯文本
        for svg in a_tag.find_all("svg"):
            svg.extract()
        # 清理文本：去掉多余空格、换行、制表符
        category_name = re.sub(r"\s+", " ", a_tag.get_text(strip=True)).strip()
        # 提取URL
        category_url = a_tag.get("href", "").strip()

        # 3. 检查当前li是否有子菜单（sub-menu）→ 判断是否是叶子节点
        sub_menu = current_li.find("ul", class_="sub-menu")
        if sub_menu and len(sub_menu.find_all("li")) > 0:
            # 有子菜单 → 递归解析子li，父级分类列表追加当前分类名
            for child_li in sub_menu.find_all("li", recursive=False):
                _recursive_parse(child_li, parent_categories + [category_name])
        else:
            # 无自菜单 → 叶子节点，拼接分类层级（用^分隔）
            full_category = "^".join(parent_categories + [category_name])
            leaf_nodes.append({
                "url": category_url,
                "category": full_category
            })

    # 4. 从最外层li的sub-menu开始递归（跳过Products本身，从一级分类如Rectifiers开始）
    root_sub_menu = category_li.find("ul", class_="sub-menu")
    if root_sub_menu:
        for first_level_li in root_sub_menu.find_all("li", recursive=False):
            _recursive_parse(first_level_li, parent_categories=[])

    return leaf_nodes


if __name__ == '__main__':
    url = "https://ssdi-power.com/products/szu6c62s22/"
    response = requests.get(url=url)
    print(response.status_code)
    soup = BeautifulSoup(response.text, "lxml")

    category_li = soup.find("li", id="menu-item-539")
    # print(category_li.prettify())

    leaf_nodes = parse_category_leaf_nodes(category_li)


    print(json.dumps(leaf_nodes, indent=2, ensure_ascii=False))
    file_path = "ssdi.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(leaf_nodes, f, indent=2, ensure_ascii=False)