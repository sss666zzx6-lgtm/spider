import requests
from bs4 import BeautifulSoup
import json
import re
from silergy_util.mapping import product_status,application_level_mapping
from silergy_util.list_parse import parse_product_data_from
from silergy_util.product_parse import parse_product_detail

# 目标站点根域名（处理相对链接）
BASE_DOMAIN = "https://www.silergy.com"




# ------------------- 测试使用 -------------------
if __name__ == "__main__":
    target_url = "https://www.silergy.com/list/288"

    # 提取数据
    product_data = parse_product_data_from(target_url)
    print(f"共提取到 {len(product_data)} 个产品数据：")
    for idx, prod in enumerate(product_data, 1):
        ppn = prod["part_number"]
        application_level = application_level_mapping(prod["part_type"])
        product_url = f"https://www.silergy.com/productsview/{ppn}"

        fieldMap = parse_product_detail(product_url, ppn, application_level)



