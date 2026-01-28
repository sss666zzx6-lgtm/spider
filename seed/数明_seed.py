import os
import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse_category(head_pro_node, base_domain):
    """
    解析head_pro节点，提取叶子节点的URL和分类层级（修复连续^问题）
    :param head_pro_node: BeautifulSoup找到的.head_pro flexlf节点
    :param base_domain: 网站基础域名
    :return: 叶子节点列表，每个元素是{"url": "", "category": ""}
    """
    leaf_nodes = []

    # 遍历所有一级分类
    head_pli_list = head_pro_node.find_all("div", class_="head_pli")
    for head_pli in head_pli_list:
        # 提取一级分类名（过滤空值）
        first_level_a = head_pli.find("a", class_="tit")
        first_level_name = ""
        if first_level_a and first_level_a.find("span"):
            first_level_name = first_level_a.find("span").get_text(strip=True)

        # 遍历二级分类容器
        dec_box = head_pli.find("div", class_="decBox")
        if not dec_box:
            continue
        decli_list = dec_box.find_all("div", class_="decli")
        for decli in decli_list:
            # 提取二级分类名（过滤空值）
            second_level_name = ""
            second_level_a = decli.find("a", class_="link")
            if second_level_a:
                second_level_name = second_level_a.get_text(strip=True)

            # 查找叶子节点（.link1/.link2）
            dec_node = decli.find("div", class_="dec")
            if dec_node:
                # 遍历三级分类（叶子）
                leaf_a_list = dec_node.find_all("a", class_=["link1", "link2"])
                for leaf_a in leaf_a_list:
                    leaf_name = leaf_a.get_text(strip=True)
                    leaf_relative_url = leaf_a.get("href", "").strip()
                    if not leaf_relative_url or not leaf_name:
                        continue

                    # 关键修复：收集有效层级，过滤空值后拼接
                    category_levels = [
                        first_level_name,
                        second_level_name,
                        leaf_name
                    ]
                    # 过滤空字符串，再用^连接
                    valid_levels = [level for level in category_levels if level]
                    category = "^".join(valid_levels)

                    # 拼接绝对URL
                    leaf_url = urljoin(base_domain, leaf_relative_url)
                    leaf_nodes.append({
                        "url": leaf_url,
                        "category": category
                    })
            else:
                # 无三级分类，二级是叶子
                if second_level_a:
                    leaf_relative_url = second_level_a.get("href", "").strip()
                    if not leaf_relative_url:
                        continue

                    # 同样过滤空层级
                    category_levels = [first_level_name, second_level_name]
                    valid_levels = [level for level in category_levels if level]
                    category = "^".join(valid_levels)

                    leaf_url = urljoin(base_domain, leaf_relative_url)
                    leaf_nodes.append({
                        "url": leaf_url,
                        "category": category
                    })

    return leaf_nodes


if __name__ == "__main__":
    base_domain = "https://www.sillumin.com/"
    target_url = "https://www.sillumin.com/"  # 假设的目标URL，替换为实际地址
    try:
        response = requests.get(target_url, timeout=15)
        response.raise_for_status()
        # print(response.text)
        soup = BeautifulSoup(response.text, "lxml")
        head_pro_node = soup.find("div", class_="head_pro flexlf")
        if not head_pro_node:
            print("未找到class='head_pro flexlf'的节点")
        else:
            # 调用解析函数
            leaf_category_list = parse_category(head_pro_node, base_domain)
            print(json.dumps(leaf_category_list, indent=4, ensure_ascii=False))
            base_path = "./seed_json"
            file_path = os.path.join(base_path, "sillumin.json")

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(leaf_category_list, f, indent=2, ensure_ascii=False)




    except requests.exceptions.RequestException as e:
        print(f"❌ 请求URL失败：{str(e)}")
    except Exception as e:
        print(f"❌ 解析失败：{str(e)}")