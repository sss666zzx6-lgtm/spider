import json
import os
from util.create_darwin_api import create_api

# base_path = "../seed_json"
# #
# file_path = os.path.join(base_path, "kinet.json")
# with open(file_path, "r", encoding="utf-8") as f:
#     seed_data = json.load(f)
#     for item in seed_data:
#         path = item["url"] + "#tab-id-1"
#         category = item["category"]
#         custom_map = {"category": category}
#         create_api(plan_id="c712723e38f2ab87dad78832958df6ae", path=path, custom_map=custom_map)


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "Sec-Ch-Device-Memory": "8",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
    "Cookie": "ASP.NET_SessionId=0ng4inmbow10xeoqanqdpasa; PIM-SESSION-ID=vxBRGlmmjk99rgir; preferences=ps=www&pl=en-US&pc_www=USDu",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}

path = "https://www.mouser.com/ProductDetail/Kinetic-Technologies/KTS1865CEIAA-TA?qs=ZcfC38r4PovBHhe59sPlNw%3D%3D"

custom_map = {"category": "5555"}
create_api(plan_id="c712723e38f2ab87dad78832958df6ae", path=path, custom_map=custom_map,headers=headers)