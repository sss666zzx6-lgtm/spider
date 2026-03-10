import json
import os
from util.create_darwin_api import create_api

# base_path = "../seed_json"

file_path = "mitsubishielectric.json"
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        data = item["data"]
        path = "https://www.mitsubishielectric.com/semiconductors/app/SearchResult.aspx"
        category = item["category"]
        custom_map = {"category": category}
        create_api(plan_id="46eb191842abc3bfb676b2ec8af4e90e", path=path,post_media_type="FORM",
           custom_map=custom_map,http_request="POST",request_body=data)

#
# path = "https://www.mitsubishielectric.com/semiconductors/app/SearchResult.aspx"
#
# data = {
#     "productCategoryName": "Power Modules",
#     "ProductCategoryId": "0",
#     "TypeName": "",
#     "VoltageClass": "",
#     "ConnectionCode": "",
#     "RatedCurrentLower": "",
#     "RatedCurrentUpper": "",
#     "DeprecationCodeList%5B0%5D": "37",
#     "DeprecationCodeList%5B1%5D": "40",
#     "DeprecationCodeList%5B2%5D": "39",
#     "DeprecationCodeList%5B3%5D": "38",
#     "DivisionCodeList%5B0%5D": "70",
#     "TypeNameLabel": "Model number",
#     "__RequestVerificationToken": ""
# }
# category = "66666666666666"
# custom_map = {"category": category}
# create_api(plan_id="46eb191842abc3bfb676b2ec8af4e90e", path=path,post_media_type="FORM",
#            custom_map=custom_map,http_request="POST",request_body=data)