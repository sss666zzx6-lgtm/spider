
import time
import requests
from bs4 import BeautifulSoup
import json
import re
from common.utils.logger import get_logger

logger = get_logger("product-parse")

brand = "矽力杰"
country = "中国"
ds = "官网"
BASE_URL = "https://www.silergy.com"

def product_status(raw_status: str | None) -> str:

    status_mapping = {
        "预发布": "新产品",
        "正在供货": "量产",
        "正在量产": "量产",
        # "not recommended for new designs": "不推荐新设计",
        # "last time buy": "最后购买",
        # "obsolete": "停产",
    }
    if not raw_status:
        return "未知状态"

    key = raw_status.strip().lower()
    return status_mapping.get(key, "未知状态")

def request_get(url):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        # response.encoding = response.apparent_encoding
        return response

    except Exception as e:
        print(f"解析数据时发生未知错误：{e}")


def traverse_node(tree_list, sup="\n"):
    datas = []
    for td in tree_list:
        td_texts = td.get_text()
        td_texts = [i.strip() for i in td_texts if i.strip()]
        td_text = "".join(td_texts)
        datas.append(td_text)
    return f"{sup}".join(datas)

def parse_product_detail(url:str,ppn: str, application_level: str=None,category: str=None,
                         datasheet_id:str=None):
    fieldMap = dict()
    type = "PPN"

    # product = {}
    datasheets = []
    papers = []
    order_devices = []
    order_device = {}
    product = {
        "brand": brand,
        "country": country,
        "ds": ds,
        "product_number": ppn
    }
    order_device["order_device_number"] = ppn
    if category:
        product["category"] = category

    if application_level:
        order_device["application_level"] = [application_level]
        product["application_level"] = [application_level]
        logger.info(order_device["application_level"])

    response = request_get(url)
    if not response:
        logger.info(f"PPN[{ppn}] 请求失败，返回基础数据")
        return None
    soup = BeautifulSoup(response.text, "lxml")
    tooltip_div = soup.find("div", class_="tooltip")
    if tooltip_div:
        status = tooltip_div.get_text().strip()
        if status:
            product["status"] = product_status(status)
            order_device["status"] = product_status(status)
            # print(product["status"])
            logger.info(product_status(status))

    title_div = soup.find(
        "div",
        attrs={"style": re.compile(r"^max-height", re.I)}
    )
    if title_div:
        title = title_div.get_text().strip()
        product["title"] = title
        # print(title)
        logger.info(title)

    # datasheet_div = soup.find(
    #     "div",
    #     attrs={"style": re.compile(r"display:\s*inline-block;float:\s*right;.*position:\s*absolute", re.I)}
    # )
    #
    # # 3. 提取a标签的href属性（关键：判空防护，避免None报错）
    # href = ""
    # if datasheet_div:
    #     # 从div中找到第一个a标签
    #     a_tag = datasheet_div.find("a")
    #     if a_tag and a_tag.has_attr("href"):
    #         # 提取href属性值，strip()去除可能的首尾空格
    #         href = a_tag["href"].strip()
    #
    # raw_path = BASE_URL + href
    # if "id" in raw_path:
    #     result = {"raw_path":raw_path}
    #     logger.info(result)
    #     datasheets.append(result)

    if datasheet_id:
        raw_path = f"https://www.silergy.com/download/downloadFile?id={datasheet_id}&type=product&ftype=note"
        result = {"raw_path": raw_path}
        logger.info(result)
        datasheets.append(result)

    params_div = soup.find("div", id="parameters")

    temp_min = None
    temp_max = None
    if params_div:
        # 找到表格的所有行（tr）
        tr_list = params_div.find_all("tr")
        for tr in tr_list:
            # 提取th（参数名）和td（参数值）的文本，去空格
            th_text = tr.find("th").get_text(strip=True)
            td_text = tr.find("td").get_text(strip=True)

            # 匹配“封装”参数
            if th_text == "Package":
                package = td_text
                if package:
                    order_device["package_type"] = package
                    logger.info(package)

            # 匹配“工作温度范围”参数
            elif th_text == "Operating temperature range(°C)":
                if td_text:  # 确保温度值非空
                    try:
                        # 拆分温度（格式："-40 to 125" → 拆分成["-40", "125"]）
                        temp_parts = td_text.split(" to ")
                        # 转换为int（保留负号）
                        temp_min = int(temp_parts[0].strip())
                        temp_max = int(temp_parts[1].strip())
                        logger.info("最低温度：%d °C，最高温度：%d °C", temp_min, temp_max)
                    except (IndexError, ValueError) as e:
                        # 处理格式异常（比如不是"x to y"、无法转int）
                        logger.info(f"温度格式解析失败：{td_text}，错误：{e}")
                        temp_min = None
                        temp_max = None

    if temp_min:
        order_device["min_operation_temp"] = temp_min
    if temp_max:
        order_device["max_operation_temp"] = temp_max

    features_div = soup.find("div", id="features")
    if not features_div:
        logger.info(f"PPN[{ppn}]未找到id=features的div")

    if features_div:
        ul = features_div.find("ul")
        if not ul:
            logger.info(f"PPN[{ppn}] features div内未找到ul标签")
        if ul:
            li_list = ul.find_all("li")
            feature = traverse_node(li_list)
            # print(feature)
            product["feature"] = feature
    else:
        logger.info(f"PPN[{ppn}] 未找到id=features的div")

    doc_div = soup.find("div", id="other_file")
    if not doc_div:
        logger.info(f"PPN[{ppn}] 未找到id=other_file的div")

    if doc_div:
        tr_list = doc_div.find_all("tr")
        for i in range(1, len(tr_list)):
            tr = tr_list[i]
            item = {}

            # 提取a标签相关信息（有值才加字段）
            a_tag = tr.find('a')
            if a_tag:
                # 提取标题：文本非空才添加title字段
                title = a_tag.get_text(strip=True)
                if title:  # 过滤空文本（比如a标签只有空格的情况）
                    item['name'] = title

                # 提取href：属性值非空才添加href字段
                href = a_tag.get('href')
                if href:
                    doc_raw_path = BASE_URL + href
                    item['raw_path'] = doc_raw_path

            td_list = tr.find_all('td')
            if len(td_list) >= 2:
                date_str = td_list[1].get_text(strip=True)
                if date_str:
                    try:
                        date_timestamp = int(time.mktime(time.strptime(date_str, "%Y-%m-%d")))
                        item['date'] = date_timestamp
                    except (ValueError, IndexError) as e:
                        logger.info(f"PPN[{ppn}] 文档日期解析失败：{date_str}，错误：{str(e)}")
            papers.append(item)


    if order_device:
        order_devices.append(order_device)
        fieldMap["order_devices"] = order_devices
    fieldMap["type"] = type
    fieldMap["product"] = product
    if datasheets:
        fieldMap["datasheets"] = datasheets
    if papers:
        fieldMap["papers"] = papers

    if datasheets:
        return fieldMap
    else:
        return None


if __name__ in "__main__":
    product_url = "https://www.silergy.com/productsview/SY8884ADFC"
    ppn = "SY8884ADFC"
    application_level = "车规级"
    fieldMap = parse_product_detail(product_url, ppn, application_level,category="5555")
    print(json.dumps(fieldMap, indent=4,ensure_ascii=False))