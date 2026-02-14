import os
import time
import requests
from curl_cffi import requests


headers = {
    # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    # "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    # "cache-control": "no-cache",
    # "pragma": "no-cache",
    # "priority": "u=0, i",
    # "referer": "https://www.renesas.cn/zh/search?keywords=RBC220A75F3JWS%20",
    # "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
    # "sec-ch-ua-mobile": "?0",
    # "sec-ch-ua-platform": "\"Windows\"",
    # "sec-ch-ua-platform-version": "\"19.0.0\"",
    # "sec-fetch-dest": "document",
    # "sec-fetch-mode": "navigate",
    # "sec-fetch-site": "same-origin",
    # "sec-fetch-user": "?1",
    # "upgrade-insecure-requests": "1",
    "cookie" : """kapa_ab_group=control; nmstat=16dce3a3-2c23-15d2-1e61-a1736d3b5475; ELOQUA=GUID=D5880C96D8114262829A97FB0D0A1FD9; ren_usr_pr=0; notice_preferences=2:; notice_gdpr_prefs=0,1,2:; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3; _ga=GA1.1.252753382.1765965542; IDT-Language=zh; MkHcLang=zh-CN; MkHcCurrencyId=USD; notice_behavior=expressed,eu; _ALGOLIA=anonymous-3755666a-0b13-482f-bee3-4cef80c7daa9; Hm_lvt_b99db6af50ce7be250cabdfa36f447da=1768273379,1768464776,1768541212,1770721347; HMACCOUNT=045E38B63DFCF0FA; _clck=6prpxc%5E2%5Eg3h%5E0%5E2206; ELQCOUNTRY=CN; _ga_5JDBBP5TWD=GS2.1.s1770782282$o1$g0$t1770782282$j60$l0$h0; currentpath=/zh/support/document-search; TAsessionID=26ebf285-c4f6-4d81-a85c-652c04bcc592|EXISTING; _gcl_au=1.1.299705081.1765965542.427803347.1770788128.1770788127; myr=102-jzEmU6KS1Su-yw8-ovthw; sid=102-jzEmU6KS1Su-yw8-ovthw; xids=1021VJyYq3NQ0iwz8Qh700dPw; JSESSIONID=9F504AC50571D676D2CAE9D93EC72EDF; idx=eyJ6aXAiOiJERUYiLCJ2ZXIiOiIxIiwiYWxpYXMiOiJlbmNyeXB0aW9ua2V5Iiwib2lkIjoiMDBvMWNneDRvNHlBYXBZMmgzNTciLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiZGlyIiwieHNpZCI6ImlkeG4wcUgxcXFCVHFHdlNuMXB1anI4Y3cifQ..3hGujvolnYGimcd0.YjtQD3Ql3EDFZVAhufXurC3l9s4UtIQIqffvU1MF8E3QvEmQJPgi4Y09xAMuFPOZN09-3GPrpjmiek9DnrM9C9ixWgU_PQSJeRnIfKbhQmKYe1hZF9VXjCWn5PLvt7M_vv2njSiXzE-xxIQCXaMmAKArJiIgkMHvSLA7uvZc8r4dC3cLLfZiNDnw4_5BjYVU0DCsjIofUsaZU2B4mUjk-Pf1H6Z3dNWgZmDlIAL4pjcbWTS3UGHii4xLPjYeL1qDce_sLIi6uOzYhmrYG7BSx95ZdYvRV6UHYBnHKwqLMNpM1-NUA9NqbYHZcxv9VU7hbufkbRB59-rBh31eyfOqVpKCC_zlAdiW3CvEZM_0jGsqWXz1zSEj7fDi8Ya3SpqwEPV2AtBWcIYf-UgNEiO0yB6xq64qFeN89YoKZXv1EbzsQ-PvMRubues_GgYOz8cyRGk5eyMIzRx_MN-wai2FNRhW0Cmj40MZ4tI8XNglNQR8bWtX7wdvqeKJVRJoUZceiQM6Rx5Mzageyl4CnYaRth6Q0gNXkgtBhsdPNdje3vXTo5sY1uRaRl7SLtpNMD7CQR5mFQF8Zw0g9bDv4o-eTgZopAVlxE2RFF0YyO1hxLQN7x4GmXpGXl2f50GuwZFxtuoToVpV-XMxgVSkNG__cxX40aLd9giHoxfrfz2Y0K0xUiXDFisMIeysSfxesRct_SupjV1ORvsWHVU4HiSCxJUwkWXP2cxlu-ZlgGIPjWuG33ClNTMKJKdjIpjn-NeSZNSw9OlxOWLvZb6anWQH4QQzuU2ZWvt5xkztbz-EYGddHpp6KiiPvMzfXr3tVcBj_nL2Is_ajBT0dIDGmWisoxQPa6A98y3A2Krm1DP8UWWz86M3qQ7AQLzJWpd_2_HFP2KZoU-gV6_7PkiGmw595slwFwJLYGqVr1uzpDHkwvbbnA.pW91hHCtXClXXixCRdc-Lg; DT=DI1pIJ833EcQO22y7M2l60c4Q; proximity_400d32b72c8ba6f4d4a8984df2612eb0=eyJ6aXAiOiJERUYiLCJwMnMiOiJObk9OdzU4Q0lHR29WbGQ1WUV0ZmxRIiwicDJjIjoxMDAwLCJ2ZXIiOiIxIiwiZW5jIjoiQTI1NkdDTSIsImFsZyI6IlBCRVMyLUhTNTEyK0EyNTZLVyJ9._i0U8IRV39xF0cgP1W53TVNo1BemYQPPAJ1zIBWOrM9QRZxgX6OLxw.78ruqytMMty4uZmU.p33nIq_0TjicUwicbqhtJrusaE_WsxPlOEzThV4XFUuME-Ff29tffU9X3mDD4uF2tMnKjx71J4TaRDn7mPw0-j5pDJeeFOzFxzKaq2o7dx55bYHeFG77LvbzY81OY1dRQCF0RX52D3k-3yay8hECiRThorx6SJTpDdR69XaP57WURw.kfL6gIWiP-JqkqV7LU4nMQ; SSESSf924456a8134245645d3d9c6c79ad01a=snqbcae2onqpdqqbp5sg7nko27; uid=6930727; ldoc=25547336-en; referrer_path=/products/rbc220a75f3jws; Hm_lpvt_b99db6af50ce7be250cabdfa36f447da=1770788622; _uetsid=fcb290d0066f11f1924a456922007945; _uetvid=5b154240db2f11f09bdabd14e06f1c08; _clsk=da0mjv%5E1770788623386%5E18%5E1%5Ez.clarity.ms%2Fcollect; _ga_D1706WVDQV=GS2.1.s1770787935$o63$g1$t1770788639$j60$l0$h0; __cf_bm=YBEGf5qYeSnOtT3akfRLitUzR6lX_XDt6G3KWoHzHAk-1770788880-1.0.1.1-PlmohbnmHlhwd_cPq6dTf3wG5P2V7ARA09yTIK4WXbSJSMN73uT77s.cGzQkPPTlHL6sD.nTpqJ1GApMrZC..VoDMpa8E_u3LDcLXQ9zJzY""",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
}
cookies = {
    "kapa_ab_group": "control",
    "nmstat": "16dce3a3-2c23-15d2-1e61-a1736d3b5475",
    "ELOQUA": "GUID=D5880C96D8114262829A97FB0D0A1FD9",
    "ren_usr_pr": "0",
    "notice_preferences": "2:",
    "notice_gdpr_prefs": "0,1,2:",
    "cmapi_gtm_bl": "",
    "cmapi_cookie_privacy": "permit 1,2,3",
    "_ga": "GA1.1.252753382.1765965542",
    "IDT-Language": "zh",
    "MkHcLang": "zh-CN",
    "MkHcCurrencyId": "USD",
    "notice_behavior": "expressed,eu",
    "_ALGOLIA": "anonymous-3755666a-0b13-482f-bee3-4cef80c7daa9",
    "Hm_lvt_b99db6af50ce7be250cabdfa36f447da": "1768273379,1768464776,1768541212,1770721347",
    "HMACCOUNT": "045E38B63DFCF0FA",
    "_clck": "6prpxc%5E2%5Eg3h%5E0%5E2206",
    "ELQCOUNTRY": "CN",
    "_ga_5JDBBP5TWD": "GS2.1.s1770782282$o1$g0$t1770782282$j60$l0$h0",
    "currentpath": "/zh/support/document-search",
    "TAsessionID": "26ebf285-c4f6-4d81-a85c-652c04bcc592|EXISTING",
    "_gcl_au": "1.1.299705081.1765965542.427803347.1770788128.1770788127",
    "myr": "102-jzEmU6KS1Su-yw8-ovthw",
    "sid": "102-jzEmU6KS1Su-yw8-ovthw",
    "xids": "1021VJyYq3NQ0iwz8Qh700dPw",
    "JSESSIONID": "9F504AC50571D676D2CAE9D93EC72EDF",
    "idx": "eyJ6aXAiOiJERUYiLCJ2ZXIiOiIxIiwiYWxpYXMiOiJlbmNyeXB0aW9ua2V5Iiwib2lkIjoiMDBvMWNneDRvNHlBYXBZMmgzNTciLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiZGlyIiwieHNpZCI6ImlkeG4wcUgxcXFCVHFHdlNuMXB1anI4Y3cifQ..3hGujvolnYGimcd0.YjtQD3Ql3EDFZVAhufXurC3l9s4UtIQIqffvU1MF8E3QvEmQJPgi4Y09xAMuFPOZN09-3GPrpjmiek9DnrM9C9ixWgU_PQSJeRnIfKbhQmKYe1hZF9VXjCWn5PLvt7M_vv2njSiXzE-xxIQCXaMmAKArJiIgkMHvSLA7uvZc8r4dC3cLLfZiNDnw4_5BjYVU0DCsjIofUsaZU2B4mUjk-Pf1H6Z3dNWgZmDlIAL4pjcbWTS3UGHii4xLPjYeL1qDce_sLIi6uOzYhmrYG7BSx95ZdYvRV6UHYBnHKwqLMNpM1-NUA9NqbYHZcxv9VU7hbufkbRB59-rBh31eyfOqVpKCC_zlAdiW3CvEZM_0jGsqWXz1zSEj7fDi8Ya3SpqwEPV2AtBWcIYf-UgNEiO0yB6xq64qFeN89YoKZXv1EbzsQ-PvMRubues_GgYOz8cyRGk5eyMIzRx_MN-wai2FNRhW0Cmj40MZ4tI8XNglNQR8bWtX7wdvqeKJVRJoUZceiQM6Rx5Mzageyl4CnYaRth6Q0gNXkgtBhsdPNdje3vXTo5sY1uRaRl7SLtpNMD7CQR5mFQF8Zw0g9bDv4o-eTgZopAVlxE2RFF0YyO1hxLQN7x4GmXpGXl2f50GuwZFxtuoToVpV-XMxgVSkNG__cxX40aLd9giHoxfrfz2Y0K0xUiXDFisMIeysSfxesRct_SupjV1ORvsWHVU4HiSCxJUwkWXP2cxlu-ZlgGIPjWuG33ClNTMKJKdjIpjn-NeSZNSw9OlxOWLvZb6anWQH4QQzuU2ZWvt5xkztbz-EYGddHpp6KiiPvMzfXr3tVcBj_nL2Is_ajBT0dIDGmWisoxQPa6A98y3A2Krm1DP8UWWz86M3qQ7AQLzJWpd_2_HFP2KZoU-gV6_7PkiGmw595slwFwJLYGqVr1uzpDHkwvbbnA.pW91hHCtXClXXixCRdc-Lg",
    "DT": "DI1pIJ833EcQO22y7M2l60c4Q",
    "proximity_400d32b72c8ba6f4d4a8984df2612eb0": "eyJ6aXAiOiJERUYiLCJwMnMiOiJObk9OdzU4Q0lHR29WbGQ1WUV0ZmxRIiwicDJjIjoxMDAwLCJ2ZXIiOiIxIiwiZW5jIjoiQTI1NkdDTSIsImFsZyI6IlBCRVMyLUhTNTEyK0EyNTZLVyJ9._i0U8IRV39xF0cgP1W53TVNo1BemYQPPAJ1zIBWOrM9QRZxgX6OLxw.78ruqytMMty4uZmU.p33nIq_0TjicUwicbqhtJrusaE_WsxPlOEzThV4XFUuME-Ff29tffU9X3mDD4uF2tMnKjx71J4TaRDn7mPw0-j5pDJeeFOzFxzKaq2o7dx55bYHeFG77LvbzY81OY1dRQCF0RX52D3k-3yay8hECiRThorx6SJTpDdR69XaP57WURw.kfL6gIWiP-JqkqV7LU4nMQ",
    "SSESSf924456a8134245645d3d9c6c79ad01a": "snqbcae2onqpdqqbp5sg7nko27",
    "uid": "6930727",
    "ldoc": "25547336-en",
    "referrer_path": "/products/rbc220a75f3jws",
    "Hm_lpvt_b99db6af50ce7be250cabdfa36f447da": "1770788622",
    "_uetsid": "fcb290d0066f11f1924a456922007945",
    "_uetvid": "5b154240db2f11f09bdabd14e06f1c08",
    "_clsk": "da0mjv%5E1770788623386%5E18%5E1%5Ez.clarity.ms%2Fcollect",
    "_ga_D1706WVDQV": "GS2.1.s1770787935$o63$g1$t1770788639$j60$l0$h0",
    "__cf_bm": "YBEGf5qYeSnOtT3akfRLitUzR6lX_XDt6G3KWoHzHAk-1770788880-1.0.1.1-PlmohbnmHlhwd_cPq6dTf3wG5P2V7ARA09yTIK4WXbSJSMN73uT77s.cGzQkPPTlHL6sD.nTpqJ1GApMrZC..VoDMpa8E_u3LDcLXQ9zJzY"
}
url = "https://www.renesas.cn/zh/products/rbc220a75f3jws"
params = {
    "queryID": "c90f114073f188f73662c89b3bac89c8",
    "tab": "documentation"
}

session = requests.Session()

# for key, value in cookies.items():
#     session.cookies.set(key, value)


response = session.get(url, headers=headers, params=params)
print(f"响应文本：{response.text}")
print("\n===== 服务器返回的Cookie =====")
print(response.cookies)
print(session.cookies)


print(f"\n响应状态码：{response.status_code}")
# https://www.renesas.cn/zh/document/dst/rbn300n75a5jws-datasheet
# pdf_url = "https://www.renesas.cn/zh/document/dst/rbc220a75f3jws-datasheet"
# pdf_url = "https://www.renesas.cn/zh/document/dst/rju1c16jws-datasheet"
pdf_url = "https://www.renesas.cn/zh/document/dst/cl8060-datasheet"
# cl8060
save_path = "cl8060_datasheet.pdf"
time.sleep(1)
try:
    response = requests.get(
        pdf_url,
        headers=headers,
        # cookies=cookies,
        stream=True,
    )
    response.raise_for_status()
    print(response)

    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=32 * 1024):
            if chunk:
                f.write(chunk)

    if os.path.getsize(save_path) > 0:
        print(f"PDF下载成功，保存路径：{os.path.abspath(save_path)}")
    else:
        print("下载失败：文件为空")

except Exception as e:
    print(f"下载失败：{str(e)}")



# https://toshiba.semicon-storage.com/info/lookup.jsp?pid=TDTC144E&region=apc&lang=en
# https://toshiba.semicon-storage.com/info/lookup.jsp?pid=2SA1162&region=apc&lang=en

# https://toshiba.semicon-storage.com/info/lookup.jsp?pid=RN4987&region=apc&lang=en
# https://toshiba.semicon-storage.com/info/lookup.jsp?pid=TLX9150M&region=apc&lang=en
