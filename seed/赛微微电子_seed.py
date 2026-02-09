import os

import requests
from bs4 import BeautifulSoup
import json


def parse_products_box(products_box: BeautifulSoup) -> list:
    result = []
    # 基础域名（拼接完整URL）
    base_domain = "http://en.cellwise-semi.com"

    # 1. 遍历每个product-item（一级分类容器）
    if not products_box:
        return result

    product_items = products_box.find_all("div", class_="product-item")
    for item in product_items:
        # 提取一级分类（ptitle的文本，去重空格/换行）
        ptitle_elem = item.find("div", class_="ptitle")
        if not ptitle_elem:
            continue
        first_category = ptitle_elem.get_text(strip=True)  # strip=True自动去除首尾空格/换行

        # 2. 遍历当前一级分类下的所有叶子节点（sublinks里的a标签）
        sublinks_elem = item.find("div", class_=lambda x: x and x.startswith("sublinks"))
        if not sublinks_elem:
            continue
        a_tags = sublinks_elem.find_all("a")

        for a in a_tags:
            # 提取二级分类（a标签文本，去重空格/换行）
            second_category = a.get_text(strip=True)
            if not second_category:
                continue

            # 拼接完整URL（处理相对路径）
            href = a.get("href", "")
            if not href:
                continue
            full_url = base_domain + href if href.startswith("/") else href

            # 拼接层级分类（一级^二级）
            category = f"{first_category}^{second_category}"

            # 构造字典并加入结果列表
            result.append({
                "url": full_url,
                "category": category
            })

    return result


if __name__ == '__main__':
    url = "http://en.cellwise-semi.com/Home/Index/products"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    products_box = soup.find('div', class_='products-box')

    result = parse_products_box(products_box)

    print(json.dumps(result, indent=4, ensure_ascii=False))

    base_path = "./seed_json"
    file_path = os.path.join(base_path, "cellwise.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
