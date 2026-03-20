import json
import os
from util.create_darwin_api import create_api

# base_path = "../seed_json"

file_path = "ssdi.json"
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        path = item["url"]
        category = item["category"]
        custom_map = {"category": category}
        create_api(plan_id="192011c6132aa08f3ad6a12bed0a7bb1", path=path,
           custom_map=custom_map)

