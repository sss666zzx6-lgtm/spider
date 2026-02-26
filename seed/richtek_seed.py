import os

import requests
import time
import json
from bs4 import BeautifulSoup
from requests.compat import urljoin
import re
from util.create_darwin_api import create_api

# 基础配置
base_url = "https://www.richtek.com/"



# 第一步：获取所有产品分类的 URL（复用之前的逻辑）
def get_product_urls():
    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()  # 触发HTTP错误（如404/500）
        soup = BeautifulSoup(response.text, "lxml")

        target_section = soup.find("section", id="main_0_v2_0_h1_0_SubMenu_MenuLevel2_0_section_0")
        if not target_section:
            print("未找到目标section")
            return None

        a_tags = target_section.find("ul").find_all("a")
        product_tree = []
        for a in a_tags:
            item = {
                "familyName": a.get_text(strip=True),
                "level": "1",
                "url": urljoin(base_url, a.get("href")),
                "children": []
            }
            product_tree.append(item)

        result = {"ProductTree": product_tree}
        return result
    except Exception as e:
        print(f"获取产品URL失败：{e}")
        return None


def crawl_product_pages(result):
    if not result or "ProductTree" not in result:
        print("无有效URL可遍历")
        return

    for item in result["ProductTree"]:
        family_name = item["familyName"]
        url = item["url"]

        try:
            time.sleep(2)
            response = requests.get(url, timeout=15)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "lxml")

                children = []
                # 定位所有包含目标内容的col容器
                col_divs = soup.find_all("div", class_="col mb-4")
                for col in col_divs:
                    # 1. 提取h5标签文本（备用）
                    h5_tag = col.find("h5", class_="card-title font-weight-bold")
                    if not h5_tag:
                        continue
                    h5_family_name = h5_tag.get_text(strip=True)

                    # 2. 提取当前卡片下的所有按钮并判断数量
                    btn_tags = col.find_all("button", class_="cus-btn btn-sm my-1 btn-primary")
                    btn_count = len(btn_tags)
                    if btn_count == 0:  # 无按钮跳过
                        continue

                    if btn_count >= 2:  # 多个按钮：嵌套层级
                        # 构造h5对应的父项（level2，无URL）
                        h5_item = {
                            "familyName": h5_family_name,
                            "level": "2",
                            "url": "",
                            "children": []
                        }
                        # 遍历按钮，作为h5项的子项（level3）
                        for btn_tag in btn_tags:
                            if not btn_tag.has_attr("onclick"):
                                continue
                            onclick_str = btn_tag["onclick"].replace("&quot;", '"')
                            url_match = re.search(r'window\.open\("(.*?)"\)', onclick_str)
                            if not url_match:
                                continue
                            full_url = urljoin(base_url, url_match.group(1))
                            # 按钮子项
                            btn_child_item = {
                                "familyName": btn_tag.get_text(strip=True),
                                "level": "3",
                                "url": full_url
                            }
                            h5_item["children"].append(btn_child_item)
                        # 加入一级项children
                        children.append(h5_item)

                    else:  # 单个按钮：保留原有逻辑（老样子）
                        btn_tag = btn_tags[0]  # 取唯一的按钮
                        if not btn_tag.has_attr("onclick"):
                            continue
                        onclick_str = btn_tag["onclick"].replace("&quot;", '"')
                        url_match = re.search(r'window\.open\("(.*?)"\)', onclick_str)
                        if not url_match:
                            continue
                        full_url = urljoin(base_url, url_match.group(1))
                        # 老逻辑：按钮文本为familyName，level=2，带URL
                        child_item = {
                            "familyName": h5_family_name,
                            "level": "2",
                            "url": full_url
                        }
                        children.append(child_item)

                item["children"] = children

                total_btn = 0
                for child in children:
                    if "children" in child:  # 嵌套项统计按钮数
                        total_btn += len(child["children"])
                    else:  # 单按钮项统计1个
                        total_btn += 1
                print(f"✅ {family_name} 提取到 {len(children)} 个二级项，共 {total_btn} 个按钮子项")

            else:
                print(f"❌ 请求失败，状态码：{response.status_code}")

        except Exception as e:
            print(f"❌ 未知错误：{e}")


def extract_final_urls(result):
    """
    提取所有最后一层的URL，并拼接路径上的familyName为category（用^分隔）
    :param result: 包含ProductTree的层级字典
    :return: 列表，每个元素为{"url": 最后一层URL, "category": 拼接后的分类路径}
    """
    final_url_list = []

    # 递归遍历节点的内部函数
    def traverse_node(node, path):
        # 拼接当前节点的familyName到路径
        current_path = path + [node["familyName"]]

        # 判断是否是最后一层：无children 或 children为空，且url非空
        if not node.get("children", []) and node.get("url", "").strip():
            # 拼接category（路径用^连接）
            category = "^".join(current_path)
            final_url_list.append({
                "url": node["url"],
                "category": category
            })
            return

        # 非最后一层，递归遍历children
        for child in node.get("children", []):
            traverse_node(child, current_path)

    # 遍历一级节点（ProductTree）
    for root_node in result.get("ProductTree", []):
        traverse_node(root_node, path=[])

    return final_url_list

# 主程序执行
if __name__ == "__main__":
    result = get_product_urls()
    if result:
        crawl_product_pages(result)

        # print(json.dumps(result, indent=2, ensure_ascii=False))

        seed= extract_final_urls(result)
        base_path = "./seed_json"
        # if not os.path.exists(base_path):
        #     os.makedirs(base_path)
        file_path = os.path.join(base_path, "richtek.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(seed, f, indent=2, ensure_ascii=False)

        # print(json.dumps(seed, indent=2, ensure_ascii=False))
        # print(len(seed))
