import json
import os
from util.create_darwin_api import create_api
from urllib.parse import urlparse,parse_qs


def extract_ptype_and_params(url: str) -> dict:

    result = {
        "ptype": "",
        "other_params": {}
    }

    # 1. 解析URL，提取查询字符串部分
    parsed_url = urlparse(url)
    query_str = parsed_url.query
    if not query_str:
        return result

    # 2. 解析查询参数（自动解码URL编码，如%20→空格、%26→&）
    query_params = parse_qs(query_str, keep_blank_values=True)

    # 3. 提取ptype参数（取第一个值，兼容多值场景）
    if "ptype" in query_params:
        result["ptype"] = query_params["ptype"][0] if query_params["ptype"] else ""

    # 4. 提取其他参数（排除ptype，取每个参数的第一个值）
    for key, values in query_params.items():
        if key != "ptype" and values:
            result["other_params"][key] = values[0]

    return result

base_path = "../seed_json"

file_path = os.path.join(base_path, "cellwise.json")
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        url = item["url"]
        params = extract_ptype_and_params(url)
        ptype = params["ptype"]
        other_params = params["other_params"]
        data = {"filter":{}}
        if other_params:
            key = next(iter(other_params.keys()))
            value = other_params[key]
            if key:
                data = {
                    "filter": {key: [value]},
                }
        # print(json.dumps(data, indent=4, ensure_ascii=False))

        category = item["category"]
        custom_map = {
            "category": category,
            "ptype": ptype,
        }
        path = f"http://en.cellwise-semi.com/Api/Index/get{ptype}List"
        if ptype == "usb_ic":
            path = f"http://en.cellwise-semi.com/Api/Index/getusb_controlList"

        if ptype == "buck":
            path = f"http://en.cellwise-semi.com/Api/Index/getbuck_converterList"

        create_api(plan_id="91ae1a6f573696104500dfc3d3d885ed", path=path, custom_map=custom_map
                   ,http_request = "POST",request_body = data,)




# url = "http://en.cellwise-semi.com/Api/Index/getProductDetail"
# data = {
#     "filter": {
#         "ptype": "usb_ic",
#         "id": "3"
#     }
# }
#
# path = url
# category = "666666"
# custom_map = {"category": category}
# create_api(plan_id="91ae1a6f573696104500dfc3d3d885ed", path=path, custom_map=custom_map
#            ,http_request = "POST",request_body = data,)