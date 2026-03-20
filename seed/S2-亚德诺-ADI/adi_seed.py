# -*- coding: utf-8 -*-
"""
@Time    : 2025/12/29 10:59
@Author  : Jason
@Ver     : Python3.13
"""
from curl_cffi import requests
from lxml import etree
import json
import re


def process_categories(categories, parent_names=None):
    """
    递归处理分类数据，当options为空时将多层name用^拼接
    """
    if parent_names is None:
        parent_names = []

    results = []

    for category in categories:
        title = category.get("name", "")
        current_names = parent_names + [title]
        options = category.get("options", [])

        # 检查options是否存在且不为空
        if options:
            # 如果options不为空，递归处理子选项
            results.extend(process_categories(options, current_names))
        else:
            # 如果options为空，将当前路径的name用^拼接
            path = "^".join(current_names)
            if path not in [
                "Product Categories",
                "New Products",
                "Voltage References"]:
                pst_href = category.get("pstHref")
                # 'https://www.analog.com/en/parametricsearch/2989'
                pattern = r"parametricsearch/(\d+)"
                ids = re.findall(pattern, pst_href)
                if ids:
                    pst_id = ids[0]
                    url = f"https://www.analog.com/cdp/pst2/data/standard/{pst_id}.js"
                    # url = "https://www.analog.com/cdp/pst2/data/standard/3675.js"
                    results.append({
                        "name": path,
                        "url": url,
                    })

    return results

rd_file = "analog-category.json"
ot_file = "analog-clean-category.json"
# category_file = "analog-category.json"
with open(rd_file, "r", encoding="utf-8") as f:
    content = f.read()
categories_dic = json.loads(content)
categories = categories_dic["menu"][0].get("options")
# for category in categories:
#     title = category.get("name", "")
#     options = category.get("options", "")
final_results = process_categories(categories)
result = []
print(json.dumps(final_results, ensure_ascii=False))
plan_id = "1167a8ceac0659bf76028c53d869a177"
# 打印结果
for item in final_results:
    print(item)
    url = item["url"]
    result.append({"url": url, "name": item["name"]})
with open(ot_file, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)


