# import requests
import time
from bs4 import BeautifulSoup
import json
from curl_cffi import requests
import re

def parse_product_leaf_nodes(product_category, base_url):
    """
    解析SEMICONDUCTORS分类下的叶子节点，返回指定格式的列表
    :param product_category: BeautifulSoup解析后的div#ulMobileProdMenu1节点
    :param base_url: 基础URL（用于拼接相对路径，如https://www.renesas.com）
    :return: 叶子节点列表，格式：[{"url": "", "category": ""}]
    """
    leaf_nodes = []
    # 1. 校验输入节点是否有效
    if not product_category:
        print("❌ 传入的product_category节点为空")
        return leaf_nodes

    # 2. 提取顶层分类名（SEMICONDUCTORS）
    top_category_ele = product_category.find("div", class_="vsh-mobile-menu-heading")
    if not top_category_ele:
        print("❌ 未找到顶层分类（vsh-mobile-menu-heading）")
        return leaf_nodes
    # 清理顶层分类文本（去除多余空格、换行、标签）
    top_category = re.sub(r'\s+', ' ', top_category_ele.get_text(strip=True)).strip()
    if not top_category:
        print("❌ 顶层分类文本为空")
        return leaf_nodes

    # 3. 遍历所有二级分类（vsh-accordion）
    accordion_list = product_category.find_all("div", class_="vsh-accordion")
    for accordion in accordion_list:
        # 3.1 提取二级分类名（span标签文本）
        second_span = accordion.find("span")
        if not second_span:
            continue
        second_category = re.sub(r'\s+', ' ', second_span.get_text(strip=True)).strip()
        if not second_category:
            continue

        # 3.2 找到二级分类下的内容容器（vsh-home-content）
        content_div = accordion.find("div", class_="vsh-home-content")
        if not content_div:
            continue

        # 3.3 遍历所有叶子节点（ul>li>a）
        leaf_a_list = content_div.find_all("ul")[-1].find_all("a")  # 确保取到ul下的所有a标签
        for a_tag in leaf_a_list:
            # 提取叶子节点文本（三级分类）
            leaf_text = re.sub(r'\s+', ' ', a_tag.get_text(strip=True)).strip()
            if not leaf_text:
                continue

            # 提取并拼接URL
            href = a_tag.get("href", "").strip()
            if not href:
                continue
            # 处理相对路径/绝对路径
            if href.startswith("/"):
                full_url = f"{base_url}{href}"
            elif href.startswith("http"):
                full_url = href
            else:
                full_url = f"{base_url}/{href}"

            # 拼接分类层级（顶层^二级^叶子）
            category_path = f"{top_category}^{second_category}^{leaf_text}"

            # 构造叶子节点字典并加入列表
            leaf_node = {
                "url": full_url,
                "category": category_path
            }
            leaf_nodes.append(leaf_node)
            print(f"✅ 新增叶子节点：{leaf_node}")

    return leaf_nodes


def update_leaf_nodes_with_deeper_levels(leaf_nodes, base_url, timeout=10):
    """
    遍历leaf_nodes中的URL，请求页面并解析Gateway_columnsWrap__1FSPR结构，更新分类层级（三级/四级）
    :param leaf_nodes: 原始叶子节点列表，格式[{"url": "", "category": ""}]
    :param base_url: 基础URL（用于拼接相对路径，如https://www.renesas.com）
    :param timeout: 请求超时时间（默认10秒）
    :return: 更新后的叶子节点列表
    """
    # 初始化更新后的节点列表
    updated_leaf_nodes = []
    # 请求头（模拟浏览器，避免被拦截）
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }

    # 遍历每个原始叶子节点
    for idx, node in enumerate(leaf_nodes):
        original_url = node.get("url", "")
        original_category = node.get("category", "")
        print(f"\n[{idx+1}/{len(leaf_nodes)}] 处理URL: {original_url}")

        # 跳过空URL
        if not original_url:
            updated_leaf_nodes.append(node)
            print("❌ URL为空，跳过")
            continue

        try:
            # 发起请求（加重试机制，避免网络波动）
            max_retries = 2
            response = None
            for retry in range(max_retries + 1):
                try:
                    response = requests.get(
                        original_url,
                        headers=headers,
                        timeout=timeout,
                        verify=False  # 忽略SSL证书验证（可选，根据实际情况调整）
                    )
                    response.raise_for_status()  # 抛出HTTP错误（4xx/5xx）
                    break
                except requests.exceptions.RequestException as e:
                    if retry == max_retries:
                        raise e
                    print(f"⚠️ 请求失败（重试{retry+1}/{max_retries}）：{str(e)}")
                    time.sleep(1)  # 重试前等待1秒

            # 解析页面
            soup = BeautifulSoup(response.text, "html.parser")
            # 查找目标div（Gateway_columnsWrap__1FSPR）
            target_div = soup.find("div", class_="Gateway_columnsWrap__1FSPR")

            # 情况1：未找到目标div → 保持原节点不变
            if not target_div:
                updated_leaf_nodes.append(node)
                print("ℹ️ 未找到Gateway_columnsWrap__1FSPR，保持原节点")
                continue

            # 情况2：找到目标div → 解析三级/四级分类
            # 存储解析出的深层节点
            deep_nodes = []
            # 遍历所有column（1of3/2of3/3of3）
            column_divs = target_div.find_all("div", class_=re.compile(r"Gateway_column\d+of3__"))
            for column in column_divs:
                # 提取三级分类名（dt标签文本）
                dt_tag = column.find("dt")
                third_category = ""
                if dt_tag:
                    third_category = re.sub(r'\s+', ' ', dt_tag.get_text(strip=True)).strip()
                    # 处理空dt（如第二个示例中的空dt）
                    third_category = third_category if third_category else "Uncategorized"

                # 提取四级节点（ul>li>a）
                li_list = column.find_all("li")
                for li in li_list:
                    a_tag = li.find("a")
                    if not a_tag:
                        continue

                    # 提取四级分类名（清理文本）
                    fourth_text = re.sub(r'\s+', ' ', a_tag.get_text(strip=True)).strip()
                    if not fourth_text:
                        continue

                    # 提取并拼接四级URL
                    fourth_href = a_tag.get("href", "").strip()
                    if fourth_href:
                        if fourth_href.startswith("/"):
                            fourth_url = f"{base_url}{fourth_href}"
                        elif fourth_href.startswith("http"):
                            fourth_url = fourth_href
                        else:
                            fourth_url = f"{base_url}/{fourth_href}"
                    else:
                        fourth_url = original_url  # 无href则复用原URL

                    # 拼接分类层级
                    # 规则：原分类^三级^四级（三级为空则原分类^四级）
                    if third_category and third_category != "Uncategorized":
                        new_category = f"{original_category}^{third_category}^{fourth_text}"
                    else:
                        new_category = f"{original_category}^{fourth_text}"

                    # 构造新节点
                    deep_node = {
                        "url": fourth_url,
                        "category": new_category
                    }
                    deep_nodes.append(deep_node)
                    print(f"✅ 解析出深层节点：{deep_node}")

            # 将解析出的深层节点加入结果（无深层节点则保留原节点）
            if deep_nodes:
                updated_leaf_nodes.extend(deep_nodes)
            else:
                updated_leaf_nodes.append(node)

        except Exception as e:
            # 捕获所有异常，避免单个URL失败导致整体中断
            updated_leaf_nodes.append(node)
            print(f"❌ 处理URL失败：{str(e)}，保留原节点")

    return updated_leaf_nodes


if __name__ == "__main__":


    url = "https://www.vishay.com/"
    base_url = "https://www.vishay.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"lxml")
    # print(response.text)

    product_category = soup.find("div",id="ulMobileProdMenu1")
    # print(product_category)

    leaf_nodes = parse_product_leaf_nodes(product_category, base_url)
    #
    # 5. 输出最终结果

    # print(json.dumps(leaf_nodes, indent=2, ensure_ascii=False))
    print(f"\n========== 解析完成 ==========")
    print(f"📊 共解析出 {len(leaf_nodes)} 个叶子节点")

    updated_nodes = update_leaf_nodes_with_deeper_levels(leaf_nodes, base_url)


    # print(json.dumps(updated_nodes, indent=2, ensure_ascii=False))
    print(f"📊 原始节点数：{len(leaf_nodes)}，更新后节点数：{len(updated_nodes)}")

    updated_nodes_2 = update_leaf_nodes_with_deeper_levels(updated_nodes, base_url)

    print(json.dumps(updated_nodes_2, indent=2, ensure_ascii=False))
    print(f"📊 原始节点数：{len(updated_nodes)}，更新后节点数：{len(updated_nodes_2)}")

    file_path = "vishay.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(updated_nodes_2, f, indent=2, ensure_ascii=False)
