import os
import time
from curl_cffi import requests

headers = {
    "cookie": """_ALGOLIA=anonymous-b94a6d11-3b83-4b31-9800-f3c4324764d6; nmstat=272f2b61-d302-dee8-953c-17fbb3d27624; DT=DI1GWGErz9GRd2vZEkuhiDvKg; kapa_ab_group=ai_enabled; _ga_D1706WVDQV=GS2.1.s1773297649$o7$g1$t1773297700$j9$l0$h0; accessedDocumentsFetched=1; IDT-Language=en; ren_usr_pr=0; MkHcCurrencyId=USD; cf_clearance=sLyOMvsXV3Orni3fvIUyH0GMdTXHQYfsj0Milo121eU-1773297692-1.2.1.1-B3mGEdk3fG4hI5_9UxGa4ies5BxUA88gdvG8mSR7Bov_DrIQYxH2LC3jV8z4beWYHcH6k_ZAal9tIJRyt8rPI4JqjC9bYoxQEfYW7.pIRUCTlcK_.Hz42yf5eQfyLbO8rsKGBeljIkyZ8YbI97vIsgRZKzg7SXL.P3T3guCImmwTY5JNMPpUaOrLKveHgFVZePpn7nKSCU3TDgxH36.4taEgwMls4n8BNwZBIXXuggLxrEofAXTcV8n9WWpBX8Mw; xids=1029n-gZ9gFQmKBQryiTLsjiQ; idx=eyJ6aXAiOiJERUYiLCJ2ZXIiOiIxIiwiYWxpYXMiOiJlbmNyeXB0aW9ua2V5Iiwib2lkIjoiMDBvMWNneDRvNHlBYXBZMmgzNTciLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiZGlyIiwieHNpZCI6ImlkeDZPQTZCLVNUUjRDVUlCbGZ3R2pCLXcifQ..rHKx3EMQ88woNH6H.w4H6dMD74j_hXwC2uCNzJsTwftRwPoZRYadROxQKwu9ZurEWD8ydxBzaGpaHiYZ_BwdeGTeFHRL2np-mCgniYWBlunRQaiHe5-HvlAl_0djmhvjIzSUafgin5a1sfQzapuZJlTC5T7UJB79OKc-pg2Tj52l-5TZM5OCj01DTvPYpoC_G0vXkOF5JKU-IyK5ygvuBqfQWWxIY8yG7S9MVjOUfWKEDD0wUb75RMlcqRAGd5L3zPgwolUM3kgilAAB4Imu0Ni-Z9QaTSxmPz5zMMtSnkYqOybABMjsNftTnf15XHO44IhIseSqloXBy9DtVl4OhxGTfYl6r_xnqix4FmCCkf751bh1IfFnW2LRdnbC-RnqDUmXhccXQdHcGMqKtomp98P3JyOoutE7aktrepguVECxU_qZE1dSnG3LC-Zu_Yia2ZTuOACIA5PttspsPhE7GoIphMWyo1WeR_63rdXa639U5bYTOROaYRUs_NtvPW27FtD9OEOHGspTMjuaNAnaH_azrZcenjdoNgOzBTfziNUJoiOknL5gugQGDuxsesE0YjEcr7aprX8ZCmmr3Xe4CTXsCOhXvep2YEERDm6DituqX7GO1-uhb3FLyNFdzLi91Y1M8WzEhyEmDl77zfcnXVsBVQQDEDDW640CZgcbMcvlQn_aIEMH9r_8MVeZwVX8THRk5u8OwQFuLUU9Fa9lswNbF3quWZIGpmyrLSoc-rkcFaodBYLgCHyYtgNG9baxUATu8gDy7hpbIe3QqllZPE2hvErXfL4IL2seW2hFixYsPyv5KDcCkFK85qhWr_YKxwoHWNwwcF0LY3BBWzT_e7NB5cDicYtjwuuxQg6zvRWlaGCoTStUd_B-BQB4-O_-cFlUUS3AlxKuikGvfCwa70MoW4Sw6BBSB-fGDN4q7lnfGhOE6zWgl7PfMKG6jwsI.z7hV1YWlAKSvTV6gaKKWjw; myr=102Bxjt8k2xQbSTDVHWugleBA; idt_user_login_type=login; uid=6942801; referrer_path=/products/cl8060; notice_behavior=none; _ga=GA1.1.1401676060.1772535507; ELOQUA=GUID=7C83A6B8AC734A69877ED6FFC79B8D00; _gcl_au=1.1.2137071434.1772535507.426341254.1773297694.1773297694; MkHcLang=en; sid=102Bxjt8k2xQbSTDVHWugleBA; JSESSIONID=312E85D56041FCA75D475719AD63142E; proximity_b7b50f02d73fdbb68d58d277864c3613=eyJ6aXAiOiJERUYiLCJwMnMiOiItcnVTTWFZWlJhRk0xRWxnZmwwdW5BIiwicDJjIjoxMDAwLCJ2ZXIiOiIxIiwiZW5jIjoiQTI1NkdDTSIsImFsZyI6IlBCRVMyLUhTNTEyK0EyNTZLVyJ9.FTCbrZw82x6TM-Jy6DxnIGEoaAr3utISd_jNoNebnwqWxtwC2lBlaA.SIi5ndnku8lvcq2I.Xa7KAd5wQ8H1rhFGKZnxCS4a1-NFalBZDez0cg340aJwPLDWwxOpBHaT-W58SZiuhD-fPJwpa253nTymwkfL5fmCntasZULkdFDJ3Y5m_zKJnbb5S4hpavYbki2TqCsI5WpD6jVt8ePa1Sj0Aro6ORb_LJpTwHBD66R-BViG3aGReQ.BypzzZMmvwlbslcYxk1jzg; __cf_bm=qclzfW0rS5yWXEkB0sMW.1189eDfAjV.HyH5uVgFGOU-1773297692.560536-1.0.1.1-26rbmX5XuiWayt5t1aBlfJK30fH95OwRnh17h7un9vwbyVLbFEen7aiGNgDkTx_Tzp1jAHu3rSD4qVpPT9Os349u7PkJKqsUCBZe0eYA0zEKu4ihwEa915iqs8.nXt0d; SSESS8d786bdf64747b7f1b2e52f729beec12=24k0boqc4f4ihl523khmiiu96a""",
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
pdf_url = "https://www.renesas.com/en/document/dst/cl8060-datasheet"
# cl8060
save_path = "cl8060_datasheet.pdf"
time.sleep(1)
try:
    response = requests.get(
        pdf_url,
        headers=headers,
        # cookies=cookies,
        stream=True,
        impersonate="chrome110"
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

