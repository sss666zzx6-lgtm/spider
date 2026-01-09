import json
import os
from util.create_darwin_api import create_api

base_path = "../seed_json"


file_path = os.path.join(base_path, "beiling.json")
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        original_url = item.get("url", "")
        if not original_url:
            continue

        if "product_list.html" in original_url:
            path = original_url.replace("product_list.html", "get_ppi_item")
            category = item["category"]
            custom_map = {"category": category}
            create_api(plan_id="63d0d509ff414b0d9e3778066f93ca05", path=path, custom_map=custom_map)