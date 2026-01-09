import requests
import ceshi
session = requests.Session()


headers = {
    "accept": "application/json",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "origin": "https://www.monolithicpower.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.monolithicpower.com/en/products/power-management/data-center/mpq8645.html",
    "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}
cookies = {
    "_fs_ch_st_FSBmUei20MqUiJb9": "AfA8BiqDDLzxFSYAvPeXJFLMI2-yq2MTxPRi3dVkCw_p8gWeBN6TrhonUvNdXsNDb5jvKZW5N6RI0aBR-rxzH4YFT85QzRUMEb3NXL-WuRvCgKG8LL3uACsHJKMyNPvVOT33hY67sZfLieAY_KZnbRTQiJRSI074Zd6e5RjDBtC3yfmtaB2VaQEPgQlJ08AlWWysao1VbiSICa-qGVnRUzmneg2Bl40WYSJEuLrug0zLktkyQ2ae7ceKf-uPKxA5AWe6rvvLJB8Xuwl4ccairfYriORb8ia5u33MyGkETJ99Qnc4dNyK40dMNkVJyl9tPlRpnXw2cwCQOALuR8PY7eOThK_KddKfhRBTpJZNgiQtftIS7aTTJm8pwKjUI6Xn415P"
}
url = "https://www.monolithicpower.com/_fs-ch-1T1wmsGaOgGaSxcX/fst-post-back"
data = {
    "token": "AbgMmh3uAMYXQMqUyO_eZ5eGZ4DPj6wWFBsCrIPxeLqm2Qqs3IpE14N5j7jytcPnf242UxjVWfo9x3SkEum3-WQ9C2GlZqPXLPv7chQiRm-IcMhSm3kdCnJ5nRBRTkEL_Y6-lRyPlAxChiBjWnQE37GRRqR5cYUl_3RawtdEFC_SpxqSyU9B3855zyJg9dHqt6BndCvvmi3Jj9sSHP6n3T87rD2qp0CBSikS-hsOsWXxZhXIVnsPXQbhMbE9jIA--xwxEnVL9h61heYVftoKynipzC1gcPXYHLVEZcqUacX7el7JrtFBa1JDf992lAF5tR8FgoPYKSRnI8dCLvDDUCPEogKqad_ImB_nGSGPrQNls2YTTcNdQT1JCgZK5WBaVXXDal96MNkQAadisgI-1IFcQXupWgYLATFg8A8NX_Jpqn5L",
    "data": [
        {
            "ty": "pow",
            "base": "gYvAZCT5WijdsOQp",
            "answer": "tl",
            "hmac": "e6c33bb5197ccf9718e2c6807557de91b49ca9f15dd79c2ac9a5783a1937cc55",
            "expires": "1766744021"
        }
    ]
}
# data = json.dumps(data, separators=(',', ':'))
response = session.post(url,json=data)


print(response.text)
print(response.cookies)

print("响应状态码：", response.status_code)
print("响应头中的Set-Cookie：", response.headers.get("Set-Cookie"))
print("Session中保存的Cookie：", session.cookies)