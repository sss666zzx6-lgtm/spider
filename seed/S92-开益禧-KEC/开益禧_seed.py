import requests
from bs4 import BeautifulSoup
import json
import re
from curl_cffi import requests

def parse_product_leaf_nodes(category_ul):
    """
    解析分类ul节点，提取叶子节点的URL和层级分类名（层级用^拼接）
    :param category_ul: BeautifulSoup解析后的目标ul节点（class="clearfix"的ul）
    :return: 叶子节点列表，格式[{"url": "", "category": ""}]
    """
    leaf_nodes = []
    # 校验输入节点是否有效
    if not category_ul:
        return leaf_nodes

    # 清理文本的辅助函数（去除多余空格/换行，处理特殊字符如&amp;）
    def clean_text(text):
        if not text:
            return ""
        # 替换&amp;为&，去除多余空格/换行，首尾去空格
        cleaned = re.sub(r'\s+', ' ', text).replace("&amp;", "&").strip()
        return cleaned

    # 遍历最外层的一级li（Discrete、IC等）
    first_level_li_list = category_ul.find_all("li", recursive=False)
    for first_li in first_level_li_list:
        # 提取一级分类名（最外层li下的span文本）
        first_level_span = first_li.find("span")
        first_category = clean_text(first_level_span.get_text() if first_level_span else "")
        if not first_category:
            continue

        # 找到二级分类容器（gnb-3dep）
        second_level_ul = first_li.find("ul", class_="gnb-3dep")
        if not second_level_ul:
            continue

        # 遍历二级分类li
        second_level_li_list = second_level_ul.find_all("li", recursive=False)
        for second_li in second_level_li_list:
            # 提取二级分类名（gnb-3dep li下的span文本）
            second_level_span = second_li.find("span")
            second_category = clean_text(second_level_span.get_text() if second_level_span else "")
            if not second_category:
                continue

            # 找到叶子节点容器（gnb-4dep，最内层ul）
            leaf_level_ul = second_li.find("ul", class_="gnb-4dep")
            if not leaf_level_ul:
                continue

            # 遍历叶子节点li（最内层，无后续子ul）
            leaf_li_list = leaf_level_ul.find_all("li", recursive=False)
            for leaf_li in leaf_li_list:
                # 提取叶子节点的a标签
                leaf_a = leaf_li.find("a")
                if not leaf_a:
                    continue

                # 提取叶子节点URL
                leaf_url = leaf_a.get("href", "").strip()
                if not leaf_url:
                    continue

                # 提取三级分类名（叶子节点span文本）
                leaf_span = leaf_a.find("span")
                third_category = clean_text(leaf_span.get_text() if leaf_span else "")
                if not third_category:
                    continue

                # 拼接层级分类名（一级^二级^三级）
                full_category = f"{first_category}^{second_category}^{third_category}"

                # 构造叶子节点字典
                leaf_node = {
                    "url": leaf_url,
                    "category": full_category
                }
                leaf_nodes.append(leaf_node)

    return leaf_nodes

if __name__ == "__main__":
    url = "https://www.keccorp.com/en/product/product_value.asp?part_idx=3"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    category_ul  = soup.select_one("li.gnb1 ul")
    # print(category_ul.prettify())


    leaf_nodes = parse_product_leaf_nodes(category_ul)
    print(json.dumps(leaf_nodes, indent=2, ensure_ascii=False))
    print(f"\n========== 解析完成 ==========")
    print(f"📊 共解析出 {len(leaf_nodes)} 个叶子节点")

    file_path = "keccorp.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(leaf_nodes, f, indent=2, ensure_ascii=False)
