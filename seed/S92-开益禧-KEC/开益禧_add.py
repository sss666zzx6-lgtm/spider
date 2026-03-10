import json
import os
from util.create_darwin_api import create_api

# base_path = "../seed_json"

file_path = "keccorp.json"
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        part_idx = item["url"].split("part_idx=")[1]
        path = f"https://www.keccorp.com/en/include/finder.asp?part_idx={part_idx}&sunsu=&search_v="
        # print(path)
        category = item["category"]
        custom_map = {"category": category}
        create_api(plan_id="155cfcd7377c1e2d5d5f865a0310a8f0", path=path, custom_map=custom_map)