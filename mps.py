import requests


# headers = {
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
#     "cache-control": "no-cache",
#     "pragma": "no-cache",
#     "priority": "u=0, i",
#     "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-dest": "document",
#     "sec-fetch-mode": "navigate",
#     "sec-fetch-site": "cross-site",
#     "sec-fetch-user": "?1",
#     "upgrade-insecure-requests": "1",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
# }
# cookies = {
    # "ipAddress": "212.135.214.2",
    # "searchReport-log": "0",
    # "_gcl_au": "1.1.1745802299.1766539562",
    # "Hm_lvt_96a83d53ee50f608d33fd01c7f644870": "1766539562",
    # "HMACCOUNT": "4AB96E1A380B0DB7",
    # "_fbp": "fb.1.1766539563144.177218975460278352",
    # "_mkto_trk": "id:186-OUG-983&token:_mch-monolithicpower.com-26e1a08916d89e1dac90f8fc92cc68e3",
    # "dd_anonymous_id": "9bd716b8-2d27-4a3c-bd79-2692a034fee4",
    # "CookieConsent": "{stamp:%27-1%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27implied%27%2Cver:2%2Cutc:1766539564037%2Ciab2:%27%27%2Cregion:%27HK%27}",
    # "_ga": "GA1.1.544416440.1766539564",
    # "_hjSessionUser_449473": "eyJpZCI6ImMzNjdlM2M5LTY4M2EtNTJiYS04ZjA1LTZkNDc2MWIyZTFhYyIsImNyZWF0ZWQiOjE3NjY1Mzk1NjQyMTYsImV4aXN0aW5nIjp0cnVlfQ==",
    # "PHPSESSID": "k6sk29hl36s806tc3lvvtjgrkg",
    # "_clck": "wvphpy%5E2%5Eg26%5E0%5E2184",
    # "form_key": "FQa8VpUPthCtHGvc",
    # "mage-cache-storage": "{}",
    # "mage-cache-storage-section-invalidation": "{}",
    # "mage-cache-sessid": "true",
    # "recently_viewed_product": "{}",
    # "recently_viewed_product_previous": "{}",
    # "recently_compared_product": "{}",
    # "recently_compared_product_previous": "{}",
    # "product_data_storage": "{}",
# AYu9ZxeRsE_xwo_eIsMBuRSnSfmuPa7uC7ggzptGgtG3b4GKJSVLKduU6EGYsJO0h_Z7IsjioL-XP2MLoiK-SnRBccuWAk2xIbFwAWgTvEtmUKALyj7eL4hTAg2NgfA412oXjkf7wR65-W67Eud-acK_zrGHtV0RoVLRsQ1NBWdpkx7uxPMSW1bQULlMvkAPrjb1-oapEo85M6vvgD1tCA-dsM4cbTRucS1Q6BjEaY3aHaNOBW5fZWC-4OVax_cLy4IgWKo1vcHDnlEy;
# eyJpZCI6Ijk5MzQzNWEyLWE2ODQtNDU0NS04YmRmLWYxMWYzZWViMDNjMyIsImMiOjE3NjY3Mjc0OTQ2NTMsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=
#     "_fs_ch_cp_79UUvfpJ5mWYtLQv": "AYu9ZxeRsE_xwo_eIsMBuRSnSfmuPa7uC7ggzptGgtG3b4GKJSVLKduU6EGYsJO0h_Z7IsjioL-XP2MLoiK-SnRBccuWAk2xIbFwAWgTvEtmUKALyj7eL4hTAg2NgfA412oXjkf7wR65-W67Eud-acK_zrGHtV0RoVLRsQ1NBWdpkx7uxPMSW1bQULlMvkAPrjb1-oapEo85M6vvgD1tCA-dsM4cbTRucS1Q6BjEaY3aHaNOBW5fZWC-4OVax_cLy4IgWKo1vcHDnlEy",
#     "_hjSession_449473": "eyJpZCI6Ijk5MzQzNWEyLWE2ODQtNDU0NS04YmRmLWYxMWYzZWViMDNjMyIsImMiOjE3NjY3Mjc0OTQ2NTMsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=",
    # "section_data_ids": "{%22gtm%22:1766727492}",
    # "Hm_lpvt_96a83d53ee50f608d33fd01c7f644870": "1766727727",
    # "_uetsid": "a1f8c180e21411f08e739b63519be30a",
    # "_uetvid": "82a4bbd0e06711f0a4694300aca209b4",
    # "_clsk": "9v0qwt%5E1766727738080%5E2%5E1%5Ed.clarity.ms%2Fcollect",
    # "private_content_version": "804d38cf52c1b20245e5c82dddb1c2b5",
    # "_ga_XNRPF6L9DD": "GS2.1.s1766727566$o3$g1$t1766727739$j9$l0$h817798821",
    # "AWSALBTG": "IPzce/8IbvZViMWK/iYk7GiZ3bvd50lNRxiybaeLhZ8/OqdLng0JZ9tVVIQ2ado0dbJ6B8MvrWlgypEeKHq1yfQd1EgPUJL2t2GeOetpIviAfJXUR5stKnF7Iv9T6W2UqHkBa/mEsUC7E5fEHiYRnWiV6dIVc88bNbUjBRfF7sTSWMoFFBc=",
    # "AWSALBTGCORS": "IPzce/8IbvZViMWK/iYk7GiZ3bvd50lNRxiybaeLhZ8/OqdLng0JZ9tVVIQ2ado0dbJ6B8MvrWlgypEeKHq1yfQd1EgPUJL2t2GeOetpIviAfJXUR5stKnF7Iv9T6W2UqHkBa/mEsUC7E5fEHiYRnWiV6dIVc88bNbUjBRfF7sTSWMoFFBc=",
    # "AWSALB": "HUzS6gzMfF1b67E2OeGEwUFNB+K67PegJRJwGqiol5Jp9cGWvT07KUEwJ233RazmPEfJsUke7BFwXBA1Qbx5LkLOrn2e1FoIy0JZpLdZYsmEGQYiEz3R/WZdxMe7",
    # "AWSALBCORS": "HUzS6gzMfF1b67E2OeGEwUFNB+K67PegJRJwGqiol5Jp9cGWvT07KUEwJ233RazmPEfJsUke7BFwXBA1Qbx5LkLOrn2e1FoIy0JZpLdZYsmEGQYiEz3R/WZdxMe7"
# }

# _fs_ch_cp_79UUvfpJ5mWYtLQv=AZySPWHePXZ61TAjIA4haOsz3pbCUKXG3wCIMniZhtuCtYVWapx140nyQ45UZZvvffx7Ad8P6-ScruNWYcE0SpAaUfri-TB9PVWkDbkORxLTy9JNJxOLrhPkfRRuRkZGZ42u_ITKI8zZh3MZtcspG5H55SGEjeodJMBa2eNpqkeBrKNQB0GKuyjK7aYVpbzI6wxZcV-fmEDIOKhywXIGJpNwihseKqGvqj1ShDoLraBQs9AdqAvEn_nqcnpGyOGP4ZSPDiHyKtJ5gjwNzA==
# cookie_str = "_fs_ch_cp_79UUvfpJ5mWYtLQv=AYu9ZxeRsE_xwo_eIsMBuRSnSfmuPa7uC7ggzptGgtG3b4GKJSVLKduU6EGYsJO0h_Z7IsjioL-XP2MLoiK-SnRBccuWAk2xIbFwAWgTvEtmUKALyj7eL4hTAg2NgfA412oXjkf7wR65-W67Eud-acK_zrGHtV0RoVLRsQ1NBWdpkx7uxPMSW1bQULlMvkAPrjb1-oapEo85M6vvgD1tCA-dsM4cbTRucS1Q6BjEaY3aHaNOBW5fZWC-4OVax_cLy4IgWKo1vcHDnlEy; _hjSession_449473=eyJpZCI6Ijk5MzQzNWEyLWE2ODQtNDU0NS04YmRmLWYxMWYzZWViMDNjMyIsImMiOjE3NjY3Mjc0OTQ2NTMsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0="

cookie_str = "_fs_ch_cp_79UUvfpJ5mWYtLQv=AduUVq3auVkP8uM-WP90_9Jxtj6a4WtAxEfyAFO-N5-i9KKX96qrMj7YM3jaNo4uwgFpvHNMr8DvvkRN0631kvvYp-Fu-4HkS6pxOql2GZU4qCRGa6oDEXJQxPxXeWDZhrXqibUtjB5FvBXBX5WUHmq96pRxUnzQbcRAj3IjqBJ8_eqIM7zCgh4ePxs5T_I-20mQ37hcej_fjktukbeelRq4cGa4CDo50lfbIdotaQuh0j9HQB29SBCReknymF3UrChD556IQG44HuY7Xw=="
headers = {
    "Cookie": cookie_str  # Key为Cookie，Value为完整字符串
}
# url = "https://www.monolithicpower.com/en/mp38875.html"
# url = "https://www.monolithicpower.com/en/products/power-management/data-center/processor-core-power-intelli-phase-monolithic-drmos/mp86936.html"
# response = requests.get(url,headers=headers)

# url = "https://www.monolithicpower.com/en/mp38875.html"
# response = requests.get(url)
#
# print(response.text)
# print(response)

# aa ={
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



url = "https://www.ti.com/product/MSPM0L1116"
response = requests.get(url)

print(response.text)
print(response)