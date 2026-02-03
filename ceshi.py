import requests
import json
from curl_cffi import requests


headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "cache-control": "no-cache",
    "content-type": "application/json; charset=UTF-8",
    "origin": "https://www.skyworksinc.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.skyworksinc.com/Products/Audio-and-Radio/Si4790x-Automotive-Tuners",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-bitness": "\"64\"",
    "sec-ch-ua-full-version-list": "\"Not(A:Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"144.0.7559.110\", \"Google Chrome\";v=\"144.0.7559.110\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-platform-version": "\"19.0.0\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

url = "https://www.skyworksinc.com//api/feature/search/getsilabsproductspecification/"
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
    "ItemID": "{60CB0D8C-576B-47C3-8EAB-7794720F5BA0}"
}
# data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, json=data)

print(response.text)
print(response)