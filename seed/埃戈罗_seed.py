import requests
from bs4 import BeautifulSoup
import json
import os

def parse_leaf_nodes(data, base_url="https://www.allegromicro.com"):
    leaf_nodes = []


    def _traverse(node, parent_categories=None):
        # 初始化父分类列表
        if parent_categories is None:
            parent_categories = []

        # 1. 处理一级父节点（ParentMainNode）
        if "ParentMainNode" in node:
            parent_main = node["ParentMainNode"]
            # 提取一级分类名称
            main_text = parent_main["LinkText"]
            main_url = parent_main["ItemUrl"]
            # 拼接一级分类路径
            new_categories = parent_categories + [main_text]

            # 处理二级节点（MenuSectionNodes）
            if "MenuSectionNodes" in node and node["MenuSectionNodes"] is not None:
                for section in node["MenuSectionNodes"]:
                    section_main = section["SectionMainNode"]
                    section_text = section_main["LinkText"]
                    section_url_path = section_main["ItemUrl"]
                    # 拼接二级分类路径
                    section_categories = new_categories + [section_text]

                    # 获取三级节点（SectionNodes）
                    section_nodes = section.get("SectionNodes")

                    # 情况1：有三级节点（列表且非空）→ 解析三级作为叶子节点
                    if section_nodes is not None and isinstance(section_nodes, list) and len(section_nodes) > 0:
                        for leaf in section_nodes:
                            leaf_text = leaf["LinkText"]
                            leaf_url_path = leaf["ItemUrl"]
                            full_url = f"{base_url}{leaf_url_path}"
                            full_category = "^".join(section_categories + [leaf_text])
                            leaf_nodes.append({
                                "url": full_url,
                                "category": full_category
                            })
                    # 情况2：无三级节点（None/空列表）→ 把二级节点本身作为叶子节点
                    else:
                        full_url = f"{base_url}{section_url_path}"
                        full_category = "^".join(section_categories)
                        leaf_nodes.append({
                            "url": full_url,
                            "category": full_category
                        })

    _traverse(data)
    return leaf_nodes


if __name__ == '__main__':
    url = "https://www.allegromicro.com/en/products"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup.prettify())

    products_a = soup.find('a', id='Products')
    target_div = None
    if products_a:
        for sibling in products_a.next_siblings:
            if sibling.name == 'div':
                target_div = sibling
                break

    li_elements = []
    if target_div:
        li_elements = target_div.find_all('li')

    level2_ids = []
    for li in li_elements:
        # 提取属性值：get方法更安全，属性不存在时返回None而非报错
        level2_id = li.get('data-level2-id')
        if level2_id:
            level2_ids.append(level2_id)
            print(f"提取到data-level2-id: {level2_id}")
    category_list = []
    for level2_id in level2_ids:
        data_url = f"https://www.allegromicro.com/all-api/getmegamenu?itemId={level2_id}"
        res = requests.get(data_url)
        if res.status_code == 200:
            print(f"正在解析{data_url}")
            data_dict = json.loads(res.json())
            data = parse_leaf_nodes(data_dict)
            category_list += data


    print(json.dumps(category_list, ensure_ascii=False,indent=4))

    base_path = "./seed_json"
    file_path = os.path.join(base_path, "allegromicro.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(category_list, f, indent=2, ensure_ascii=False)
