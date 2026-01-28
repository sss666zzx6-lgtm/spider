import requests


headers = {
    # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}
# url = "https://www.st.com/en/power-management/l6598.html"
# response = requests.get(url, headers=headers)
#
# print(response.text)
# print(response)


url = "https://www.st.com/en/power-management/voltage-references/products.html"
response = requests.get(url,headers=headers,timeout=10)

print(response.text)
print(response)