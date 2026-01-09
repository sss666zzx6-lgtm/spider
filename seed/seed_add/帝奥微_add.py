import json
import os
from util.create_darwin_api import create_api

base_path = "../seed_json"

file_path = os.path.join(base_path, "dioo.json")
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        path = "https://www.dioo.com/api/web/productList"
        pid = int(item["url"])
        data = {
            "pageNo": 1,
            "pageSize": 10000,
            "keyword": "",
            "names": "",
            "pid": pid
        }

        category = item["category"]
        custom_map = {"category":category}
        create_api(plan_id="8476f93db1a91b3d6dddfa9968156ac4",path=path,custom_map=custom_map,
                   http_request="POST",request_body=data)


#
# path = "https://www.dioo.com/api/web/productList"
# category = "666"
# custom_map = {"category":category}
# create_api(plan_id="8476f93db1a91b3d6dddfa9968156ac4",path=path,
#            custom_map=custom_map,http_request="POST",request_body = data)