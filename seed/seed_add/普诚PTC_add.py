import json
import os
from util.create_darwin_api import create_api
from urllib.parse import quote

base_path = "../seed_json"

file_path = os.path.join(base_path, "princeton.json")
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        encoded_path = quote(item["url"].strip(), safe=':/?&=')
        path = encoded_path
        # print(path)
        category = item["category"]
        custom_map = {"category": category}
        create_api(plan_id="23755935a07e9b683fb7ac6907ff54f7", path=path, custom_map=custom_map)

