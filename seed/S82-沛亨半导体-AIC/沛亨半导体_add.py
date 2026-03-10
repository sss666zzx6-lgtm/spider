import json
import os
from util.create_darwin_api import create_api

# base_path = "../seed_json"

file_path = "analog.json"
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        path = item["url"]
        category = item["category"]
        custom_map = {"category": category}
        create_api(plan_id="a6da5f2f712354486682376a0fbb5449", path=path, custom_map=custom_map)