import requests
from bs4 import BeautifulSoup

# 写个函数来解析，将products 传进去，获取分类名和对应url，只保留叶子节点，{
#     "url": "",
#     "category": ""
#   },按照这个格式，category按照层级使用^进行拼接


# 开益禧-KEC     Content-Type    application/unknown
# Kodenshi-AUK   Content-Type	PDF ÆÄÀÏ; Charset=euc-kr

import requests
import re


def recovery(secret,proxies=None):
    url = "https://www.silergy.com/index/restoreAccess"

    data = {
        "secret": secret
    }
    try:
        # 发送POST请求（如果不用代理，删掉proxies参数）
        response = requests.post(
            url=url,
            data=data,
            # proxies=proxies,  # 不用代理则注释这行
            timeout=10
        )

        # 打印响应结果
        print("请求状态码：", response.status_code)
        print("解封接口返回内容：", response.json())  # 接口返回JSON格式

    except requests.exceptions.JSONDecodeError:
        # 如果返回不是JSON，打印原始文本
        print("接口返回非JSON：", response.text)
    except Exception as e:
        print("请求失败：", str(e))


def get_secret(text):
    secret = re.search(r'secret=([0-9a-f]{32})', text).group(1)
    if re.search(r'secret=([0-9a-f]{32})', text):
        return secret
    else:
        print('未找到')
        return False


if __name__ == '__main__':
    target_url = "https://www.silergy.com/list/294"

    response = requests.get(target_url, timeout=5)
    # print(response.text)
    print(response)
    if response.status_code == 403:
        print(response.text)
        text = response.text
        secret = get_secret(text)
        print(secret)
        recovery(secret=secret)
        response = requests.get(target_url, timeout=5)
        # print(response.text)
        print(response)