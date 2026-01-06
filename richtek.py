import requests

url  = "https://www.richtek.com/Parametric%20Search/Parametric%20Search?tree_id=105&bookmarkid=b3c757ce-e0c0-ea11-80e1-005056863180&blockId=%7b7F7F50DB-7853-4AC1-A32A-18FF3C106D15%7d"
response = requests.get(url)
print(response.text)
print(response)