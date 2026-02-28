import requests
from lxml import etree
import json


def parse_product_leaf_nodes(products, base_url="https://www.egmicro.com"):

    leaf_nodes = []

    # 遍历每个一级分类（product-card）
    for product_card in products:
        # 1. 提取一级分类名称（h3标签文本）
        first_level_elem = product_card.xpath(".//h3/text()")
        if not first_level_elem:
            continue  # 无一级分类名称则跳过
        first_level_name = first_level_elem[0].strip()  # 去除前后空格/换行

        # 2. 提取该一级分类下的所有二级叶子节点（li.products-li > a）
        second_level_elems = product_card.xpath(".//li[@class='products-li']/a")
        for a_elem in second_level_elems:
            # 提取二级分类名称
            second_level_name = a_elem.xpath("text()")[0].strip() if a_elem.xpath("text()") else ""
            if not second_level_name:
                continue

            # 提取二级分类URL（处理相对路径）
            relative_url = a_elem.xpath("@href")[0].strip() if a_elem.xpath("@href") else ""
            if relative_url:
                # 拼接完整URL（处理绝对/相对路径）
                if relative_url.startswith("http"):
                    full_url = relative_url
                else:
                    full_url = f"{base_url}{relative_url}" if not relative_url.startswith(
                        "/") else f"{base_url}{relative_url}"
            else:
                full_url = ""

            # 拼接分类层级（一级^二级）
            full_category = f"{first_level_name}^{second_level_name}"

            # 添加到结果列表
            leaf_nodes.append({
                "url": full_url,
                "category": full_category
            })

    return leaf_nodes


if __name__ == "__main__":
    url = "https://www.egmicro.com/products/?lang=en"
    base_url = "https://www.egmicro.com"
    response = requests.get(url)
    tree = etree.HTML(response.text)
    # print(soup.prettify())
    products = tree.xpath("//div[@class='container']//div[@class='product-card']")

    leaf_nodes = parse_product_leaf_nodes(products, base_url)

    # 打印结果验证
    print("解析出的叶子节点：")
    for idx, node in enumerate(leaf_nodes, 1):
        print(f"{idx}. {node}")

    file_path = "egmicro.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(leaf_nodes, f, indent=2, ensure_ascii=False)
