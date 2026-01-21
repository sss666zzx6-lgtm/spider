import os
import time
import requests
import json

from bs4 import BeautifulSoup

url = "https://www.sg-micro.com"

response = requests.get(url)

# print(response.text)

def bulid_url():
    soup = BeautifulSoup(response.text, 'lxml')
    result = []

    main_divs = soup.select(r'div.grid.grid-cols-1.gap-4.md\:grid-cols-2 > div')

    for main_div in main_divs:
        # 提取一级分类名称
        level1_name = main_div.find('div', class_='bg-primary').get_text(strip=True)
        # 构造一级分类的URL（根据二级URL规律推导）
        level1_url = f"{url}/products/{level1_name.lower().replace(' ', '-')}"

        # 初始化一级分类字典
        level1_item = {
            "url": level1_url,
            "familyName": level1_name,
            "level": 1,
            "children": []
        }

        # 找到当前一级分类下的所有二级分类li元素
        level2_li_list = main_div.select('ul.grid-cols-2 > li')

        for li in level2_li_list:
            # 提取a标签
            a_tag = li.find('a')
            if not a_tag:
                continue

            # 提取二级分类URL
            level2_url = url + a_tag.get('href', '').strip()
            # 提取二级分类名称（优先用title属性，避免文本中的格式问题）
            level2_name = a_tag.get('title', '').strip()
            # 处理特殊字符（&amp; 转 &）
            level2_name = level2_name.replace('&amp;', '&')

            # 构造二级分类字典
            level2_item = {
                "url": level2_url,
                "familyName": level2_name,
                "level": 2,
                "children": []
            }

            # 添加到一级分类的children中
            level1_item['children'].append(level2_item)

        # 将一级分类添加到结果列表
        result.append(level1_item)
    return result


def fetch_level2_urls(category_result: list):
    # level2_relative_urls = []
    # for level1 in category_result:
    #     for level2 in level1['children']:
    #         if level2['level'] == 2 and level2['url'].strip():
    #             level2_relative_urls.append(level2['url'].strip())
    #
    # print(f"共筛选出 {len(level2_relative_urls)} 个level=2的URL")

    for level1_item in category_result:
        # 遍历二级分类（直接关联原对象，方便填充children）
        for level2_item in level1_item['children']:
            level2_url = level2_item['url'].strip()
            if not level2_url:
                print(f"跳过空URL的二级分类：{level2_item['familyName']}")
                continue
            try:
                response = requests.get(url=level2_url)

                if response.status_code == 200:
                    # print(f"请求成功")
                    print(f"请求成功：{level2_item['familyName']}")
                    # response.encoding = response.apparent_encoding or 'utf-8'
                    soup = BeautifulSoup(response.text, 'lxml')
                    # 匹配目标div（三级分类容器）
                    target_div = soup.select_one(
                        r'div.grid.grid-cols-1.gap-x-10.gap-y-2.md\:grid-cols-2.md\:gap-y-4.lg\:grid-cols-3.lg\:gap-x-4'
                    )
                    if target_div:
                        # 提取所有a标签并构建三级分类
                        level3_list = []
                        a_tags = target_div.find_all('a')
                        for a in a_tags:
                            # 提取三级分类URL和名称
                            level3_href = a.get('href', '').strip()
                            level3_url = f"{url}{level3_href}" if level3_href else ""
                            # 优先用title，无则用文本
                            level3_name = a.get('title', '').strip() or a.get_text(strip=True)

                            if level3_url and level3_name and level3_name != "Automotive Grade":  # 过滤空数据
                                level3_item = {
                                    "url": level3_url,
                                    "familyName": level3_name,
                                    "level": 3,
                                    "children": []
                                }
                                level3_list.append(level3_item)
                        # 填充到二级分类的children中
                        level2_item['children'] = level3_list
                        print(f"  └─ 提取到 {len(level3_list)} 个三级分类")
                    else:
                        print(f"  └─ 未找到三级分类容器")
                else:
                    print(f"请求失败：HTTP状态码 {response.status_code}")
            except Exception as e:
                print(f"请求失败：未知错误 - {str(e)[:50]}")

            time.sleep(1)

    return category_result


def extract_leaf_nodes(category_tree: list) -> list:
    """
    递归遍历分类树，提取所有叶子节点（children为空的节点）
    :param category_tree: 完整的分类树（final_category_tree）
    :return: 叶子节点列表，格式为 [{"url": "", "category": ""}, ...]
    """
    leaf_nodes = []  # 存储最终叶子节点结果

    def recursive_traverse(node, parent_path: list):
        """
        递归遍历单个节点
        :param node: 当前遍历的节点（一级/二级/三级）
        :param parent_path: 父层级的名称列表（用于拼接category）
        """
        # 1. 拼接当前节点的名称到路径中
        current_path = parent_path + [node['familyName']]

        # 2. 判断是否是叶子节点（children为空）
        if not node['children']:  # children为空列表 → 叶子节点
            leaf_node = {
                "url": node['url'],
                "category": "^".join(current_path)  # 用^拼接层级名称
            }
            leaf_nodes.append(leaf_node)
        else:  # 非叶子节点 → 递归遍历子节点
            for child in node['children']:
                recursive_traverse(child, current_path)

    # 3. 遍历所有一级节点，启动递归
    for level1_node in category_tree:
        recursive_traverse(level1_node, parent_path=[])

    return leaf_nodes

if __name__ == "__main__":
    result_list = bulid_url()
    print(json.dumps(result_list, indent=4, ensure_ascii=False))

    final_category_tree  = fetch_level2_urls(result_list)

    leaf_nodes = extract_leaf_nodes(final_category_tree)

    base_path = "./seed_json"
    file_path = os.path.join(base_path, "sg_micro.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(leaf_nodes, f, indent=2, ensure_ascii=False)