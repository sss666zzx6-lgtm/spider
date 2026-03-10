import json
import os
from util.create_darwin_api import create_api

# base_path = "../seed_json"

file_path = "auk.json"
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        path = item["url"]
        if "leds.asp" in path:
            path = path.replace("leds", "product_list")
            print(path)
        category = item["category"]
        custom_map = {"category": category}
        create_api(plan_id="d03e2b241ef8eb0944e12cde05e57662", path=path, custom_map=custom_map)