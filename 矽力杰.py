import requests


url = "https://www.silergy.com/list/216"

response = requests.get(url)

print(response.text)
print(response)