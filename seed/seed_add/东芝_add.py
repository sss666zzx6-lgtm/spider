import json
import os
from util.create_darwin_api import create_api
from urllib.parse import urlparse, parse_qs

base_path = "../seed_json"


def extract_code_param(url):
    """
    从URL中提取query参数里code对应的值（如从/parametric?code=param_208&...提取param_208）
    :param url: 目标URL（相对路径/完整URL均可）
    :return: code参数值（无则返回空字符串）
    """
    # 解析URL，分离出查询参数部分（?后的内容）
    parsed_url = urlparse(url)
    # 解析查询参数为字典（key: [value1, value2]，兼容多值参数）
    query_params = parse_qs(parsed_url.query)
    # 提取code参数值：取列表第一个元素，无code则返回空字符串
    code_value = query_params.get('code', [''])[0].strip()
    return code_value

file_path = os.path.join(base_path, "toshiba.json")
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        base_url = "https://toshiba.semicon-storage.com/parametric/rest/getRowData?region=apc&lang=en&code="
        code = extract_code_param(item["url"])
        # print(code)
        path = base_url + code
        category = item["category"]
        custom_map = {"category": category}
        create_api(plan_id="fb9119c64487d78e58b8f8559c6b47fa", path=path, custom_map=custom_map)