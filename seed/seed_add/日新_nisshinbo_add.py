import json
import os
from util.create_darwin_api import create_api
from urllib.parse import urlparse, parse_qs


base_path = "../seed_json"

file_path = os.path.join(base_path, "nisshinbo.json")
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        path = item["url"]
        category = item["category"]
        custom_map = {"category": category}
        create_api(plan_id="5b07f33da5c96da1062bf20de26716ab", path=path, custom_map=custom_map)

# data = {
#     "category_product_division_code": "watchdog-timer",
#     "language_code": "en",
#     "product_grade": "all"
# }
#
# path = "https://www.nisshinbo-microdevices.co.jp/api/parametric-search/getData.do"
# category = "666666"
# custom_map = {"category": category}
# create_api(plan_id="5b07f33da5c96da1062bf20de26716ab", path=path, custom_map=custom_map
#            ,http_request = "POST",request_body = data,post_media_type="FORM")