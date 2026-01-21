import json
import os
import re
import requests
from bs4 import BeautifulSoup
import time
import chardet

if __name__ == "__main__":

    url = "https://www.xlsemi.com/products_DC_DC_buck_hv.html"
    response = requests.get(url)

    # print(response.text)
    response.encoding = response.apparent_encoding
    # print(response.text)

    raw_html = response.text
    # 1. 替换掉所有<html>...</html>片段（反爬干扰）
    clean_html = re.sub(r'<html.*?</html>', '', raw_html, flags=re.DOTALL | re.IGNORECASE)
    # 2. 给干净的内容包裹一个<html>标签（让BeautifulSoup能正常解析）
    clean_html = f"<html>{clean_html}</html>"

    soup = BeautifulSoup(clean_html, "lxml")
    print(soup.prettify())
    print(f"页面编码：{response.encoding}")



    # base_path = "./seed_json"
    # file_path = os.path.join(base_path, "lowpowersemi.json")
    #
    # with open(file_path, "w", encoding="utf-8") as f:
    #     json.dump(leaf_result, f, indent=2, ensure_ascii=False)