from curl_cffi import requests
from bs4 import BeautifulSoup
import json
import re
from Crypto.Cipher import AES
import time

cookies = {
    "CUPID": "0650005feec44c466b1a7eeb83f4a63e",
    "PHPSESSID": "b907a86f086eb30f23c98e577807afd6",
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


def extract_product_info(product_table):
    """
    从产品表格中提取 Part No、Package 文本、Data Sheet 下载链接
    :param product_table: BeautifulSoup 解析后的 table 对象（class=scrolltable）
    :return: 列表，每个元素是字典：{"part_no": "", "package": "", "data_sheet_href": ""}
    """
    # 最终返回的产品信息列表
    product_list = []

    # -------------------------- 第一步：解析表头，获取目标列索引 --------------------------
    try:
        thead = product_table.find("thead")
        if not thead:
            print("⚠ 表格无 thead 部分")
            return product_list

        # 只取第一个 tr 表头
        first_tr = thead.find("tr")
        if not first_tr:
            print("⚠ 表头无第一个 tr")
            return product_list

        # 展开表头列名（处理 colspan，比如 Data Sheet 占 2 列）
        column_names = []
        ths = first_tr.find_all("th")
        for th in ths:
            # 提取表头文本（去空格）
            th_text = th.get_text(strip=True)
            # 获取跨列数（默认 1，Data Sheet 是 colspan=2）
            colspan = int(th.get("colspan", 1))
            # 按跨列数填充列名（比如 Data Sheet 添加 2 次）
            for _ in range(colspan):
                column_names.append(th_text)

        # 定位目标列索引（容错：不存在则设为 -1）
        part_no_idx = column_names.index("Part No") if "Part No" in column_names else -1
        package_idx = column_names.index("Package") if "Package" in column_names else -1
        data_sheet_idx = column_names.index("Data Sheet") if "Data Sheet" in column_names else -1

    except Exception as e:
        print(f"⚠ 解析第一个 tr 表头失败：{e}")
        return product_list

    # -------------------------- 第二步：遍历 tbody，提取产品数据 --------------------------
    try:
        tbody = product_table.find("tbody")
        if not tbody:
            print("⚠ 表格无 tbody 部分")
            return product_list

        rows = tbody.find_all("tr")
        for row in rows:
            tds = row.find_all("td")
            # 跳过列数不足的行
            if len(tds) < max(part_no_idx, package_idx, data_sheet_idx) + 1:
                continue

            # 提取 Part No（去除多余空格/换行）
            part_no = tds[part_no_idx].get_text(strip=True) if part_no_idx != -1 else ""

            # 提取 Package
            package = tds[package_idx].get_text(strip=True) if package_idx != -1 else ""

            # 提取 Data Sheet 的 href（a 标签的链接）
            data_sheet_href = ""
            if data_sheet_idx != -1 and len(tds) > data_sheet_idx:
                a_tag = tds[data_sheet_idx].find("a")
                if a_tag:
                    data_sheet_href = a_tag.get("href", "")

            # 添加到产品列表
            product_list.append({
                "part_no": part_no,
                "package": package,
                "data_sheet_href": data_sheet_href
            })

    except Exception as e:
        print(f"⚠ 解析 tbody 失败：{e}")
        return product_list

    return product_list


def parse_product_list(url, category, max_retries=4):
    """
    解析产品列表页
    :param url: 产品列表页 URL
    :param category: 产品分类
    :param max_retries: 最大重试次数（默认 2 次，即首次 1 次 + 重试 2 次 = 最多 3 次）
    :return: 产品数据列表
    """
    all_field = []
    attempt = 0  # 当前尝试次数

    while attempt <= max_retries:
        attempt += 1
        print(f"\n【第 {attempt}/{max_retries + 1} 次请求】{url}")

        try:
            response = requests.get(url, cookies=cookies, timeout=30,impersonate="chrome120")
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
                    response = requests.get(url, cookies=cookies, timeout=30,impersonate="chrome120")
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

            product_table = soup.find("table", class_="scrolltable")
            if product_table:
                products = extract_product_info(product_table)

                # 打印结果
                for idx, product in enumerate(products, 1):
                    print(f"产品{idx}:")
                    print(f"  Part No: {product['part_no']}")
                    print(f"  Package: {product['package']}")
                    print(f"  Data Sheet 链接：{product['data_sheet_href']}")

                    if product['data_sheet_href']:
                        fieldMap = {}
                        product_info = {}
                        datasheets = []
                        order_devices = []
                        ppn = product['part_no']
                        package_type = product['package']
                        datasheets.append({"raw_path": product['data_sheet_href']})

                        fieldMap["type"] = "PPN"
                        product_info["brand"] = "firstsilicon"
                        product_info["country"] = "韩国"
                        product_info["ds"] = "官网"
                        product_info["status"] = "量产"

                        product_info["category"] = category
                        if '-' in ppn:
                            prefix, suffix = ppn.split('-', 1)
                            print(f"横线前：{prefix}，横线后：{suffix}")
                            product_info["product_number"] = prefix
                            result = {}
                            result["order_device_number"] = ppn
                            result["status"] = "量产"
                            if package_type:
                                result["package_type"] = package_type
                            if result:
                                order_devices.append(result)
                        else:
                            product_info["product_number"] = ppn
                            print(f"❌ PPN {ppn} 不包含横线 '-',没有 OPN")

                        fieldMap["datasheets"] = datasheets
                        fieldMap["product"] = product_info
                        if order_devices:
                            fieldMap["order_devices"] = order_devices

                        all_field.append(fieldMap)
                    else:
                        print("没有规格书链接")

                    print("-" * 50)
            else:
                print("⚠ 未找到 product_table")

            # 解析成功，跳出重试循环
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

    return all_field


if __name__ == '__main__':

    url = "https://www.firstsilicon.co.kr/theme/daontheme_pro10/html/business/04.php?cate_id=0305"
    # url = "https://www.firstsilicon.co.kr/theme/daontheme_pro10/html/business/04.php?cate_id=0102"
    result_field = parse_product_list(url, category="d2222222222")

    print(f"\n共提取到 {len(result_field)} 个产品的 fieldMap：")
    for i, fm in enumerate(result_field):
        print(f"\n第{i + 1} 个产品的 fieldMap：")
        print(json.dumps(fm, ensure_ascii=False, indent=4))

    # a = "3c5e0b2da6592bbd8e9771f62b5803dd"  # key
    # b = "4bdeb14be32cfd1a3fb81fc171e8709a"  # iv
    # c = "b0d217259933cfd8e654a378c2235460"  # encrypted