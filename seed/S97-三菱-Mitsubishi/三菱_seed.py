import json
import requests
from bs4 import BeautifulSoup


def extract_division_checkbox(soup):
    """
    从soup中提取class="check-box division"下的checkbox信息
    :param soup: BeautifulSoup解析后的对象
    :return: dict {label文本: input的value值}
    """
    # 初始化字典存储结果
    division_dict = {}

    # 1. 找到class="check-box division"的父div（注意class有两个值，需精准匹配）
    parent_div = soup.find("div", class_="check-box division")
    child_divs = parent_div.find_all("div",recursive=False)
    for child_div in child_divs:
        input_value = child_div.find("input")["value"] if product_category.find("input") else ""
        # 提取label文本
        label_text = child_div.find("label").get_text(strip=True) if product_category.find("label") else ""

        # 存入字典（label文本为key，value为值）
        division_dict[label_text] = input_value

    return division_dict

if __name__ == "__main__" :
    url = "https://www.mitsubishielectric.com/semiconductors/app/SearchDevice.aspx"
    leaf_nodes = []
    response = requests.post(url)
    soup = BeautifulSoup(response.text, "lxml")
    product_category_group = soup.find("div", class_="product-category-group")
    productCategoryId = {}
    if product_category_group:
        product_category_list = product_category_group.find_all("div",recursive=False)
        print(len(product_category_list))
        for product_category in product_category_list:
            value = product_category.find("input")["value"] if product_category.find("input") else ""
            # 提取label文本
            label_text = product_category.find("label").get_text(strip=True) if product_category.find("label") else ""

            productCategoryId[label_text] = value

    for label_text, value in productCategoryId.items():
        print(f"标签文本：{label_text} → 对应value值：{value}")
        url = "https://www.mitsubishielectric.com/semiconductors/app/Condition.aspx"
        data = {
            "productCategoryId": f"{value}",
            "productCategoryName": f"{label_text}",
            "__RequestVerificationToken": ""
        }
        print(data)
        res = requests.post(url, data=data)
        soup_2 = BeautifulSoup(res.text, "lxml")
        # print(soup_2.prettify())
        division_result = extract_division_checkbox(soup_2)
        for label_text_2, value_2 in division_result.items():
            print(f"{label_text_2} → Value值：{value_2}")
            data = {
                "productCategoryName": f"{label_text}",
                "ProductCategoryId": f"{value}",
                "TypeName": "",
                "VoltageClass": "",
                "ConnectionCode": "",
                "RatedCurrentLower": "",
                "RatedCurrentUpper": "",
                "DeprecationCodeList%5B0%5D": "37",
                "DeprecationCodeList%5B1%5D": "40",
                "DeprecationCodeList%5B2%5D": "39",
                "DeprecationCodeList%5B3%5D": "38",
                "DivisionCodeList%5B0%5D": value_2,
                "TypeNameLabel": label_text_2,
                "__RequestVerificationToken": ""
            }
            if label_text_2 == label_text:
                leaf_nodes.append({
                    "data": data,
                    "category":f"{label_text}",
                })
            else :
                leaf_nodes.append({
                    "data": data,
                    "category": f"{label_text}^{label_text_2}",
                })

    file_path = "mitsubishielectric.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(leaf_nodes, f, indent=2, ensure_ascii=False)
