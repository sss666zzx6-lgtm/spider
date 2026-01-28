import requests

# url = "https://www.silergy.com/list/216"

url = "https://www.silergy.com/productsview/SY8884ADFC"

response = requests.get(url)

print(response.text)
print(response)