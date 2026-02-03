import os
import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse_category(soup):
    """
    适配【多个】div.class=heading_wrapper的场景：
    1. 遍历所有heading_wrapper，每个作为独立一级分类容器
    2. 每个heading_wrapper取自身下一个兄弟节点作为专属二级分类容器
    3. 汇总所有一级^二级分类，返回[{"url": "", "category": ""}]格式
    :param soup: BeautifulSoup解析后的对象
    :return: 符合格式的分类列表，无数据则返回空列表
    """
    result_list = []
    # 核心修改1：从find改为find_all，获取【所有】heading_wrapper节点
    first_cate_div_list = soup.find_all("div", class_="heading_wrapper")
    if not first_cate_div_list:  # 无任何一级分类容器，直接返回
        return result_list

    # 核心修改2：循环遍历每个heading_wrapper，独立处理
    for first_cate_div in first_cate_div_list:
        # 提取当前一级分类名称
        h2_tag = first_cate_div.find("h2", class_="lms_heading_title")
        if not h2_tag:  # 无h2标题，跳过当前heading_wrapper
            continue
        span_tag = h2_tag.find("span")
        if not span_tag:  # 无span文本容器，跳过当前heading_wrapper
            continue
        first_cate = span_tag.get_text(strip=True)
        if not first_cate:  # 一级分类名称为空，跳过当前heading_wrapper
            continue

        # 取当前heading_wrapper的【下一个直接兄弟节点】（专属二级分类容器）
        second_cate_container = first_cate_div.find_next_sibling()
        if not second_cate_container:  # 无二级容器，跳过当前heading_wrapper
            continue

        # 定位当前二级容器中的所有二级a标签（精准匹配，避免无关a标签）
        second_a_list = second_cate_container.select("ul.linklist > li.linkitem > a")
        if not second_a_list:  # 无二级分类，跳过当前heading_wrapper
            continue

        # 遍历当前二级分类，构造结果
        for a in second_a_list:
            second_url = a.get("href", "").strip()
            second_cate = a.get_text(strip=True)
            if not second_url or not second_cate:  # 过滤无效二级分类
                continue
            full_cate = f"{first_cate}^{second_cate}"
            result_list.append({
                "url": second_url,
                "category": full_cate
            })
    return result_list


if __name__ == "__main__":

    url = "https://www.princeton.com.tw/zh-cn/%E4%BA%A7%E5%93%81%E6%80%BB%E8%A7%88"
    response = requests.get(url,verify=False)
    # print(response.text)
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, "lxml")
    category_result = parse_category(soup)

    print("解析结果总数：", len(category_result))
    print(json.dumps(category_result, indent=4, ensure_ascii=False))
    base_path = "./seed_json"
    file_path = os.path.join(base_path, "princeton.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(category_result, f, indent=2, ensure_ascii=False)


