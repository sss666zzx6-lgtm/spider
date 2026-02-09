import requests
from bs4 import BeautifulSoup
import json
import re


def parse_product_detail(url:str,ppn: str, application_level: str):
    fieldMap = dict()
    try:
        # 发起请求，加请求头+超时，避免被拦截/卡死
        response = requests.get(url, timeout=15)
        response.raise_for_status()  # 抛出4xx/5xx状态码异常
        response.encoding = response.apparent_encoding  # 自动适配编码，避免乱码
        page_html = response.text



    except requests.exceptions.RequestException as e:
        print(f"请求URL失败：{e}")
    except json.JSONDecodeError as e:
        print(f"JSON解析失败（字符串格式异常）：{e}")
    except Exception as e:
        print(f"解析数据时发生未知错误：{e}")