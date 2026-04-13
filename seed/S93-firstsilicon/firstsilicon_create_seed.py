import requests
from bs4 import BeautifulSoup
import json
import re
from Crypto.Cipher import AES
import time


cookies = {
    "CUPID": "b907a86f086eb30f23c98e577807afd6",
    "PHPSESSID": "lb77kb8nani6me5b6ba3adkhfl",
    "dt": "dt"
}


def extract_abc(html):
    """从 HTML 中提取 a, b, c 三个值"""
    # 匹配 toNumbers("...") 中的三个十六进制字符串
    pattern = r'toNumbers\("([a-f0-9]+)"\)'
    matches = re.findall(pattern, html)

    if len(matches) == 3:
        return {
            'key': matches[0],  # a
            'iv': matches[1],  # b
            'encrypted': matches[2]  # c
        }
    return None


def decrypt_cupid(key_hex, iv_hex, encrypted_hex):
    """AES 解密获取 CUPID token"""
    key = bytes.fromhex(key_hex)
    iv = bytes.fromhex(iv_hex)
    encrypted = bytes.fromhex(encrypted_hex)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)
    return decrypted.hex()

def get_soup(url,max_retries = 2):
    attempt = 0  # 当前尝试次数
    soup = None

    while attempt <= max_retries:
        attempt += 1
        print(f"\n【第 {attempt}/{max_retries + 1} 次请求】{url}")

        try:
            response = requests.get(url, cookies=cookies, timeout=30)
            html = response.text

            # 检查是否需要验证（包含 toNumbers 脚本）
            if 'toNumbers' in html:
                print(f"⚠ CUPID 已过期/无效，需要重新获取...")
                abc = extract_abc(html)

                if abc:
                    cupid_token = decrypt_cupid(abc['key'], abc['iv'], abc['encrypted'])
                    print(f"✓ 新 CUPID: {cupid_token}")
                    cookies['CUPID'] = cupid_token

                    # 使用新 CUPID 重新请求（不计入重试次数）
                    print("使用新 CUPID 重新请求...")
                    response = requests.get(url, cookies=cookies, timeout=30)
                    html = response.text

                    # 再次检查验证，如果还需要验证则继续重试
                    if 'toNumbers' in html:
                        print("⚠ 更新 CUPID 后仍需验证，继续重试...")
                        continue
                else:
                    print("❌ 未能提取到 abc 参数")
                    if attempt <= max_retries:
                        print(f"等待 2 秒后重试...")
                        time.sleep(2)
                        continue
                    return None

            # 验证通过，解析数据
            print("✓ 验证通过，开始解析数据...")
            soup = BeautifulSoup(html, "lxml")
            break

        except requests.exceptions.RequestException as e:
            print(f"❌ 请求 URL 失败：{e}")
            if attempt <= max_retries:
                print(f"等待 2 秒后重试...")
                time.sleep(2)
            continue
        except Exception as e:
            print(f"❌ 解析数据时发生未知错误：{e}")
            if attempt <= max_retries:
                print(f"等待 2 秒后重试...")
                time.sleep(2)
            continue
    return soup

if __name__ == "__main__":
    url = "https://www.firstsilicon.co.kr/index.php"
    soup = get_soup(url)
    # print(soup.prettify())

    inner_left_box = soup.find("ul", class_="inner_left_box")
    # print(inner_left_box.prettify())
    category_list = []
    if inner_left_box:
        lis = inner_left_box.find_all("li")
        for li in lis:
            level_1 = li.text.strip()
            data_code = li.attrs["data-code"].strip()
            levle_url = f"https://www.firstsilicon.co.kr/theme/daontheme_pro10/html/business/04.php?cate_id={data_code}"
            soup = get_soup(levle_url)
            inner_right_box = soup.find("ul", class_="inner_right_box")
            if inner_right_box:
                right_lis = inner_right_box.find_all("li")
                for right_li in right_lis:
                    a_tag = right_li.find("a")
                    levle_2 = right_li.text.strip()
                    href = a_tag.attrs["href"].strip()
                    if href:
                        category_list.append({
                            "url": href,
                            "category": f"{level_1}^{levle_2}"
                        })



    print(json.dumps(category_list, indent=2,ensure_ascii=False))
    with open("firstsilicon.json", "w", encoding="utf-8") as f:
        json.dump(category_list, f, indent=2, ensure_ascii=False)