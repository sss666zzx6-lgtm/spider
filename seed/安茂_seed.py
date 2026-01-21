import json
import os
import requests
from bs4 import BeautifulSoup
BASE_URL = "https://www.ame.com.tw"


def get_product_menu(soup):
    target_li = soup.select_one("#menu-item-641")
    if not target_li:
        print("未找到id=menu-item-641的li元素")
        return []

    # 2. 找到该li下的ul.sub-menu（子菜单）
    sub_menu_ul = target_li.find('ul', class_='sub-menu')
    if not sub_menu_ul:
        print("未找到子菜单ul.sub-menu")
        return []

    # 3. 遍历ul下的所有li，提取文本和href
    result_list = []
    for li in sub_menu_ul.find_all('li'):
        # 提取a标签
        a_tag = li.find('a')
        if not a_tag:
            continue

        # 提取href（处理转义字符&#038; → &，拼接相对路径）
        href = a_tag.get('href', '').strip()
        # 替换HTML转义字符
        href = href.replace('&#038;', '&')
        # 拼接完整URL（如果是相对路径）
        if href.startswith('?'):
            full_href = f"{BASE_URL}/{href}"
        elif not href.startswith('http'):
            full_href = f"{BASE_URL}{href}"
        else:
            full_href = href

        # 提取span标签的文本（菜单名称）
        span_tag = a_tag.find('span')
        menu_text = span_tag.get_text(strip=True) if span_tag else ""

        # 过滤空数据，添加到结果列表
        if menu_text and full_href:
            result_item = {
                "url": full_href,  # 对应span的文本
                "category": menu_text  # 对应a标签的完整href
            }
            result_list.append(result_item)

    return result_list




if __name__ == "__main__":
    url = "https://www.ame.com.tw/?lang=en"

    response = requests.get(url)

    # print(response.text)

    soup = BeautifulSoup(response.text, 'lxml')
    product_menu_list = get_product_menu(soup)

    base_path = "./seed_json"
    file_path = os.path.join(base_path, "ame.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(product_menu_list, f, indent=2, ensure_ascii=False)