import requests
from bs4 import BeautifulSoup
import json
import os
import re


def parse_category_div(category_div: BeautifulSoup) -> list:
    """
    解析category_div，提取叶子节点的URL和层级分类（^拼接）
    Args:
        category_div: BeautifulSoup解析后的fl-list标签对象
    Returns:
        列表，每个元素为{"url": 完整URL, "category": "一级^二级^三级/一级^二级"}
    """
    # 初始化结果列表（去重用）
    result = []
    seen_urls = set()  # 记录已处理的URL，避免重复
    base_domain = "https://www.silan.com.cn"  # 拼接相对路径

    # 1. 遍历所有list（listone/listtwo，内容重复，后续去重）
    category_lists = category_div.find_all("div", class_=lambda x: x in ["list listone", "list listtwo"])
    for cate_list in category_lists:
        # 2. 遍历每个item（一级分类容器）
        items = cate_list.find_all("div", class_="item")
        for item in items:
            # 提取一级分类（清理文本：去掉b标签、多余空格）
            first_cate_elem = item.find("div", class_="items").find("span")
            if not first_cate_elem:
                continue
            # 移除b标签，清理文本
            for b_tag in first_cate_elem.find_all("b"):
                b_tag.extract()
            first_cate = re.sub(r"\s+", " ", first_cate_elem.get_text(strip=True))  # 合并多空格为一个
            if not first_cate:
                continue

            # 3. 遍历item-bot下的twoitem（二级分类容器）
            twoitems = item.find("div", class_="item-bot").find_all("div", class_="twoitem")
            for twoitem in twoitems:
                # 提取二级分类（清理文本）
                second_cate_elem = twoitem.find("a", class_="li")
                if not second_cate_elem:
                    continue
                # 移除b标签，清理文本
                for b_tag in second_cate_elem.find_all("b"):
                    b_tag.extract()
                second_cate = re.sub(r"\s+", " ", second_cate_elem.get_text(strip=True))
                if not second_cate:
                    continue

                # 4. 检查是否有三级分类（three节点）
                three_elem = twoitem.find("div", class_="three")
                if three_elem:
                    # 有三级分类：遍历three下的a标签（叶子节点）
                    leaf_links = three_elem.find_all("a", href=True)  # 只取有href的a标签
                    for link in leaf_links:
                        # 提取URL和三级分类
                        href = link.get("href", "")
                        if not href or href.startswith("javascript:"):
                            continue
                        # 拼接完整URL
                        full_url = href if href.startswith("http") else f"{base_domain}{href}"
                        # 提取三级分类（清理文本）
                        third_cate = re.sub(r"\s+", " ", link.get_text(strip=True))
                        if not third_cate:
                            continue
                        # 拼接层级分类：一级^二级^三级
                        full_cate = f"{first_cate}^{second_cate}^{third_cate}"

                        # 去重：URL未处理过才添加
                        if full_url not in seen_urls:
                            seen_urls.add(full_url)
                            result.append({
                                "url": full_url,
                                "category": full_cate
                            })
                else:
                    # 无三级分类：twoitem的li本身是叶子节点
                    href = second_cate_elem.get("href", "")
                    if not href or href.startswith("javascript:"):
                        continue
                    # 拼接完整URL
                    full_url = href if href.startswith("http") else f"{base_domain}{href}"
                    # 拼接层级分类：一级^二级
                    full_cate = f"{first_cate}^{second_cate}"

                    # 去重：URL未处理过才添加
                    if full_url not in seen_urls:
                        seen_urls.add(full_url)
                        result.append({
                            "url": full_url,
                            "category": full_cate
                        })

    return result


if __name__ == '__main__':
    target_url = "https://www.silan.com.cn/en/index.php/product.html"

    response = requests.get(target_url)

    soup = BeautifulSoup(response.text, "lxml")
    category_div = soup.find("div", class_="fl-list secwen applicationfl-list")
    # print(category_div)

    result = parse_category_div(category_div)
    print(json.dumps(result, indent=4, ensure_ascii=False))
    print(len(result))

    base_path = "./seed_json"
    file_path = os.path.join(base_path, "silan.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)