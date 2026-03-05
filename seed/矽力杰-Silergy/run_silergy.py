import requests
from bs4 import BeautifulSoup
import json
import re
from list_parse import parse_product_data_from,application_level_mapping
from product_parse import parse_product_detail
from src.utils.logger import get_logger
from src.core.clean_run import manage_complete_run

logger = get_logger("product-run")

if __name__ == "__main__":
    # url = "https://www.silergy.com/list/294"
    # product_data = parse_product_data_from(url)
    # print(json.dumps(product_data, indent=4, ensure_ascii=False))

    with open("silergy.json", "r", encoding="utf-8") as f:
        seed_data = json.load(f)
        for item in seed_data:
            path = item["url"]
            category = item["category"]
            product_data = parse_product_data_from(path)
            logger.info(f"{path}共提取到 {len(product_data)} 个产品数据：")
            for idx, prod in enumerate(product_data, 1):
                ppn = prod["part_number"]
                application_level = application_level_mapping(prod["part_type"])
                product_url = f"https://www.silergy.com/productsview/{ppn}"
                datasheet = prod["datasheet"]

                fieldMap = parse_product_detail(product_url, ppn, application_level,category=category,datasheet_id=datasheet)
                if fieldMap:
                    logger.info(f"{ppn}解析完成")
                    manage_complete_run(fieldMap)
                else:
                    logger.info(f"{ppn}解析结果为空")



