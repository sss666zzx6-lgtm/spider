import requests

url = "https://auk.co.kr/eng//s2/product_down.asp?idx=438"

response = requests.get(url,headers={"content-type":"application/pdf"})

print(response.text)
print(response.headers["content-type"])