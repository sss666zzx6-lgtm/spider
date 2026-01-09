import json
import os
import requests
from requests.compat import urljoin

base_url = "https://www.st.com"

headers = {
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}

url = "https://www.st.com/bin/st/top_menu.en.json"
response = requests.get(url, headers=headers)
items = response.json()["products"]["items"]
# print(json.dumps(items, indent=4, ensure_ascii=False))



result_list = []
def extract_last_layer(node, current_category):
    """
    递归遍历节点，提取最后一层的url和层级category
    :param node: 当前遍历的节点
    :param current_category: 已拼接的层级路径（初始为空）
    """
    # 获取当前节点的标题（用titleEn保证一致性）
    node_title = node.get("titleEn", "")
    # 拼接层级路径（初始为空时直接用当前标题，否则用^连接）
    new_category = f"{current_category}^{node_title}" if current_category else node_title
    # 获取当前节点的子节点
    children = node.get("children", [])

    # 终止条件：子节点为空 → 是最后一层，收集数据
    if not children:
        url = urljoin(base_url, node.get("url", ""))
        result_list.append({
            "url": url,
            "category": new_category
        })
    # 递归处理子节点
    else:
        for child in children:
            extract_last_layer(child, new_category)


# 遍历顶层节点，启动递归
for top_node in items:
    extract_last_layer(top_node, "")

# 打印结果（可根据需要保存为JSON/其他格式）
if __name__ == "__main__":
    print(json.dumps(result_list, indent=4, ensure_ascii=False))

    base_path = "./seed_json"
    file_path = os.path.join(base_path, "stm.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result_list, f, indent=2, ensure_ascii=False)
    print(f"\n共提取到 {len(result_list)} 条最后一层数据")