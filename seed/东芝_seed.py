import os
import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse_search_type_categories(soup):
    """
    解析name=searchType的select标签，提取一级(optgroup.label)^二级(option)的分类和对应URL
    :param soup: BeautifulSoup解析后的对象
    :return: 列表，每个元素为{"url": option的value, "category": "一级分类^二级分类"}
    """
    # 初始化结果列表
    result_list = []
    # 精准匹配：name=searchType的select下的直接子optgroup（按你的要求写法）
    optgroup_list = soup.select('select[name="searchType"] > optgroup')

    # 遍历所有一级分类optgroup
    for optgroup in optgroup_list:
        # 提取一级分类名称（optgroup的label属性），去除前后空格，处理空值
        first_cate = optgroup.get('label', '').strip()
        if not first_cate:  # 过滤无名称的一级分类
            continue
        # 遍历optgroup下的所有二级分类option（叶子节点）
        option_list = optgroup.find_all('option')
        for option in option_list:
            # 提取二级分类的URL（option的value属性），去除前后空格
            second_url = option.get('value', '').strip()
            # 提取二级分类名称，去除前后空格（自动处理换行/多余空格）
            second_cate = option.get_text(strip=True)
            # 过滤无效数据：URL为空或二级分类名称为空的情况
            if "Not Recommended" in second_cate:
                continue
            if not second_url or not second_cate:
                continue
            # 按层级拼接分类名：一级^二级
            full_cate = f"{first_cate}^{second_cate}"
            # 构造指定格式的字典并添加到结果
            result_list.append({
                "url": second_url,
                "category": full_cate
            })
    return result_list
if __name__ == "__main__":

    url = "https://toshiba.semicon-storage.com/ap-en/semiconductor.html"
    response = requests.get(url)
    # print(response.text)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "lxml")
    category_result = parse_search_type_categories(soup)

    # 打印结果（可根据需要保存为JSON/Excel）
    # print("解析结果总数：", len(category_result))
    # print(json.dumps(category_result, indent=4, ensure_ascii=False))
    base_path = "./seed_json"
    file_path = os.path.join(base_path, "toshiba.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(category_result, f, indent=2, ensure_ascii=False)


