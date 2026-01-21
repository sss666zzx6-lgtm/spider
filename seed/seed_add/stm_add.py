import json
import os
from util.create_darwin_api import create_api


base_path = "../seed_json"
headers = {
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}

# file_path = os.path.join(base_path, "stm.json")
# with open(file_path, "r", encoding="utf-8") as f:
#     seed_data = json.load(f)
#     for item in seed_data:
#         original_url = item.get("url", "")
#         if not original_url:
#             continue
#
#         if ".html" in original_url:
#             path = original_url.replace(".html", "/products.html")
#             category = item["category"]
#             custom_map = {"category":category}
#             create_api(plan_id="ce83d200f1cc051868306263350618af",path=path,custom_map=custom_map,headers=headers)



# file_path = os.path.join(base_path, "stm.json")
# with open(file_path, "r", encoding="utf-8") as f:
#     seed_data = json.load(f)
#     for i in range(50,100):
#         original_url = seed_data[i].get("url", "")
#         if not original_url:
#             continue
#
#         if ".html" in original_url:
#             path = original_url.replace(".html", "/products.html")
#             category = seed_data[i]["category"]
#             custom_map = {"category":category}
#             create_api(plan_id="ce83d200f1cc051868306263350618af",path=path,custom_map=custom_map,headers=headers)

target_prefixes = (
    "Automotive analog and power",
    "Motor drivers",
    "Power management",
    "Power modules and IPM"
)

file_path = os.path.join(base_path, "stm.json")
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        original_url = item.get("url", "")
        if not original_url:
            continue

        if ".html" in original_url:
            path = original_url.replace(".html", "/products.html")
            category = item["category"]
            if category.startswith(target_prefixes):
                custom_map = {"category":category}
                create_api(plan_id="ce83d200f1cc051868306263350618af",path=path,custom_map=custom_map,headers=headers)
            else:
                print(f"跳过不符合前缀的项：category={category}")