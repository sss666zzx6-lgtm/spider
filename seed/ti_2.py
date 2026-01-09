import os
import re
import time
import json
import requests


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://www.ti.com/product-category/clocks-timing/clock-buffers/overview.html",
    "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}

# 正则表达式：匹配destination-id="数字" 中的数字
DEST_ID_PATTERN = re.compile(r'destination-id="(\d+)"')


def extract_real_dest_id(url: str) -> str:
    """
    请求叶子节点原始URL，提取响应中的destination-id对应的数字ID
    :param url: 叶子节点的原始url
    :return: 提取到的数字ID，失败返回空字符串
    """
    if not url:  # 空URL直接返回
        print(f"❌ 原始URL为空，跳过")
        return ""

    modified_url = url.replace("overview.html", "products.html")
    print(f"🔄 URL替换：{url} → {modified_url}")

    try:
        # 发送请求（添加延迟，避免IP封禁）
        time.sleep(1)
        response = requests.get(modified_url, headers=headers,timeout=10)
        response.raise_for_status()  # 触发HTTP异常（404/500等）

        # 正则匹配destination-id="xxx"中的数字
        match = DEST_ID_PATTERN.search(response.text)
        if match:
            dest_id = match.group(1)
            print(f"✅ 从URL {url} 提取到destination-id: {dest_id}")
            return dest_id
        else:
            print(f"❌ URL {url} 响应中未找到destination-id")
            return ""

    except requests.exceptions.RequestException as e:
        print(f"❌ 请求URL {url} 失败：{str(e)}")
        return ""


def traverse_leaf_nodes(tree_data: list) -> list:
    """
    递归遍历树形数据，提取所有叶子节点的信息：原始url、层级category，再获取真实dest_id并拼接最终URL
    :param tree_data: ti.json加载后的树形数据
    :return: 最终的[{"url": 拼接后的API URL, "category": 层级字符串}]列表
    """
    final_result = []

    # 递归遍历节点的内部函数
    def recursive_traverse(node: dict, path: list):
        # 当前节点名称加入层级路径
        current_path = path + [node["familyName"]]

        # 判断是否是叶子节点
        if node.get("isLeaf") == "Y":
            # 1. 获取叶子节点原始URL
            original_url = node.get("url", "")
            # 2. 提取真实的destination-id
            real_dest_id = extract_real_dest_id(original_url)

            if real_dest_id:
                # 3. 拼接最终的API URL
                api_url = (
                    f"https://www.ti.com/selectionmodel/api/gpn/result-list"
                    f"?destinationId={real_dest_id}&destinationType=GPT&mode=parametric&locale=en-US"
                )
                # 4. 拼接category（层级用^分隔）
                category_str = "^".join(current_path)
                # 5. 添加到最终结果
                final_result.append({
                    "url": api_url,
                    "category": category_str
                })
        else:
            # 非叶子节点，递归处理子节点
            for child in node.get("children", []):
                recursive_traverse(child, current_path)

    # 遍历所有一级分类的树形结构
    for item in tree_data:
        # 取出一级分类名称和对应的树形结构（item是{分类名: [树形列表]}）
        for root_name, root_tree in item.items():
            # 遍历根节点下的所有节点
            for root_node in root_tree:
                recursive_traverse(root_node, path=[])

    return final_result


if __name__ == "__main__":
    base_path = "./seed_json"

    file_path = os.path.join(base_path, "ti.json")

    if not os.path.exists(file_path):
        print(f"❌ 文件不存在：{file_path}")
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            ti_json_data = json.load(f)

        # 2. 遍历叶子节点，提取真实dest_id并生成最终列表
        print("===== 开始处理叶子节点 =====")
        final_leaf_result = traverse_leaf_nodes(ti_json_data)

        base_path_2 = "./seed_json"
        file_path = os.path.join(base_path, "ti_seed.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(final_leaf_result, f, indent=2, ensure_ascii=False)

        print(f"✅ 成功提取到有效ID的叶子节点数量：{len(final_leaf_result)}")

        # 打印前3个结果示例
        if final_leaf_result:
            print(f"\n📊 结果示例（前3个）：")
            print(json.dumps(final_leaf_result[:3], indent=4, ensure_ascii=False))