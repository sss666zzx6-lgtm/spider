import json
import os
from util.create_darwin_api import create_api

# base_path = "../seed_json"

def extract_url_segment(url):
    stripped_url = url.strip("/")
    # 步骤2：按"/"分割成路径列表
    path_parts = stripped_url.split("/")
    # 步骤3：取最后一个非空片段（兼容空URL/异常URL）
    if path_parts and path_parts[-1]:
        return path_parts[-1]
    return ""

file_path = "wolfspeed.json"
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        # url_segment = extract_url_segment(item["url"])
        # print(url_segment)
        # path = f"https://www.wolfspeed.com/page-data/products/power/{url_segment}/page-data.json"
        path = f"https://www.wolfspeed.com{item['url']}"
        category = item["category"]
        custom_map = {"category": category}
        create_api(plan_id="561b8dfe7470b392c6069a018d3079fd", path=path,
           custom_map=custom_map)
