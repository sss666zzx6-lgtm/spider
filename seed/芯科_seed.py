import requests
from bs4 import BeautifulSoup
import re,json,os


def extract_three_four_categories(result, base_domain="https://www.silabs.com"):
    """
    遍历result中的二级分类URL，解析页面提取三级/四级分类
    核心规则：
    - 仅提取四级分类（有四级才保留，无四级则只留原二级）
    - 无table/tbody/四级行时，一律保留原二级分类，舍弃三级
    - 无三级分类名的container：第一个保留二级，非第一个跳过
    :param result: 二级分类列表，元素格式{"url": "", "category": "一级^二级"}
    :param base_domain: 基础域名，用于补全四级URL
    :return: 更新后的列表，仅包含二级/四级分类（无三级分类）
    """
    final_result = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/144.0.0.0 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": base_domain
    }

    for idx, item in enumerate(result):
        second_url = item["url"]
        second_category = item["category"]  # 原始二级分类：一级^二级
        print(f"正在处理第 {idx + 1}/{len(result)} 条：{second_category} | URL: {second_url}")

        # 容错：跳过空URL
        if not second_url:
            final_result.append(item)
            print(f"跳过空URL条目：{second_category}")
            continue

        # 标记：是否已为当前二级分类添加过二级条目（避免重复）
        has_added_second = False

        try:
            response = requests.get(second_url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")

            table_containers = soup.find_all("div", class_="table-container")
            if not table_containers:
                # 无table-container，直接保留原二级
                final_result.append(item)
                has_added_second = True
                print(f"未找到table-container，保留二级分类：{second_category}")
                continue

            # ========== 核心修改：遍历container时记录索引 ==========
            for container_idx, container in enumerate(table_containers):
                # 提取三级分类名（仅用于四级拼接，无四级则舍弃）
                title_tag = container.find("div", class_="pftable-title")

                # 无三级分类名的判断逻辑（新增索引判断）
                if not title_tag:
                    print(f"跳过无标题的table-container：{second_category}（索引：{container_idx}）")
                    # 是第一个container → 保留原二级
                    if container_idx == 0 and not has_added_second:
                        final_result.append(item)
                        has_added_second = True
                        print(f"第一个container无三级分类名，保留原二级分类：{second_category}")
                    # 不是第一个 → 按原逻辑跳过
                    continue

                # 清理三级分类名（仅用于四级拼接）
                columns_link = title_tag.find("a", class_="columns-link")
                if columns_link:
                    columns_link.decompose()
                three_category = title_tag.get_text(strip=True)
                three_category = ' '.join(three_category.split())
                if three_category and three_category[-1].isdigit():
                    three_category = three_category[:-1].rstrip()
                if not three_category:
                    print(f"三级分类名为空，跳过该container：{second_category}（索引：{container_idx}）")
                    # 是第一个container → 保留原二级
                    if container_idx == 0 and not has_added_second:
                        final_result.append(item)
                        has_added_second = True
                        print(f"第一个container三级分类为空，保留原二级分类：{second_category}")
                    # 不是第一个 → 跳过
                    continue

                # 未找到table → 保留原二级（第一个/非第一个都保留，但仅添加一次）
                table = container.find("table", class_="pftable")
                if not table:
                    print(f"table-container中未找到table：{second_category} → {three_category}（索引：{container_idx}）")
                    if not has_added_second:
                        final_result.append(item)
                        has_added_second = True
                        print(f"保留原二级分类：{second_category}")
                    continue

                # 未找到tbody → 保留原二级
                tbody = table.find("tbody")
                if not tbody:
                    print(f"table中未找到tbody：{second_category} → {three_category}（索引：{container_idx}）")
                    if not has_added_second:
                        final_result.append(item)
                        has_added_second = True
                        print(f"保留原二级分类：{second_category}")
                    continue

                # 查找所有tr并过滤空行
                tr_list = tbody.find_all("tr")
                tr_list = [tr for tr in tr_list if tr.get_text(strip=True)]

                # 无四级行 → 保留原二级
                if not tr_list:
                    print(f"无四级分类行：{second_category} → {three_category}（索引：{container_idx}）")
                    if not has_added_second:
                        final_result.append(item)
                        has_added_second = True
                        print(f"保留原二级分类：{second_category}")
                    continue

                # 有四级行时，提取四级分类
                for tr in tr_list:
                    sticky_col = tr.find("td", class_="sticky-col")
                    if not sticky_col:
                        continue
                    four_a_tag = sticky_col.find("a", href=True)
                    if not four_a_tag:
                        continue

                    four_category = four_a_tag.get_text(strip=True)
                    four_url_path = four_a_tag["href"]
                    four_url = base_domain + four_url_path if four_url_path.startswith("/") else four_url_path

                    if not four_category or not four_url:
                        continue

                    # 拼接完整分类（一级^二级^三级^四级）
                    full_category = f"{second_category}^{three_category}^{four_category}"
                    final_result.append({
                        "url": four_url,
                        "category": full_category
                    })
                    print(f"提取四级分类：{full_category} | URL: {four_url}")
                    # 提取到四级则标记无需再添加二级
                    has_added_second = True

        except requests.exceptions.RequestException as e:
            # 请求失败 → 保留原二级
            final_result.append(item)
            print(f"请求失败，保留原条目：{second_category} | 错误：{str(e)}")
        except Exception as e:
            # 解析失败 → 保留原二级
            final_result.append(item)
            print(f"解析失败，保留原条目：{second_category} | 错误：{str(e)}")

    return final_result

def extract_category_url(soup,id):
    wireless_a = soup.find(id=id)

    if wireless_a:
        parent_div = wireless_a.parent

        # 4. 找到父元素的下一个兄弟节点（目标div.nav-items-cols）
        # next_sibling会包含空白字符，用find_next_sibling过滤标签类型
        target_div = parent_div.find_next_sibling("div", class_="nav-items-cols")

        if target_div:
            print(f"找到{id}目标div：")
            # print(target_div)
            return target_div
        else:
            print("未找到class='nav-items-cols'的div")
    else:
        print(f"未找到id={id}的a标签")


def extract_second_categories(target_div, first_category):
    """
    从target_div中提取二级分类的url和拼接后的category
    :param target_div: BeautifulSoup的Tag对象（class="nav-items-cols"的div）
    :param first_category: 一级分类名，默认是Wireless
    :return: 列表，每个元素是{"url": "", "category": "一级^二级"}格式的字典
    """
    # 初始化结果列表
    result = []

    # 容错：如果target_div为空，直接返回空列表
    if not target_div:
        print("警告：target_div为空，未提取到二级分类")
        return result

    # 1. 找到target_div内所有带nav-item-title类的a标签（精准匹配二级分类的a标签）
    second_category_a_tags = target_div.find_all(
        "a",
        class_="nav-item-title",  # 筛选指定类的a标签，避免匹配无关a标签
        href=True  # 只提取有href属性的a标签
    )

    # 2. 遍历每个二级分类的a标签，提取信息
    for a_tag in second_category_a_tags:
        # 提取二级分类名称：去除首尾空格、换行符等空白字符
        second_category = a_tag.get_text(strip=True)
        # 提取URL：保留原始href（若需补全域名，可在这里拼接，比如 + "https://xxx.com"）
        second_url = a_tag["href"]

        # 容错：跳过空的二级分类名称/url
        if not second_category or not second_url:
            continue

        # 拼接category：一级^二级
        full_category = f"{first_category}^{second_category}"

        # 构造指定格式的字典，添加到结果列表
        result.append({
            "url": "https://www.silabs.com" + second_url,
            "category": full_category
        })

    return result

if __name__ == '__main__':
    url = "https://www.silabs.com/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    non_wireless_target_div = extract_category_url(soup,"NonWireless")
    wireless_target_div = extract_category_url(soup,"Wireless")

    wireless_result = extract_second_categories(wireless_target_div,first_category="Wireless")

    # print(json.dumps(wireless_result, ensure_ascii=False, indent=4))

    non_wireless_result = extract_second_categories(non_wireless_target_div,first_category="Non-Wireless")

    # print(json.dumps(non_wireless_result, ensure_ascii=False, indent=4))
    print(len(non_wireless_result))
    print(len(wireless_result))

    result = wireless_result + non_wireless_result
    for item in result:
        if item["url"] == "https://www.silabs.com/sensors":
            item["url"] = "https://www.silabs.com/sensors/magnetic"
            item["category"] += "^Magnetic Sensors"
            print(item["category"],item["url"])

        if item["url"] == "https://www.silabs.com/mcu":
            copy_category = item["category"]
            item["url"] = "https://www.silabs.com/mcu/32-bit-microcontrollers"
            item["category"] += "^Explore 32-bit MCUs"
            result.append({
                "url" : "https://www.silabs.com/mcu/8-bit-microcontrollers",
                "category": f"{copy_category}^Explore 8-bit MCUs"
            })
            print(item["category"],item["url"])
            print(copy_category)

    print(f"\n合并后的二级分类数量：{len(result)}")

    # 4. 提取三级/四级分类，更新列表
    final_result = extract_three_four_categories(result)


    print(json.dumps(final_result, ensure_ascii=False, indent=4))
    print(f"\n最终分类列表数量：{len(final_result)}")

    base_path = "./seed_json"
    file_path = os.path.join(base_path, "silabs.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(final_result, f, indent=2, ensure_ascii=False)





