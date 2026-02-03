import json
import os
import requests
import ceshi
from bs4 import BeautifulSoup
from requests.compat import urljoin


# -------------------------- 辅助函数 - 判断是否为产品列表页面 --------------------------
def is_product_table_page(li_elem):
    """
    判断某个<li>标签是否对应“产品列表页面”
    :param li_elem: bs4的<li>元素对象
    :return: True=是产品列表页面，False=非产品列表页面
    """
    # 1. 找“View Product Table”图标对应的a标签（icon-table类）
    table_icon_a = li_elem.find("a", class_="icon-table")
    if not table_icon_a:
        return False

    # 2. 检查图标a标签的href是否有效（非#，且包含/product-table/）
    table_href = table_icon_a.get("href", "").strip()
    if table_href == "#" or not table_href or "/product-table/" not in table_href:
        return False

    # 3. 检查图标a标签是否隐藏（有hidden/d-none → 非产品列表页面）
    a_classes = table_icon_a.get("class", [])
    if "hidden" in a_classes or "d-none" in a_classes:
        return False

    return True


# 基础配置
base_url = "https://www.infineon.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 获取页面内容（若用本地HTML，替换为：soup = BeautifulSoup(open("你的html文件.html", encoding="utf-8"), "lxml")）
response = requests.get(base_url, headers=headers, timeout=10)
response.raise_for_status()
soup = BeautifulSoup(response.text, "lxml")

# -------------------------- 第一步：提取一级分类 --------------------------
product_tree = []
first_level_li_list = soup.select(
    "div.firstCol.product-applications-icons ul.width_100 li.li_padding:not(.prosubLink0)[data-search-tag^='ifx:products/']"
)

for first_li in first_level_li_list:
    # 1. 一级基础信息
    label_elem = first_li.find(class_="labelText")
    if not label_elem:
        continue
    family_name = label_elem.get_text(strip=True)
    if not family_name:
        continue

    # 2. 一级target-id + URL（一级无产品列表判断）
    first_target_id = first_li.get("data-target-id", "")
    first_url = ""
    first_a_elem = first_li.find("a", class_="labelText")
    if first_a_elem and first_a_elem.get("href"):
        first_url = urljoin(base_url, first_a_elem.get("href"))

    # 3. 初始化一级字典
    first_category = {
        "familyName": family_name,
        "level": "1",
        "data-target-id": first_target_id,
        "url": first_url,
        "children": []
    }

    # -------------------------- 第二步：提取二级分类 --------------------------
    if first_target_id:
        second_level_div = soup.find("div", id=first_target_id, class_="secondColumn")
        if second_level_div:
            second_level_li_list = second_level_div.select("ul.width_100 li.li_padding.col2:not(.show_mobile)")

            for second_li in second_level_li_list:
                # 1. 二级基础信息
                second_label_elem = second_li.find(class_="labelText")
                if not second_label_elem:
                    continue
                second_family_name = second_label_elem.get_text(strip=True)
                if not second_family_name:
                    continue

                # 2. 二级target-id + URL（仅产品列表页面保存）
                second_target_id = second_li.get("data-target-id", "")
                second_url = ""
                if not second_target_id:
                    if is_product_table_page(second_li):
                        second_a_elem = second_li.find("a", class_="labelText")
                        if second_a_elem and second_a_elem.get("href"):
                            second_url = urljoin(base_url, second_a_elem.get("href"))

                # 3. 初始化二级字典
                second_category = {
                    "familyName": second_family_name,
                    "level": "2",
                    "data-target-id": second_target_id,
                    "url": second_url,
                    "children": []
                }

                # -------------------------- 第三步：提取三级分类 --------------------------
                third_level_div = None
                # 规则1：三级div.data-parent-id = 二级target-id
                if second_target_id:
                    third_level_div = soup.find(
                        "div",
                        class_="thirdCol",
                        attrs={"data-parent-id": second_target_id}
                    )
                # 规则2：三级div.data-parent-id = 一级target-id + 二级名称匹配
                if not third_level_div and first_target_id:
                    all_third_divs = soup.find_all(
                        "div",
                        class_="thirdCol",
                        attrs={"data-parent-id": first_target_id}
                    )
                    for div in all_third_divs:
                        second_title_elem = div.find("div", class_="mobileViewTitle secondLevelTitle")
                        if second_title_elem:
                            second_title_text = second_title_elem.get_text(strip=True)
                            if second_title_text == second_family_name:
                                third_level_div = div
                                break

                # 提取三级分类
                if third_level_div:
                    third_level_li_list = third_level_div.select("ul.width_100 li.li_padding:not(.show_mobile)")
                    for third_li in third_level_li_list:
                        third_label_elem = third_li.find(class_="labelText")
                        # 兼容第四层无a标签的情况（用span替代labelText）
                        if not third_label_elem:
                            third_label_elem = third_li.find("span", class_="labelText")
                        if not third_label_elem:
                            continue
                        third_family_name = third_label_elem.get_text(strip=True)
                        if not third_family_name:
                            continue

                        # 2. 三级target-id + URL（仅产品列表页面保存）
                        third_target_id = third_li.get("data-target-id", "")
                        third_url = ""
                        if not third_target_id:
                            if is_product_table_page(third_li):
                                # 兼容span包裹a标签的情况
                                third_a_elem = third_li.find("a", class_="labelText")
                                if third_a_elem and third_a_elem.get("href"):
                                    third_url = urljoin(base_url, third_a_elem.get("href"))

                        # 3. 初始化三级字典
                        third_category = {
                            "familyName": third_family_name,
                            "level": "3",
                            "data-target-id": third_target_id,
                            "url": third_url,
                            "children": []
                        }

                        # -------------------------- 关键新增：提取第四层分类 --------------------------
                        if third_target_id:
                            # 匹配第四层ul：id=三级target-id + class=fourthCategory
                            fourth_level_ul = soup.find(
                                "ul",
                                id=third_target_id,
                                # class_="fourthCategory"
                                attrs={"class": lambda x: x and "fourthCategory" in x.split()}
                            )
                            if fourth_level_ul:
                                # 提取第四层li：fourthlist + 排除show_mobile
                                fourth_level_li_list = fourth_level_ul.select("li.fourthlist:not(.show_mobile)")
                                for fourth_li in fourth_level_li_list:
                                    # 1. 第四层基础信息（兼容span/ a标签）
                                    fourth_label_elem = fourth_li.find("a", class_="labelText")
                                    if not fourth_label_elem:
                                        fourth_label_elem = fourth_li.find("span", class_="labelText")
                                    if not fourth_label_elem:
                                        continue
                                    fourth_family_name = fourth_label_elem.get_text(strip=True)
                                    if not fourth_family_name:
                                        continue

                                    # 2. 第四层target-id + URL（仅产品列表页面保存）
                                    fourth_target_id = fourth_li.get("data-target-id", "")
                                    fourth_url = ""
                                    if not fourth_target_id:
                                        if is_product_table_page(fourth_li):
                                            fourth_a_elem = fourth_li.find("a", class_="labelText")
                                            if fourth_a_elem and fourth_a_elem.get("href"):
                                                fourth_url = urljoin(base_url, fourth_a_elem.get("href"))

                                    # 3. 初始化第四层字典
                                    fourth_category = {
                                        "familyName": fourth_family_name,
                                        "level": "4",
                                        "data-target-id": fourth_target_id,
                                        "url": fourth_url,
                                        "children": []  # 预留第五层（如需可扩展）
                                    }
                                    # 将第四层加入三级children
                                    third_category["children"].append(fourth_category)

                        # 将三级分类加入二级children
                        second_category["children"].append(third_category)

                # 将二级分类加入一级
                first_category["children"].append(second_category)

    product_tree.append(first_category)

# -------------------------- 结果输出 --------------------------
result = {"ProductTree": product_tree}
print(f"✅ 提取到 {len(product_tree)} 个一级产品分类")
# 格式化输出（仅展示前2个一级分类，避免输出过长）
print(json.dumps(result, indent=4, ensure_ascii=False))



def build_url_category_list(categories, path_list, result_list):
    """
    递归遍历分类树，生成 {url:..., category:...} 格式的列表
    :param categories: 当前层级的分类列表
    :param path_list: 记录层级名称的路径（如 [一级名称, 二级名称]）
    :param result_list: 最终结果列表
    """
    for category in categories:
        # 1. 将当前分类名称加入路径
        current_name = category["familyName"].strip()
        path_list.append(current_name)

        # 2. 若当前分类有非空URL，生成category字符串并加入结果
        current_url = category.get("url", "").strip()
        if current_url:
            # 按1级^2级^3级拼接（路径列表直接用^连接）
            category_str = "^".join(path_list)
            result_list.append({
                "url": current_url,
                "category": category_str
            })

        # 3. 递归处理子分类
        if category.get("children"):
            build_url_category_list(category["children"], path_list, result_list)

        # 4. 回溯：移除当前分类名称，保证路径正确
        path_list.pop()


# 初始化结果列表
url_category_list = []
# 开始递归转换（从一级分类开始，初始路径为空）
build_url_category_list(result["ProductTree"], [], url_category_list)

print(f"✅ 生成 {len(url_category_list)} 条URL-分类记录")
for idx, item in enumerate(url_category_list, 1):
    print(f"{idx}. {json.dumps(item, ensure_ascii=False)}")

# base_path = "./seed_json"
# file_path = os.path.join(base_path, "infineon.json")
#
# with open(file_path, "w", encoding="utf-8") as f:
#     json.dump(url_category_list, f, indent=2, ensure_ascii=False)