import json
import os
from util.create_darwin_api import create_api
import requests
import re

# base_path = "../seed_json"

def get_category_id(url):
    try:
        headers = {
            "cookie": "LOCAL_LOCALE=en",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        # 设置超时时间10秒，避免请求卡死
        response = requests.get(url, headers=headers, timeout=10)

        # 3. 校验响应状态（200表示成功）
        response.raise_for_status()  # 非200状态会抛出HTTPError

        # 4. 提取页面文本，匹配正则
        page_text = response.text
        # print(page_text)
        match_result = re.search(r'\\"categoryId\\":\s*(\d+)',page_text,re.S)

        if match_result:
            # 提取分组1的数字，转成整数返回
            category_id = int(match_result.group(1))
            print(f"✅ 成功提取categoryId: {category_id}")
            return category_id
        else:
            print(f"❌ 在URL {url} 中未找到categoryId匹配项")
            return None

    # 捕获请求相关异常
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求URL失败: {e}")
        return None
    # 捕获正则匹配/类型转换异常
    except (re.error, ValueError) as e:
        print(f"❌ 提取categoryId失败: {e}")
        return None

file_path = "southchip.json"
with open(file_path, "r", encoding="utf-8") as f:
    seed_data = json.load(f)
    for item in seed_data:
        path = item["url"]
        category = item["category"]
        category_id = get_category_id(path)
        if category_id:
            path = f"https://www.southchip.com/rest/items/product?filter%5Blang_is_main%5D%5B_eq%5D=true&fields=params_data%2Cimages%2Cmaterial_number%2Cis_new_product%2Cslug%2Cdatasheet1_file.id%2Cdatasheet1_file.title%2Cdatasheet1_file.filename_download%2Cdatasheet2_file.id%2Cdatasheet2_file.title%2Cdatasheet2_file.filename_download%2Cdatasheet3_file.id%2Cdatasheet3_file.title%2Cdatasheet3_file.filename_download%2Cpackage_image%2Cpublish.publish_id.publish_date&sort%5B0%5D=-is_new_product&sort%5B1%5D=-publish.publish_id.publish_date&filter%5B_or%5D%5B0%5D%5B_and%5D%5B0%5D%5Bpublish%5D%5Bpublish_id%5D%5Bstatus%5D%5B_eq%5D=PUBLISH&filter%5B_or%5D%5B0%5D%5B_and%5D%5B1%5D%5Bpublish%5D%5Bpublish_id%5D%5Benable%5D%5B_eq%5D=false&filter%5B_or%5D%5B0%5D%5B_and%5D%5B2%5D%5Bpublish%5D%5Bpublish_id%5D%5Bsite%5D%5Bid%5D%5B_eq%5D=2&filter%5B_or%5D%5B1%5D%5B_and%5D%5B0%5D%5Bpublish%5D%5Bpublish_id%5D%5Bstatus%5D%5B_eq%5D=PUBLISH&filter%5B_or%5D%5B1%5D%5B_and%5D%5B1%5D%5Bpublish%5D%5Bpublish_id%5D%5Benable%5D%5B_eq%5D=true&filter%5B_or%5D%5B1%5D%5B_and%5D%5B2%5D%5Bpublish%5D%5Bpublish_id%5D%5Bpublish_date%5D%5B_lte%5D=%24NOW&filter%5B_or%5D%5B1%5D%5B_and%5D%5B3%5D%5Bpublish%5D%5Bpublish_id%5D%5Bsite%5D%5Bid%5D%5B_eq%5D=2&filter%5B_and%5D%5B3%5D%5Bcategory%5D%5B_eq%5D={category_id}&page=1&limit=-1"
            custom_map = {"category": category}
            create_api(plan_id="9f03e7dda460d93549420356c55ef22b", path=path, custom_map=custom_map)