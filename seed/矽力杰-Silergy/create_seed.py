import requests
from bs4 import BeautifulSoup
from lxml import etree
import json

def parse_category_html(soup) -> list:

    result = []


    # 定义递归遍历函数：遍历指定层级的节点，记录已拼接的分类名
    def traverse_node(parent_node, parent_category: str):
        """
        递归遍历分类节点，提取叶子节点
        :param parent_node: 当前层级的父节点（如cat-1/cat-2/cat-3的div）
        :param parent_category: 已拼接的上层分类名（如"DC-DC"）
        """
        # 1. 提取当前节点的a标签（分类名+URL）
        a_tag = parent_node.find("a")
        if not a_tag:
            return
        # 提取当前分类名（去空白）和URL
        current_cat = a_tag.get_text(strip=True)
        current_url = a_tag.get("href", "").strip()
        # 拼接当前层级的分类名（上层+当前，用^分隔）
        full_cat = f"{parent_category}^{current_cat}" if parent_category else current_cat

        # 2. 判断是否有下一级分类节点（cat-2→cat-3→cat-4）
        # 下一级分类的class规则：cat-n → cat-(n+1)，比如cat-1的下一级是cat-2
        next_level = None
        # 查找当前节点下的子分类节点（cat-2/cat-3/cat-4）
        for child in parent_node.children:
            if child.name != "div":
                continue
            # 匹配下一级分类的class（cat-2/cat-3/cat-4）
            if "cat-2" in child.get("class", []) and not next_level:
                next_level = child
            elif "cat-3" in child.get("class", []) and not next_level:
                next_level = child
            elif "cat-4" in child.get("class", []) and not next_level:
                next_level = child

        # 3. 无下一级 → 是叶子节点，加入结果
        url = "https://www.silergy.com" + current_url
        if not next_level:
            result.append({
                "url": url,
                "category": full_cat
            })
        # 4. 有下一级 → 递归遍历下一级所有子节点
        else:
            # 遍历下一级里的所有div（每个div对应一个子分类）
            for sub_div in next_level.find_all("div", recursive=False):
                traverse_node(sub_div, full_cat)

    # 第一步：遍历所有一级分类（cat-1）
    cat_1_list = soup.find_all("div", class_="cat-1")
    for cat_1 in cat_1_list:
        traverse_node(cat_1, "")  # 一级分类的上层分类名为空

    return result

if __name__ == "__main__":
    url = "https://www.silergy.com/classOverview/172"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    nav_ul = soup.find("ul", id="navigation")

    if nav_ul:
        mainnav_li_list = nav_ul.find_all("li", class_="mainnav1")

        for li in mainnav_li_list:
            # 找li下的所有div（和原XPath逻辑一致，提取所有div）
            div_category = li.find("div")
            leaf_categories = parse_category_html(div_category)

            print(json.dumps(leaf_categories, indent=4, ensure_ascii=False))
            print(len(leaf_categories))
            with open("silergy.json", "w", encoding="utf-8") as f:
                json.dump(leaf_categories, f, indent=2, ensure_ascii=False)