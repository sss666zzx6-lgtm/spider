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

# session = requests.Session()
#
# data = {
#     "username":"jasonlee@hhsmdl.freeqiye.com",
#     "password":"Hhsmdl123456&",
#     "form_build_id":"form-WWL8IdWrldeY9hGG0oOvNvwR3vH4OdyFbVqnc7PisxI",
#     "form_id":"idt_okta_login_form",
#     "captcha_sid":"53901963",
#     "captcha_token":"92UYVA_Z816Rod2uuakx9mbyV5cHQJYC16iP1bATSyI",
#     "captcha_response":"Turnstile no captcha",
#     "cf-turnstile-response":"0.1N7BIzYj7U91i80gDmM7ydZoX9VSgFpHu-NvaEc8i4tLJNUu7p5X6Z2o-JpzxPeECFRqILCHL3MPlTTa4z-uRTvVzJVM2sa_-Qqw9m69_-8nE8-wq1qj9HitK3JsZKkJlOMKSN4Tkk9WSMxAQoT8UP1sVEbiONbNEok7eRnR2R9lHBRdgpkRb_c55mux0FFn_nTlCabF3M2X6akvCvGOXXDOsPKewt7FFthbadveJ-AyzcChxEL-zwfjKn8Ylx6yFMY3GAZNch4UGUnIUHsPeTM2AvQ5Fwgowqtiiyof3L36kfZ4vSEcdhMmDvG6dE9Zbg9Nc_Yi3DsQ4agHipzfw3Ry5aEU63ZhsYqjGayTj5I3tg01aVpuUJ_4NtRqcDPkpLwquHsjnHPmgjdYgfa5jdJFlmM1oOnmvo7_XKdXQk0KtR8X0vNzFTT-hzD7Vz7D7vhcwg3mhExKcRM9yaX6u9-Esp7v53fwH43tlFuIEEemdvNcxO09G2HE5oGtIWmdKu3-Q0apxg-XK0JJbsQpudgPafqs65svkF1UaP2-b8dibFb13kEWI-7g4ABTBbFvwKs8QeKb6BNrA31AMu64ExjMGnSslEcpkVnE2M_Jqv9nXsJM3nsiqb8ibnAA9-mRJEYI12uNQ4TcIoG0P__CUaMbFLfjqtJ08Wq5a9-t5PamlV9WC0qL_Fm-EFfpogiuSoyplrQKQf0jBSVg5v-gNXhiC5PyVQALUEJdU6ymD0ANovWZm814GT7BNFqvZU3U8VXzBnm376DetCuR-JeEdfJUnZu0NFgnXUxA3SlWQJA1QDe2Yp8zJFmoQN-tGaKWqWhyV4xKt70hZvXle2DAd3qjFESE-oFlblCHdE2xwpG0sCJM87qq6qBJoWflZ2c1xyW7Z-26AIMX3nXMy2gX9JeIzRWZsj9GDG8_-P0ZlYo.k4Sue5hEBAfyes1Gra1ZQg.a1f24dc70cd64279bb39cea70d73dc11ed7c014ab599cf7dbe310e5f1db27b88",
#     "captcha_cacheable":"1",
#     "op":"登录"
# }
#
# url = "https://www.renesas.cn/zh/oauth2/default/v1/authorize?client_id=0oa2ixjskq8o2hdJB357&response_type=code&scope=openid%20email%20phone%20profile%20MyRenesasUserInfo&redirect_uri=https%3A//www.renesas.cn/openid-connect/renesas_okta&state=u8bgwH9v_s6BizFSbxRviK5wWR9ej7O3M8HbucKztek"
#
# response = session.post(url,data=data,headers={
#     "Content-Type":"application/x-www-form-urlencoded",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
# })
# print(response.text)
# print(response)
# print(response.cookies)
# print(session.cookies)


# res = requests.get("https://www.renesas.com/en/products/analog-products/audio-video/wireless-audio/product-selector")
# print(res.text)
# print(res)


data = {
    "requests": [
        {
            "indexName": "prod_main_en",
            "facetingAfterDistinct": True,
            "facets": [
                "fDocType.lvl0",
                "fFeatured"
            ],
            "filters": "type:'Document' AND (nid:1619801 OR nid:1620131 OR nid:25422316) AND NOT staging:true",
            "highlightPostTag": "__/ais-highlight__",
            "highlightPreTag": "__ais-highlight__",
            "hitsPerPage": 15,
            "maxValuesPerFacet": 100,
            "page": 0,
            "query": ""
        }
    ]

}

# block_config=eyJpZCI6ImRvY3VtZW50YXRpb24tc2VhcmNoIiwibGFiZWwiOiJEb2N1bWVudGF0aW9uIiwibGFiZWxfZGlzcGxheSI6ZmFsc2UsInByb3ZpZGVyIjoicmVuZXNhc19ibG9ja3MiLCJlbWJlZGRlZF9ibG9jayI6ZmFsc2UsInJlbmVzYXNfYmxvY2tzX2FqYXhfbG9hZCI6dHJ1ZSwicmVuZXNhc19ibG9ja3NfYXV0aF9vbmx5IjpmYWxzZSwicmVuZXNhc19ibG9ja3NfYmxvY2tfd3JhcHBlciI6dHJ1ZSwic2hvd19xdWlja19saW5rIjp0cnVlLCJxdWlja19saW5rX2lkIjoiZG9jdW1lbnRzIiwidW5pcXVlIjp0cnVlLCJpc19zZWN0aW9uIjp0cnVlLCJpc19ncmlkX3dyYXBwZXIiOnRydWUsInJlbmVzYXNfYmxvY2tzX21hbnVhbF9hamF4X2xvYWQiOnRydWV9&context=eyJyb3V0ZSI6ImVudGl0eS5ub2RlLmNhbm9uaWNhbCIsInBhcmFtcyI6eyJub2RlIjoiMTYxMjk1MSJ9fQ==&_wrapper_format=drupal_ajax&js=true&_drupal_ajax=1&ajax_page_state%5Btheme%5D=kachow&ajax_page_state%5Btheme_token%5D=&ajax_page_state%5Blibraries%5D=eJx1VGu64yAI3VC9LsmPKDVMiWYEm-msfsy796bzSziHl4D6XNCGUkfgL_BKTzRM6XGjoC7hVJDJ211YUIFhZLSnuKLZE7BdjwWpgsUGdvjEpG6s0p9wxFVwARROmEEpOUpj1QN0BQMV9Cr2Ct0e4Ps82Q4ED7mq5rRr95wVy671COHUBowwYKq7XrrSeF_q0O2QtCx0RhMKaGYXw_D3ZTi_h1PoGL8p5k7csr_jc_3mPen0Eppe8VYwoYA44JiZwI4FBaH4_v_MPKCD7Tj7h1jwPtfW73mIciHD0PqrOXMH5UL-gj-r7OZ7XehxbBsAczdcIIgFhkv8O4LWNhwXsq_tkipu6_hnw0sAhhQrRHQykfr-6ji0yYOJwIzl9ZNs7RBG1avbWHKoXs3najbWxQYX8i6g-ELjMvgfpr8r-Yf52Nw2cZPgSRG-OW7Bjyxi1j3ZeVGIlKLdzgOvSkxK2K6Vk2n1aOs-7yt3tWpROwym1U4xmXmYi61Zqvts3xa0B9mW9DB5th3PYpfDaN8eQwLim7xEcVhfmg5x0P3XWJSvban-ASJSsWo
# block_config=eyJpZCI6ImRvY3VtZW50YXRpb24tc2VhcmNoIiwibGFiZWwiOiJEb2N1bWVudGF0aW9uIiwibGFiZWxfZGlzcGxheSI6ZmFsc2UsInByb3ZpZGVyIjoicmVuZXNhc19ibG9ja3MiLCJlbWJlZGRlZF9ibG9jayI6ZmFsc2UsInJlbmVzYXNfYmxvY2tzX2FqYXhfbG9hZCI6dHJ1ZSwicmVuZXNhc19ibG9ja3NfYXV0aF9vbmx5IjpmYWxzZSwicmVuZXNhc19ibG9ja3NfYmxvY2tfd3JhcHBlciI6dHJ1ZSwic2hvd19xdWlja19saW5rIjp0cnVlLCJxdWlja19saW5rX2lkIjoiZG9jdW1lbnRzIiwidW5pcXVlIjp0cnVlLCJpc19zZWN0aW9uIjp0cnVlLCJpc19ncmlkX3dyYXBwZXIiOnRydWUsInJlbmVzYXNfYmxvY2tzX21hbnVhbF9hamF4X2xvYWQiOnRydWV9&context=eyJyb3V0ZSI6ImVudGl0eS5ub2RlLmNhbm9uaWNhbCIsInBhcmFtcyI6eyJub2RlIjoiNTI4NTIxIn19&_wrapper_format=drupal_ajax&js=true&_drupal_ajax=1&ajax_page_state%5Btheme%5D=kachow&ajax_page_state%5Btheme_token%5D=&ajax_page_state%5Blibraries%5D=eJx1VOua4yAIfaE6eSQ_otSwJZoVbCb79GvunabzS845CAgkLmVsfC4D8Bc4pScapvi4kVcbcczI5JrdWFiBfmBsTnNlkyPgZj0WpgjmxrPFJ0a1Q5HupAOuhvWgcNIMStFSHIoepM3oKaNTaa7U7QGuS2PTguBhF9UUd3RPSTHvqEPwJ-oxQI-x7Di3ueoul77dKalZ6Iwm5NHMVwzDv8lweg2n0DL-AOZOXLO_8nP95jXpOAmNU7hljCggFjgkJmiGjIKQXfe7Mg_oUFtO7iENOJdK7fc8RLmIvq_91ZS4hXwR_8D3atv5Xe_yHUFLbbz1yZX6ABW7dfOz4yV5qDCTs0NOvji1oJqpDuvqyRBDgYBWRlLXXVP0df5gAjBjnt7F2hRhVL1e2zKbz3Xvde11ehSXaVjG_-b6t5B7mI8trnM3EZ4U4MfFLfiRRcy6LbsuCoFiaLbz4IsSkxLWZ6Voaj1KDnhfvKtXjdqiN7V2CtHMI118zVLdZ_-6ph3Itqo3mUSxXz8o7UOv-89hAV_b7vwHvvCn1Q

url = "https://kj220gaq35-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(5.45.0)%3B%20Search%20(5.45.0)%3B%20Browser%3B%20instantsearch.js%20(4.80.0)%3B%20JS%20Helper%20(3.26.0)&x-algolia-api-key=YjFlY2I5NTUxM2ZlN2RkMmRmNmRhNjM2MDA1ZmNmMTRmODE0NTA5N2ViNmM1YTEwNjg2NjE0MzcxNzc3NzgyY2ZpbHRlcnM9cHVibGljbHlMaXN0ZWQlM0F0cnVlK09SK2RvY0FjY2VzcyUzQWxvY2stYW5vbnltb3VzK09SK2RvY0FjY2VzcyUzQW5vLWxvY2srT1IrTk9UK2J1bmRsZSUzQWRvY3VtZW50&x-algolia-application-id=KJ220GAQ35"


response = requests.post(url, json=data)
print(response.json())




headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "x-newrelic-id": "UAIFWFZSABABVFFbBwADUVIG",
    "x-requested-with": "XMLHttpRequest"
}
url = "https://www.renesas.com/en/ajax/renesas-blocks/load/documentation_search"
params = {
    "block_config": "eyJpZCI6ImRvY3VtZW50YXRpb24tc2VhcmNoIiwibGFiZWwiOiJEb2N1bWVudGF0aW9uIiwibGFiZWxfZGlzcGxheSI6ZmFsc2UsInByb3ZpZGVyIjoicmVuZXNhc19ibG9ja3MiLCJlbWJlZGRlZF9ibG9jayI6ZmFsc2UsInJlbmVzYXNfYmxvY2tzX2FqYXhfbG9hZCI6dHJ1ZSwicmVuZXNhc19ibG9ja3NfYXV0aF9vbmx5IjpmYWxzZSwicmVuZXNhc19ibG9ja3NfYmxvY2tfd3JhcHBlciI6dHJ1ZSwic2hvd19xdWlja19saW5rIjp0cnVlLCJxdWlja19saW5rX2lkIjoiZG9jdW1lbnRzIiwidW5pcXVlIjp0cnVlLCJpc19zZWN0aW9uIjp0cnVlLCJpc19ncmlkX3dyYXBwZXIiOnRydWUsInJlbmVzYXNfYmxvY2tzX21hbnVhbF9hamF4X2xvYWQiOnRydWV9",
    "context": "eyJyb3V0ZSI6ImVudGl0eS5ub2RlLmNhbm9uaWNhbCIsInBhcmFtcyI6eyJub2RlIjoiNTI4NTIxIn19",
    "_wrapper_format": "drupal_ajax",
    "js": "true",
    "_drupal_ajax": "1",
    "ajax_page_state%5Btheme%5D": "kachow",
    "ajax_page_state%5Btheme_token%5D": "",
    # "ajax_page_state%5Blibraries%5D": "eJx1VGu64yAI3VC9LsmPKDVMiWYEm-msfsy796bzSziHl4D6XNCGUkfgL_BKTzRM6XGjoC7hVJDJ211YUIFhZLSnuKLZE7BdjwWpgsUGdvjEpG6s0p9wxFVwARROmEEpOUpj1QN0BQMV9Cr2Ct0e4Ps82Q4ED7mq5rRr95wVy671COHUBowwYKq7XrrSeF_q0O2QtCx0RhMKaGYXw_D3ZTi_h1PoGL8p5k7csr_jc_3mPen0Eppe8VYwoYA44JiZwI4FBaH4_v_MPKCD7Tj7h1jwPtfW73mIciHD0PqrOXMH5UL-gj-r7OZ7XehxbBsAczdcIIgFhkv8O4LWNhwXsq_tkipu6_hnw0sAhhQrRHQykfr-6ji0yYOJwIzl9ZNs7RBG1avbWHKoXs3najbWxQYX8i6g-ELjMvgfpr8r-Yf52Nw2cZPgSRG-OW7Bjyxi1j3ZeVGIlKLdzgOvSkxK2K6Vk2n1aOs-7yt3tWpROwym1U4xmXmYi61Zqvts3xa0B9mW9DB5th3PYpfDaN8eQwLim7xEcVhfmg5x0P3XWJSvban-ASJSsWo"
}
response = requests.get(url, headers=headers, params=params)

print(response.text)
print(response)
print(response.url)

url2 = "https://www.renesas.com/en/ajax/renesas-blocks/load/documentation_search?block_config=eyJpZCI6ImRvY3VtZW50YXRpb24tc2VhcmNoIiwibGFiZWwiOiJEb2N1bWVudGF0aW9uIiwibGFiZWxfZGlzcGxheSI6ZmFsc2UsInByb3ZpZGVyIjoicmVuZXNhc19ibG9ja3MiLCJlbWJlZGRlZF9ibG9jayI6ZmFsc2UsInJlbmVzYXNfYmxvY2tzX2FqYXhfbG9hZCI6dHJ1ZSwicmVuZXNhc19ibG9ja3NfYXV0aF9vbmx5IjpmYWxzZSwicmVuZXNhc19ibG9ja3NfYmxvY2tfd3JhcHBlciI6dHJ1ZSwic2hvd19xdWlja19saW5rIjp0cnVlLCJxdWlja19saW5rX2lkIjoiZG9jdW1lbnRzIiwidW5pcXVlIjp0cnVlLCJpc19zZWN0aW9uIjp0cnVlLCJpc19ncmlkX3dyYXBwZXIiOnRydWUsInJlbmVzYXNfYmxvY2tzX21hbnVhbF9hamF4X2xvYWQiOnRydWV9&context=eyJyb3V0ZSI6ImVudGl0eS5ub2RlLmNhbm9uaWNhbCIsInBhcmFtcyI6eyJub2RlIjoiNTI4NTIxIn19&_wrapper_format=drupal_ajax&js=true&_drupal_ajax=1&ajax_page_state%255Btheme%255D=kachow&ajax_page_state%255Btheme_token%255D="
response2 = requests.get(url2, headers=headers)  # 修复：调用url2而非url
print("\n===== 第二个请求 =====")

print(response2.text[:500])
print(response2.status_code)






