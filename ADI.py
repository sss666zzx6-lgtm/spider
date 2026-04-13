import requests


headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://toshiba.semicon-storage.com/parametric/product?region=apc&lang=en&code=param_607&p=50&i=1&sort=3,asc&cc=0d,1d,35d,38h,37h,3d,19d,20d,21d,14d,12d,9d,22d,23d,24d,7d,10d,11d,5d,8d,25d,26d,27d,13d,36d,15d,28h,29h,30h,31h,32h,33h,34h&f%5B%5D=11%7C110&f%5B%5D=11%7C125&f%5B%5D=11%7C150",
    "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Google Chrome\";v=\"146\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}
cookies = {
    "OptanonAlertBoxClosed": "2026-01-30T01:34:44.948Z",
    "_gcl_au": "1.1.1462152175.1769736885",
    "_ga": "GA1.1.1252410829.1769736885",
    "visitor_id755793": "2176083952",
    "visitor_id755793-hash": "ea7b2a4d5ac75ac02bb086e200a0fac167735de802e59c2e2d2f9e54494a94c34c8760d981729c19ceaa4ba611f96fc9c6ce8d91",
    "__sna_s1d": "3m2ieR7Xua1u0VGz3jiWvPaHseE3Dh",
    "DC": "1",
    "user_region": "ap-en",
    "JSESSIONID": "993B4790E0B46775228BA1E759E89DC2",
    "OptanonConsent": "isGpcEnabled=0&datestamp=Wed+Apr+01+2026+15%3A09%3A45+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202409.2.0&browserGpcFlag=0&isIABGlobal=false&consentId=a8e26393-629d-4deb-9aea-f953dfed443d&interactionCount=2&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CC0003%3A1&hosts=dlf%3A1%2Cldc%3A1%2CH18%3A1%2Ceph%3A1%2Cfpa%3A1%2Csky%3A1%2CH30%3A1%2CH5%3A1%2CH20%3A1%2CH22%3A1%2CH28%3A1%2Cmdv%3A1%2CH24%3A1%2Cuya%3A1%2CH33%3A0&AwaitingReconsent=false&intType=1&geolocation=HK%3B",
    "pt_56601f3b": "deviceId%3Def6226d2-d305-477c-b26e-93683c0f370d%26sessionId%3D374def58-f26d-42d3-9174-5c9248511069%26accountId%3D%26vn%3D14%26pvn%3D5%26lastActionTime%3D1775027392107%26",
    "_ga_WT06FC2CJF": "GS2.1.s1775027303$o21$g1$t1775027392$j35$l0$h0"
}
url = "https://toshiba.semicon-storage.com/parametric/rest/getRowData"
params = {
    "region": "apc",
    "lang": "en",
    "code": "param_607"
}
response = requests.get(url, params=params)

print(response.text)
print(response)