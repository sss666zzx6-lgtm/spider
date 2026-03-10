import json
import os
from util.create_darwin_api import create_api




headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "Cookie": "PHPSESSID=25v0vobd0hnscdu0n4n6mmh3ok; dt=dt; e1192aefb64683cc97abb83c71057733=Tm90aWNl; CUPID=b907a86f086eb30f23c98e577807afd6; 2a0d2363701f23f8a75028924a3af643=MjEyLjEzNS4yMTQuNQ%3D%3D",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
}

path = "https://www.firstsilicon.co.kr/theme/daontheme_pro10/html/business/04.php?cate_id=0305"
category = "9999999999"
custom_map = {"category": category}
create_api(plan_id="2ae1767c5edc54872da6ee2e1390506b", path=path, custom_map=custom_map,headers=headers)