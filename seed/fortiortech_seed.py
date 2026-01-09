import os

import requests
from bs4 import BeautifulSoup
import json

base_url = "https://fortiortech.com/en"

response = requests.get(base_url)
# print(response.text)
soup = BeautifulSoup(response.text, "lxml")

# 2. 提取所有a标签，并整理数据
result_list = []
target_div = soup.find('div', class_='nav-wrap product-nav-wrap c2')
if target_div:
    a_tags = target_div.find_all('a')
    for a in a_tags:
        # 提取href（url）
        url = "https://fortiortech.com" + a.get('href', '')

        # 提取并清理分类文本
        span_tags = a.find_all('span')
        category = span_tags[1].get_text(strip=True, separator=' ') if len(span_tags) >= 2 else ''

        # 构造指定格式字典
        item = {
            "url": url,
            "category": category
        }
        result_list.append(item)

print(json.dumps(result_list, indent=2, ensure_ascii=False))




base_path = "./seed_json"
file_path = os.path.join(base_path, "fortiortech.json")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(result_list, f, indent=2, ensure_ascii=False)


