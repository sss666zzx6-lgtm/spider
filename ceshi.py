import requests


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Referer": "https://www.jjm.com/profhqj1/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Google Chrome\";v=\"145\", \"Chromium\";v=\"145\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
cookies = {
    "__51cke__": "",
    "_ga": "GA1.1.257169659.1773969879",
    "is_lang": "1",
    "_ga_M5SWZSW9JX": "GS2.1.s1773969878$o1$g1$t1773971875$j51$l0$h0",
    "__tins__21857693": "%7B%22sid%22%3A%201773971872161%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201773973675201%7D",
    "__51laig__": "9"
}
url = "https://www.jjm.com/prokkg1/"
response = requests.get(url)

print(response.text)
print(response)