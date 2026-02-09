import json
import os
from util.create_darwin_api import create_api

base_path = "../seed_json"

# file_path = os.path.join(base_path, "analog-clean-category.json")
# with open(file_path, "r", encoding="utf-8") as f:
#     seed_data = json.load(f)
#     for item in seed_data:
#         path = item["url"]
#         category = item["name"]
#         custom_map = {"category": category}
#         create_api(plan_id="1167a8ceac0659bf76028c53d869a177", path=path, custom_map=custom_map)


# file_path = os.path.join(base_path, "analog-clean-category.json")
# with open(file_path, "r", encoding="utf-8") as f:
#     seed_data = json.load(f)
#     for i in range(50):
#         path = seed_data[i]["url"]
#         category = seed_data[i]["name"]
#         custom_map = {"category": category}
#         create_api(plan_id="1167a8ceac0659bf76028c53d869a177", path=path, custom_map=custom_map)
target_prefixes = (
    "Power Management",
    "Isolation",
    "Motors & Motion Contro"
)

file_path = os.path.join(base_path, "analog-clean-category.json")
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        path = item["url"]
        category = item["name"]
        if category.startswith(target_prefixes):
            custom_map = {"category": category}
            create_api(plan_id="1167a8ceac0659bf76028c53d869a177", path=path, custom_map=custom_map,fetch_method=2)
        else:
            print(f"跳过不符合前缀的项：category={category}")
