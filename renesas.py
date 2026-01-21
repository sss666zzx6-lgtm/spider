import requests
from curl_cffi import requests
import re
#
# payload  = {
#     "requests": [
#         {
#             "indexName": "prod_main_en",
#             "params": "facetingAfterDistinct=true&facets=%5B%22fDocType.lvl0%22%2C%22fFeatured%22%5D&filters=type%3A'Document'%20AND%20(nid%3A25570833%20OR%20nid%3A25577814)%20AND%20NOT%20staging%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=15&maxValuesPerFacet=100&page=0&query="
#         }
#
#     ]
# }
#
# headers = {
#     "x-algolia-application-id": "KJ220GAQ35",
#     "x-algolia-api-key": "YjFlY2I5NTUxM2ZlN2RkMmRmNmRhNjM2MDA1ZmNmMTRmODE0NTA5N2ViNmM1YTEwNjg2NjE0MzcxNzc3NzgyY2ZpbHRlcnM9cHVibGljbHlMaXN0ZWQlM0F0cnVlK09SK2RvY0FjY2VzcyUzQWxvY2stYW5vbnltb3VzK09SK2RvY0FjY2VzcyUzQW5vLWxvY2srT1IrTk9UK2J1bmRsZSUzQWRvY3VtZW50"
# }
#
# # 发送POST请求
# url = "https://kj220gaq35-1.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.22.1)%3B%20Browser%3B%20instantsearch.js%20(4.80.0)%3B%20JS%20Helper%20(3.26.0)"
# response = requests.post(url, headers=headers, json=payload)
#
# # 打印响应结果
# print(response.json())

session = requests.Session()

data = {
    "username":"jasonlee@hhsmdl.freeqiye.com",
    "password":"Hhsmdl123456&",
    "form_build_id":"form-WWL8IdWrldeY9hGG0oOvNvwR3vH4OdyFbVqnc7PisxI",
    "form_id":"idt_okta_login_form",
    "captcha_sid":"53901963",
    "captcha_token":"92UYVA_Z816Rod2uuakx9mbyV5cHQJYC16iP1bATSyI",
    "captcha_response":"Turnstile no captcha",
    "cf-turnstile-response":"0.1N7BIzYj7U91i80gDmM7ydZoX9VSgFpHu-NvaEc8i4tLJNUu7p5X6Z2o-JpzxPeECFRqILCHL3MPlTTa4z-uRTvVzJVM2sa_-Qqw9m69_-8nE8-wq1qj9HitK3JsZKkJlOMKSN4Tkk9WSMxAQoT8UP1sVEbiONbNEok7eRnR2R9lHBRdgpkRb_c55mux0FFn_nTlCabF3M2X6akvCvGOXXDOsPKewt7FFthbadveJ-AyzcChxEL-zwfjKn8Ylx6yFMY3GAZNch4UGUnIUHsPeTM2AvQ5Fwgowqtiiyof3L36kfZ4vSEcdhMmDvG6dE9Zbg9Nc_Yi3DsQ4agHipzfw3Ry5aEU63ZhsYqjGayTj5I3tg01aVpuUJ_4NtRqcDPkpLwquHsjnHPmgjdYgfa5jdJFlmM1oOnmvo7_XKdXQk0KtR8X0vNzFTT-hzD7Vz7D7vhcwg3mhExKcRM9yaX6u9-Esp7v53fwH43tlFuIEEemdvNcxO09G2HE5oGtIWmdKu3-Q0apxg-XK0JJbsQpudgPafqs65svkF1UaP2-b8dibFb13kEWI-7g4ABTBbFvwKs8QeKb6BNrA31AMu64ExjMGnSslEcpkVnE2M_Jqv9nXsJM3nsiqb8ibnAA9-mRJEYI12uNQ4TcIoG0P__CUaMbFLfjqtJ08Wq5a9-t5PamlV9WC0qL_Fm-EFfpogiuSoyplrQKQf0jBSVg5v-gNXhiC5PyVQALUEJdU6ymD0ANovWZm814GT7BNFqvZU3U8VXzBnm376DetCuR-JeEdfJUnZu0NFgnXUxA3SlWQJA1QDe2Yp8zJFmoQN-tGaKWqWhyV4xKt70hZvXle2DAd3qjFESE-oFlblCHdE2xwpG0sCJM87qq6qBJoWflZ2c1xyW7Z-26AIMX3nXMy2gX9JeIzRWZsj9GDG8_-P0ZlYo.k4Sue5hEBAfyes1Gra1ZQg.a1f24dc70cd64279bb39cea70d73dc11ed7c014ab599cf7dbe310e5f1db27b88",
    "captcha_cacheable":"1",
    "op":"登录"
}

url = "https://www.renesas.cn/zh/oauth2/default/v1/authorize?client_id=0oa2ixjskq8o2hdJB357&response_type=code&scope=openid%20email%20phone%20profile%20MyRenesasUserInfo&redirect_uri=https%3A//www.renesas.cn/openid-connect/renesas_okta&state=u8bgwH9v_s6BizFSbxRviK5wWR9ej7O3M8HbucKztek"

response = session.post(url,data=data,headers={
    "Content-Type":"application/x-www-form-urlencoded",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
})
print(response.text)
print(response)
print(response.cookies)
print(session.cookies)


# res = requests.get("https://www.renesas.com/en/products/analog-products/audio-video/wireless-audio/product-selector")
# print(res.text)
# print(res)


headers = {
    # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    # "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    # "cache-control": "no-cache",
    # "pragma": "no-cache",
    # "priority": "u=0, i",
    # "referer": "https://darwin.lumychip.com/",
    # "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
    # "sec-ch-ua-mobile": "?0",
    # "sec-ch-ua-platform": "\"Windows\"",
    # "sec-fetch-dest": "document",
    # "sec-fetch-mode": "navigate",
    # "sec-fetch-site": "same-origin",
    # "sec-fetch-user": "?1",
    # "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}
#
# url = "https://www.renesas.com/en/products/analog-products/audio-video/wireless-audio/product-selector"
# response = requests.get(url, headers=headers)
#
# print(response.text)
# print(response)





