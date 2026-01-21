import json
import os
from util.create_darwin_api import create_api

base_path = "../seed_json"

file_path = os.path.join(base_path, "fitipower.json")
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        path = item["url"]
        category = "Power IC^" + item["category"]
        custom_map = {"category": category}
        create_api(plan_id="8358bf6fe667347c1b5973a3760d58c4", path=path, custom_map=custom_map)

