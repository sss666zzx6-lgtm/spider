import json
import os
from util.create_darwin_api import create_api

base_path = "../seed_json"

file_path = os.path.join(base_path, "manbasemi.json")
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        path = item["url"]
        category = item["category"]
        custom_map = {"category": category}
        create_api(plan_id="c9364ed2bd4b6071f8f48ec198973e66", path=path, custom_map=custom_map)