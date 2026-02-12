import json
import os
from util.create_darwin_api import create_api
from urllib.parse import urlsplit, urlunsplit,quote

def encode_non_ascii_in_url(url):
    # 拆分URL为：协议(scheme)、域名(netloc)、路径(path)、参数(query)、锚点(fragment)
    parts = urlsplit(url)
    # 仅对路径部分编码：保留/（safe='/')，用UTF-8编码非ASCII字符
    encoded_path = quote(parts.path, safe='/', encoding='utf-8')
    # 拼接回完整URL
    encoded_url = urlunsplit((
        parts.scheme,
        parts.netloc,
        encoded_path,
        parts.query,
        parts.fragment
    ))
    return encoded_url


base_path = "../seed_json"

file_path = os.path.join(base_path, "chipanalog.json")
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        original_url = item["url"]
        encoded_url = encode_non_ascii_in_url(original_url)
        print(encoded_url)
        path = encoded_url
        category = item["category"]
        custom_map = {"category": category}
        create_api(plan_id="f91ea93536d8495bc81c056d2cdb48a4", path=path, custom_map=custom_map)