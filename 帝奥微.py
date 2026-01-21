import requests
import json

url = "https://www.dioo.com/api/web/productList"
data = {
    "pageNo": 1,
    "pageSize": 10000,
    "keyword": "",
    "names": "",
    "pid": 69
}
# data = json.dumps(data, separators=(',', ':'))
response = requests.post(url,json=data)

print(response.text)
print(response)