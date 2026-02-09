import json
import os

import requests
from bs4 import BeautifulSoup
import re


def extract_category_url(category_div: BeautifulSoup) -> list:
    """
    提取一级+二级分类（无顶级分类），层级用^拼接，移除URL末尾introduction/
    Args:
        category_div: BeautifulSoup解析后的l_inner对应的Tag对象
    Returns:
        列表，每个元素为{"url": 完整URL, "category": "一级分类^二级分类"}
    """
    result = []
    base_domain = "https://www.nisshinbo-microdevices.co.jp"  # 基础域名

    # 1. 遍历所有一级分类的section（每个section对应一个一级分类）
    section_list = category_div.find_all("section", class_="l_section")
    for section in section_list:
        # 提取一级分类名称（处理h3含a标签、转义字符、多余空格）
        h3_elem = section.find("h3", class_="c_heading5")
        if not h3_elem:
            continue

        # 优先取h3内a标签文本，否则取h3本身文本
        h3_a_elem = h3_elem.find("a", class_="c_heading5__link")
        first_category = h3_a_elem.text.strip() if h3_a_elem else h3_elem.text.strip()
        # 修正转义字符（&amp;→&）和多余空格
        first_category = re.sub(r"&amp;", "&", first_category).replace("  ", " ").strip()

        # 2. 遍历当前一级分类下的二级分类（li里的a.c_link为二级分类）
        li_list = section.find_all("li")
        for li in li_list:
            leaf_a_elem = li.find("a", class_="c_link")
            if not leaf_a_elem:
                continue

            # 提取二级分类名称（修正转义字符）
            second_category = re.sub(r"&amp;", "&", leaf_a_elem.text.strip()).replace("  ", " ").strip()
            # 拼接层级分类（一级^二级）
            full_category = f"{first_category}^{second_category}"

            # 3. 处理URL（移除introduction/ + 拼接完整域名）
            raw_href = leaf_a_elem.get("href", "")
            if not raw_href:
                continue
            # 精准移除末尾的introduction/（含/introduction/或introduction/结尾）
            processed_href = re.sub(r"/?introduction/?$", "", raw_href)
            # 规范URL路径（无参数时末尾补/）
            if not processed_href.endswith("/") and "?" not in processed_href:
                processed_href += "/"
            # 拼接完整URL
            full_url = base_domain + processed_href if raw_href.startswith("/") else processed_href

            # 4. 去重后加入结果
            item = {"url": full_url, "category": full_category}
            if item not in result:
                result.append(item)

    return result


if __name__ == '__main__':

    url = "https://www.nisshinbo-microdevices.co.jp/en/products/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    category_div = soup.find("section", id="Section01")

    if category_div:
        category_div = category_div.find("div",recursive=False)

    # print(category_div)

    result = extract_category_url(category_div)
    print(json.dumps(result, ensure_ascii=False, indent=4))

    base_path = "./seed_json"
    file_path = os.path.join(base_path, "nisshinbo.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)