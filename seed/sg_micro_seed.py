import os
import time
import requests
import json

from bs4 import BeautifulSoup

url = "https://www.sg-micro.com"

response = requests.get(url)

# print(response.text)

def bulid_url():
    soup = BeautifulSoup(response.text, 'lxml')
    result = []

    main_divs = soup.select(r'div.grid.grid-cols-1.gap-4.md\:grid-cols-2 > div')

    for main_div in main_divs:
        # 提取一级分类名称
        level1_name = main_div.find('div', class_='bg-primary').get_text(strip=True)
        # 构造一级分类的URL（根据二级URL规律推导）
        level1_url = f"{url}/products/{level1_name.lower().replace(' ', '-')}"

        # 初始化一级分类字典
        level1_item = {
            "url": level1_url,
            "familyName": level1_name,
            "level": 1,
            "children": []
        }

        # 找到当前一级分类下的所有二级分类li元素
        level2_li_list = main_div.select('ul.grid-cols-2 > li')

        for li in level2_li_list:
            # 提取a标签
            a_tag = li.find('a')
            if not a_tag:
                continue

            # 提取二级分类URL
            level2_url = url + a_tag.get('href', '').strip()
            # 提取二级分类名称（优先用title属性，避免文本中的格式问题）
            level2_name = a_tag.get('title', '').strip()
            # 处理特殊字符（&amp; 转 &）
            level2_name = level2_name.replace('&amp;', '&')

            # 构造二级分类字典
            level2_item = {
                "url": level2_url,
                "familyName": level2_name,
                "level": 2,
                "children": []
            }

            # 添加到一级分类的children中
            level1_item['children'].append(level2_item)

        # 将一级分类添加到结果列表
        result.append(level1_item)
    return result


def fetch_level2_urls(category_result: list):
    level2_relative_urls = []
    for level1 in category_result:
        for level2 in level1['children']:
            if level2['level'] == 2 and level2['url'].strip():
                level2_relative_urls.append(level2['url'].strip())

    print(f"共筛选出 {len(level2_relative_urls)} 个level=2的URL")

    # 第二步：拼接完整URL并请求
    success_results = []
    for idx, relative_url in enumerate(level2_relative_urls, 1):

        try:
            # 发送请求
            response = requests.get(url=relative_url)

            if response.status_code == 200:
                print(f"请求成功")
            else:
                print(f"请求失败：HTTP状态码 {response.status_code}")
        except Exception as e:
            print(f"请求失败：未知错误 - {str(e)[:50]}")

        time.sleep(1)

    return None


if __name__ == "__main__":
    result_list = bulid_url()
    print(json.dumps(result_list, indent=4, ensure_ascii=False))

    fetch_level2_urls(result_list)



    # base_path = "./seed_json"
    # file_path = os.path.join(base_path, "sg_micro.json")

    # with open(file_path, "w", encoding="utf-8") as f:
    #     json.dump(result_list, f, indent=2, ensure_ascii=False)