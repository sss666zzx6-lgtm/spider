import json
import os
from util.create_darwin_api import create_api

base_path = "../seed_json"

file_path = os.path.join(base_path, "fremontmicro.json")
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        path = item["url"]
        category = item["category"]
        custom_map = {"category": category}
        create_api(plan_id="38df481183ffa2354350f901570c0b8b", path=path, custom_map=custom_map)