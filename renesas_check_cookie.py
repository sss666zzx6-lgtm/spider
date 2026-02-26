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
    "cookie" : """nmstat=16dce3a3-2c23-15d2-1e61-a1736d3b5475; notice_preferences=2:; notice_gdpr_prefs=0,1,2:; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3; _ga=GA1.1.252753382.1765965542; IDT-Language=zh; MkHcLang=zh-CN; MkHcCurrencyId=USD; _ALGOLIA=anonymous-3755666a-0b13-482f-bee3-4cef80c7daa9; HMACCOUNT=045E38B63DFCF0FA; ELQCOUNTRY=CN; currentpath=/zh/support/document-search; notice_behavior=none; kapa_ab_group=control; Hm_lvt_b99db6af50ce7be250cabdfa36f447da=1770721347; proximity_400d32b72c8ba6f4d4a8984df2612eb0=eyJ6aXAiOiJERUYiLCJwMnMiOiJQX2xwdEJGRVd0SU4xbGdldFA3eDVRIiwicDJjIjoxMDAwLCJ2ZXIiOiIxIiwiZW5jIjoiQTI1NkdDTSIsImFsZyI6IlBCRVMyLUhTNTEyK0EyNTZLVyJ9.lLlAD9_LMf35o9mfoSRyKN65Y-A2uhdgSd5Kf5e61iWXQ2dOzSS9YQ.dl81EVp97uUctDo4.ksFjVCy0cVB_Zu7JgnCr6vQjGQwJ0aEfbbwb7tmNZdXxn7UYtw_0gOWImNwJUjHyMat0Fz4uHo1oeYMfWR4t6deBpDOzhqdJmqaNuMFGkWoAXRv7fksNmGBmXT7ROrD4hLeOwwuEvBXmIUDX3VIrCqFfgamggt51wVbYviJZAsoqmw.Z4RTNgy5IibtLQfjS8SGWA; _clck=6prpxc%5E2%5Eg3v%5E0%5E2206; _fbp=fb.1.1771997692697.919170848503001381; OPTIN=1; ELOQUA=GUID=D5880C96D8114262829A97FB0D0A1FD9&FPCVISITED=1; _ga_5JDBBP5TWD=GS2.1.s1771997687$o2$g1$t1771997780$j47$l0$h0; ldoc=1619801-en; __cf_bm=A9BMh0r4A85aGNHMMW3aGq2ej4AW_CDC5hXWn263m0o-1771998970-1.0.1.1-lipqzwnEnDMcdQ3dFQns5RLwQal5FFe5gKAabC5fmL9iY8pEKk2_vBiOSBKNmxKEeu13ZEhpX38kH5RdKHCi7zBVtVn3YjiHu5LuvznxByQ; cf_clearance=kT5gYSKpvqVTI6oLuSFMM1JHNLh.LOZ9NJ2zb0xJEo8-1771998972-1.2.1.1-nUeZeTUPz_D69Av0rEyALeVQUZV60e0Mp3xqYan6S0FTBQkm3P81KmSQLjdjGX74CFVyIUL764lF_U6mzUhwrh60nrDiGWCkaIWY49WSUuvr169uOj5i6Rv8JMTxGDZF47S5VC8iycB6O47POjYEtDyeewIDZZ6qu6Sq7MwpUa.qA2mXwHbo4dMjb71e0r9Y5iwyqQRaCaAgMe9b.8SE_rsE.WxTq0.O.DlINGRp6ZA; _gcl_au=1.1.299705081.1765965542.1089777303.1771997877.1771998993; myr=102nf3t7OSVS7mUDnQZ4gcrRg; sid=102nf3t7OSVS7mUDnQZ4gcrRg; xids=102dwXj6sbUSTaXy_QFvB6Fsg; JSESSIONID=53CF8A3C3EAF55F55E570F7E8E1FA38B; idx=eyJ6aXAiOiJERUYiLCJ2ZXIiOiIxIiwiYWxpYXMiOiJlbmNyeXB0aW9ua2V5Iiwib2lkIjoiMDBvMWNneDRvNHlBYXBZMmgzNTciLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiZGlyIiwieHNpZCI6ImlkeFhtSXNlVnlYUWdXR2xDeDVMZmwzaUEifQ..E9XQ1FQbuJwAklFU.FqBhEpCjMCddqFJklEmz23qxUlbEYdjYomfgZVBWY-vMc42oILpM5OLUgSTgd1RpyOaUbNQTZhNYwNM7Q-rH65JL5trRYmFJsiBuLtInUeyp5CQicjFMXuPsva3bV-EEjxUvQSEp-Cul6OMpqk6_P4Knm1jQ4t-tMssFMPOWe5aAYvzDtT2zcH-6suxhJUGOfQITn8kChiKeuAzZjTTCst4vASirsn-RZ4_HCWkVxxxTNJq_UYR9wMYYjKimfJ9uWqnppLQn6ZkNsAOW9dORCbQVJ_UnF7ONLoO_r5wC4Vb5c-QN2NVZWAOp1TwYdTTsXE3kvvQDp5jcpOfY1TCQpBmEjgQtbaoX_DqhEk6Ma8P791uYpkL8G7DACBqTflUePS5l32zMkJx0VXutfz0O3tOE0qXxJG2DFyEa3JHXB3WosRNLLNLLynKsjEBJAs1xDLFrUrvbmvF4xK2_FW_WyytXLXPj8DcZ-1DZp0sD82MYy_zXvyH1lcoaTPYqBT_Z_m3xMo3t6iZwkl0bFoqEy3feLb_-dymGj_-Id17ICvWpHlTjq3hoWgBEzoWpJ6Gigit3G24mEIkF7W0yuxWTYt-b1RWqfg20Lo2zmT3KD2_YvXmCIC8Fg6XS8KmuExgRRDoOFBhihf1Ev0um9fDlBF4qN2D4hJntJ04lPZLUTpPgPEybeMW6h-ZjTJOgioBIn2-G5IHKn8Yq1v9I8ZLjTWJgM4RcsfkSeoKdqy1liDXGuyV-FazwLNKt2_C2Lf8AmtnPYoByY9ht7C4licJH0Rp_KkzJHSyku1YTxzLtf7j-7J3-gijKq6-ReT44LJIc_fjMj91B-aP5UKAgb0RTm8rKL6aLRT-WZmlh8YiZVM-mJYsKpVnTkWLAaqt_wIe-vWk_SjdkxaQscAML3IQ2XHqrxyXc7Jj4Vw3cVfrR-FNIlQ8.6-uBhf2Y0sLjwyugirx_LA; DT=DI1Mh2qeNenQKWYGTZQG1kxKA; proximity_b7b50f02d73fdbb68d58d277864c3613=eyJ6aXAiOiJERUYiLCJwMnMiOiJncTNrMGEzdHhmMHJ5dEE2d3VGUy1RIiwicDJjIjoxMDAwLCJ2ZXIiOiIxIiwiZW5jIjoiQTI1NkdDTSIsImFsZyI6IlBCRVMyLUhTNTEyK0EyNTZLVyJ9.iPHDAeXP_v3Az6kgZxPmvZkVBmm_s2djM0SklBetc1V70urUFthxDg.XpjxxOmZzDpgu8J_.HG4eJt2OvlxQF-BVzD66h-mXDDJ0ZuSl9YrfBM6cwQ4JcDkJ0KNXJ0_20LBug7NlULH4SB26AzvWYg-Sc7XiTj-CA-KTNoGSvLEpwxWN2HX2zlmpi5m8YKKMP0Oxy3b581XXcj14W3BA990p8fGJeLHy6NjLt3TpfUNPQCw4rN3Ifw.pq5xxal0ibhewbRggvqyqg; SSESSf924456a8134245645d3d9c6c79ad01a=q2vdgr4g9jc4m2jvbgftb80erb; ren_usr_pr=0; uid=6942801; referrer_path=/products/cl8060; accessedDocumentsFetched=1; Hm_lpvt_b99db6af50ce7be250cabdfa36f447da=1771999005; _uetsid=4f7b1750116711f1944e458eceefe2cb; _uetvid=5b154240db2f11f09bdabd14e06f1c08; _ga_D1706WVDQV=GS2.1.s1771997665$o68$g1$t1771999005$j24$l0$h0; _clsk=x6l7qh%5E1771999009285%5E17%5E1%5Ey.clarity.ms%2Fcollect""",
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

