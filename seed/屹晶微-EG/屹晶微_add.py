import json
import os
from util.create_darwin_api import create_api

# base_path = "../seed_json"

file_path = "egmicro.json"
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        path = item["url"] + "&lang=en"
        category = item["category"]
        custom_map = {"category": category}
        create_api(plan_id="0c16e595b08aeb65147e050cdacf5463", path=path, custom_map=custom_map)