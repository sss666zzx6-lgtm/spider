import requests
from bs4 import BeautifulSoup
import json
import re


def parse_product_leaf_nodes(s2_menu_ul, base_url, level_category):
    """
    解析ul.s2_menu节点，提取叶子节点的URL和层级分类名
    :param s2_menu_ul: BeautifulSoup解析后的ul.s2_menu节点
    :param base_url: 基础URL（https://auk.co.kr），用于拼接相对路径
    :param level_category: 一级分类名（从article.arti01 h3提取的文本）
    :return: 叶子节点列表，格式[{"url": "", "category": ""}]
    """
    leaf_nodes = []
    # 校验输入节点是否有效
    if not s2_menu_ul:
        return leaf_nodes

    # 清理一级分类名（去除多余空格/换行）
    level_category = re.sub(r'\s+', ' ', level_category).strip() if level_category else ""

    # 遍历所有二级分类li节点（s2_menu下的直接li子节点）
    second_level_li_list = s2_menu_ul.find_all("li", recursive=False)
    for second_li in second_level_li_list:
        # 提取二级分类名（dl>dt文本）
        dt_tag = second_li.find("dt")
        second_category = ""
        if dt_tag:
            second_category = re.sub(r'\s+', ' ', dt_tag.get_text(strip=True)).strip()
        if not second_category:
            continue

        # 找到叶子节点容器（dd>ul下的li>a）
        dd_tag = second_li.find("dd")
        if not dd_tag:
            continue
        leaf_ul = dd_tag.find("ul")
        if not leaf_ul:
            continue

        # 遍历所有叶子节点a标签
        leaf_a_list = leaf_ul.find_all("a")
        for a_tag in leaf_a_list:
            # 提取三级分类名（叶子节点文本）
            third_category = re.sub(r'\s+', ' ', a_tag.get_text(strip=True)).strip()
            if not third_category:
                continue

            # 提取并拼接URL
            href = a_tag.get("href", "").strip()
            if not href:
                continue
            # 判断是否为绝对路径（http开头）
            if href.startswith(("http://", "https://")):
                full_url = href
            else:
                # 拼接相对路径（处理/开头和非/开头的情况）
                if href.startswith("/"):
                    full_url = f"{base_url}{href}"
                else:
                    full_url = f"{base_url}/{href}"

            # 拼接分类层级（一级^二级^三级）
            category_path = f"{level_category}^{second_category}^{third_category}"

            # 构造叶子节点字典
            leaf_node = {
                "url": full_url,
                "category": category_path
            }
            leaf_nodes.append(leaf_node)

    return leaf_nodes

if __name__ == "__main__":
    urls = [f"https://auk.co.kr/eng/s2/product.asp?idx={i}" for i in range(1, 4)]
    product_leaf_nodes = []
    for url in urls:
        base_url = "https://auk.co.kr"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        first_h3  = soup.select_one("article.arti01 h3")
        print(first_h3 .text)
        level_category = first_h3 .text
        s2_menu_ul = soup.find("ul", class_="s2_menu")
        # print(s2_menu_ul.prettify())


        leaf_nodes = parse_product_leaf_nodes(s2_menu_ul, base_url,level_category)
        # print(json.dumps(leaf_nodes, indent=2, ensure_ascii=False))
        print(f"\n========== 解析完成 ==========")
        print(f"📊 共解析出 {len(leaf_nodes)} 个叶子节点")
        product_leaf_nodes += leaf_nodes
    print(json.dumps(product_leaf_nodes, indent=2, ensure_ascii=False))
    file_path = "auk.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(product_leaf_nodes, f, indent=2, ensure_ascii=False)
