import requests

# url = "https://www.silergy.com/list/216"

url = "https://www.anpec.com.tw/en/product-list/Analog-Digital-Converter/"

response = requests.get(url)

print(response.text)
print(response)