import requests

# res = requests.get("https://www.ti.com/selectionmodel/api/gpn/result-list?destinationId=12473&destinationType=GPT&mode=parametric&locale=en-US")
# print(res.json())
url = "https://www.ti.com/product/CSD17556Q5B"
response = requests.get(url)

print(response.text)
print(response)
#
#
# {automotive
# :
# true
# catalog
# :
# false
# highTemp
# :
# false
# hirel
# :
# false
# military
# :
# false
# space
# :
# false}

import requests
import json

# 请求URL
# url = "https://www.monolithicpower.com/_fs-ch-1T1wmsGaOgGaSxcX/fst-post-back"
# https://www.monolithicpower.com/_fs-ch-1T1wmsGaOgGaSxcX/fst-post-back

# # 请求载荷
# payload = {
#     "token": "AbgMmh3uAMYXQMqUyO_eZ5eGZ4DPj6wWFBsCrIPxeLqm2Qqs3IpE14N5j7jytcPnf242UxjVWfo9x3SkEum3-WQ9C2GlZqPXLPv7chQiRm-IcMhSm3kdCnJ5nRBRTkEL_Y6-lRyPlAxChiBjWnQE37GRRqR5cYUl_3RawtdEFC_SpxqSyU9B3855zyJg9dHqt6BndCvvmi3Jj9sSHP6n3T87rD2qp0CBSikS-hsOsWXxZhXIVnsPXQbhMbE9jIA--xwxEnVL9h61heYVftoKynipzC1gcPXYHLVEZcqUacX7el7JrtFBa1JDf992lAF5tR8FgoPYKSRnI8dCLvDDUCPEogKqad_ImB_nGSGPrQNls2YTTcNdQT1JCgZK5WBaVXXDal96MNkQAadisgI-1IFcQXupWgYLATFg8A8NX_Jpqn5L",
#     "data": [
#         {
#             "ty": "pow",
#             "base": "gYvAZCT5WijdsOQp",
#             "answer": "tl",
#             "hmac": "e6c33bb5197ccf9718e2c6807557de91b49ca9f15dd79c2ac9a5783a1937cc55",
#             "expires": "1766744021"
#         }
#     ]
# }
#
# # 设置请求头
# headers = {
#     "Content-Type": "application/json",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#     "Referer": "https://www.monolithicpower.com/"
# }
#
# try:
#     # 发送POST请求
#     response = requests.post(url, json=payload)
#
#     # 打印响应状态
#     print(f"状态码: {response.status_code}")
#
#     # 检查响应
#     if response.status_code == 200:
#         # 获取所有响应头
#         print("所有响应头:")
#         for header, value in response.headers.items():
#             print(f"{header}: {value}")
#
#         # 特别获取Set-Cookie
#         if 'Set-Cookie' in response.headers:
#             print("\nSet-Cookie 值:")
#             set_cookie = response.headers['Set-Cookie']
#             print(set_cookie)
#
#             # 解析特定的cookie
#             # 查找 _fs_ch_cp_79UUvfpJ5mWYtLQv 这个cookie
#             cookie_name = "_fs_ch_cp_79UUvfpJ5mWYtLQv"
#             if cookie_name in set_cookie:
#                 # 提取cookie值
#                 cookie_start = set_cookie.find(cookie_name) + len(cookie_name) + 1
#                 cookie_end = set_cookie.find(";", cookie_start)
#                 cookie_value = set_cookie[cookie_start:cookie_end]
#                 print(f"\n提取的 {cookie_name}: {cookie_value}")
#             else:
#                 print(f"\n未找到 {cookie_name} 在Set-Cookie中")
#
#         # 使用requests的cookies属性获取
#         print("\n所有Cookies:")
#         for cookie in response.cookies:
#             print(f"{cookie.name}: {cookie.value}")
#
#             if cookie.name == "_fs_ch_cp_79UUvfpJ5mWYtLQv":
#                 print(f"\n通过response.cookies获取的cookie值: {cookie.value}")
#
#         # 打印响应内容
#         print(f"\n响应内容: {response.text}")
#
#     else:
#         print(f"请求失败，状态码: {response.status_code}")
#
# except requests.exceptions.RequestException as e:
#     print(f"请求发生错误: {e}")
# except Exception as e:
#     print(f"发生未知错误: {e}")


