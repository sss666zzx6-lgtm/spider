import json
import os
from bs4 import BeautifulSoup
from curl_cffi import requests

from util.create_darwin_api import create_api
from urllib.parse import quote
from urllib.parse import urlparse, parse_qs

headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "Cache-Control": "no-cache",
    "Content-Type": "application/json; charset=UTF-8",
    "Origin": "https://www.skyworksinc.com",
    "Pragma": "no-cache",
    "Priority": "u=1, i",
    "Referer": "https://www.skyworksinc.com/Product-Specification?family=Power%20Management&categories=Display%20and%20Lighting;LED%20Camera%20Flash%20Drivers;Charge%20Pump%E2%84%A2%20Camera%20LED%20Flash%20Drivers%20;Serial%20Boost%20Camera%20LED%20Flash%20Drivers%20;Mid%20to%20Large%20Screen%20LCD%20LED%20Backlight%20with%20PMW%20Interface;RGB%20LED%20Driver;White%20LED%20Drivers;Charge%20Pump%20Based%20White%20LED%20Backlight%20Drivers%20;Serial%20Boost%20White%20LED%20Backlight%20Drivers",
    "Sec-Ch-Ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
    "Sec-Ch-Ua-Arch": "\"x86\"",
    "Sec-Ch-Ua-Bitness": "\"64\"",
    "Sec-Ch-Ua-Full-version-list": "\"Not(A:Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"144.0.7559.110\", \"Google Chrome\";v=\"144.0.7559.110\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Model": "\"\"",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Ch-Ua-Platform-version": "\"19.0.0\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "X-Requested-with": "XMLHttpRequest"
}
def get_skyworks_params(url):
    # 关键修复：将HTML转义的&amp;替换为原生&，保证参数解析正确
    url = url.replace("&amp;", "&")
    # 解析URL查询参数
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    # 提取参数（不存在则返回空字符串）
    family = params.get("family", [""])[0].strip()
    categories = params.get("categories", [""])[0].strip()

    return {
        "family": family,
        "categories": categories
    }
base_path = "../seed_json"



file_path = os.path.join(base_path, "skyworksinc.json")
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        data = {
            "SearchText": None,
            "MarketList": None,
            "SolutionList": None,
            "ApplicationList": None,
            "CategoryList": [],
            "FamilyList": [],
            "DocumentTypeList": None,
            "IsParameterSearch": False,
            "FrequecyMinGhz": 0,
            "FrequecyMaxGhz": 0,
        }
        final_url = ""
        if "family" in item["url"]:
            result = get_skyworks_params(item["url"])
            FamilyList = [cat for cat in result["family"].split(';') if cat]
            CategoryList = [cat for cat in result["categories"].split(';') if cat]
            data["FamilyList"] = FamilyList
            data["CategoryList"] = CategoryList
            print(FamilyList, CategoryList)
            final_url = "https://www.skyworksinc.com//api/feature/search/getspecification/"
        else:
            try:
                print(item["url"])
                result = get_skyworks_params(item["url"])
                response = requests.get(item["url"], timeout=10)
                print(response)
                soup = BeautifulSoup(response.text, "lxml")

                pageitemid_input = soup.find("input", id="pageitemid")
                pageitemid_value = pageitemid_input.get("value", "") if pageitemid_input else ""
                print(f"当前页面pageitemid：{pageitemid_value}")
                data["ItemID"] = pageitemid_value
                final_url = "https://www.skyworksinc.com//api/feature/search/getsilabsproductspecification/"

            except Exception as e:
                print(f"异常：{e}")

        path = final_url
        # print(path)
        category = item["category"]
        print(category)
        custom_map = {"category": category}
        create_api(plan_id="7ff86c874ab78f2862014bb7c4b863d2", path=path, custom_map=custom_map,
                        http_request = "POST",request_body = data,headers=headers,fetch_method=2)


# data = {
#     "SearchText": None,
#     "MarketList": None,
#     "SolutionList": None,
#     "ApplicationList": None,
#     "CategoryList": [],
#     "FamilyList": [],
#     "DocumentTypeList": None,
#     "IsParameterSearch": False,
#     "FrequecyMinGhz": 0,
#     "FrequecyMaxGhz": 0,
#     "ItemID": "{C61676A9-442F-4A69-A3DB-2BB34CD71129}"
# }
# path = "https://www.skyworksinc.com//api/feature/search/getsilabsproductspecification/"
# # print(path)
# category = "Clocks and Timing^Clock Buffers^PCIe Clock Buffers"
# custom_map = {"category": category}
# create_api(plan_id="7ff86c874ab78f2862014bb7c4b863d2", path=path, custom_map=custom_map
#            ,http_request = "POST",request_body = data,headers=headers)

# create_api(plan_id="7ff86c874ab78f2862014bb7c4b863d2", path=path, custom_map=custom_map
#            ,headers=headers)