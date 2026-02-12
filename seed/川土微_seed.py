import requests
from bs4 import BeautifulSoup
import json
import os
import re


def parse_sbcp_category(category_ul: BeautifulSoup) -> list:
    result = []
    # 去重集合（避免重复URL）
    seen_urls = set()
    base_domain = "https://e.chipanalog.com"

    # 1. 遍历所有一级分类（sbcp-li）
    first_level_li_list = category_ul.find_all("li", class_="sbcp-li")
    for first_li in first_level_li_list:
        # 提取一级分类文本（清理多余空格/换行）
        first_cate_elem = first_li.find("div", class_="sbcp-li-top").find("a", class_="std-word1")
        if not first_cate_elem:
            continue
        first_cate = re.sub(r"\s+", " ", first_cate_elem.get_text(strip=True))  # 合并多空格
        if not first_cate:
            continue

        # 2. 找到一级分类下的二级容器（sbcp-li-btm）
        second_level_ul = first_li.find("ul", class_="sbcp-li-btm")
        if not second_level_ul:
            continue

        # 3. 遍历所有二级分类（sbcp-li-btm-li）
        second_level_li_list = second_level_ul.find_all("li", class_="sbcp-li-btm-li")
        for second_li in second_level_li_list:
            # 提取二级分类文本
            second_cate_elem = second_li.find("div", class_="slbl-top").find("a", class_="std-word1")
            if not second_cate_elem:
                continue
            second_cate = re.sub(r"\s+", " ", second_cate_elem.get_text(strip=True))
            if not second_cate:
                continue

            # 4. 找到二级分类下的叶子节点容器（slbl-btm）
            leaf_container = second_li.find("div", class_="slbl-btm")
            if not leaf_container:
                continue

            # 5. 遍历所有叶子节点（slbl-li）
            leaf_li_list = leaf_container.find_all("div", class_="slbl-li")
            for leaf_li in leaf_li_list:
                # 提取叶子节点的URL和三级分类文本
                leaf_a_elem = leaf_li.find("a", class_="std-word1", href=True)
                if not leaf_a_elem:
                    continue

                # 提取URL（可选：拼接基础域名得到完整URL）
                leaf_href = leaf_a_elem.get("href", "").strip()
                # 若需完整URL，取消下面注释：
                # leaf_url = f"{base_domain}{leaf_href}" if leaf_href else ""
                # 若保留相对路径，使用：
                leaf_url = leaf_href

                # 提取三级分类文本
                third_cate = re.sub(r"\s+", " ", leaf_a_elem.get_text(strip=True))
                if not third_cate:
                    continue

                # 6. 拼接层级分类（一级^二级^三级）
                full_cate = f"{first_cate}^{second_cate}^{third_cate}"

                # 7. 去重（URL唯一）
                if leaf_url not in seen_urls:
                    seen_urls.add(leaf_url)
                    result.append({
                        "url": base_domain + leaf_url,
                        "category": full_cate
                    })

    return result

if __name__ == '__main__':
    target_url = "https://e.chipanalog.com/products/power/isolated-driver/standard-isolated-driver"

    response = requests.get(target_url)

    soup = BeautifulSoup(response.text, "lxml")
    category_ul = soup.find("ul", class_="sbcp-ul")
    print(category_ul)

    result = parse_sbcp_category(category_ul)
    print(json.dumps(result, indent=4, ensure_ascii=False))
    print(len(result))

    base_path = "./seed_json"
    file_path = os.path.join(base_path, "chipanalog.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)