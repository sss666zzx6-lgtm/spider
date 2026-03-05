import requests
from lxml import etree
import json
from curl_cffi import requests

def parse_product_leaf_nodes(products, base_url):
    """
    解析产品分类的UL/LI嵌套结构（无固定ID，仅靠class匹配）
    提取前2个产品分类（IC-Contents/Discrete Devices）下的所有叶子节点
    :param products: lxml解析后的Product菜单UL节点列表
    :param base_url: 基础URL（用于拼接相对路径）
    :return: 叶子节点列表，格式：[{"url": "", "category": ""}]
    """
    leaf_nodes = []
    if not products or len(products) == 0:
        print("❌ 未传入有效的Product菜单UL节点")
        return leaf_nodes

    # 取Product菜单的核心UL节点
    product_ul = products[0]

    # 1. 定位前2个产品分类LI（IC-Contents 和 Discrete Devices）
    main_li_list = product_ul.xpath("./li[contains(@class, 'sub_dropdown')][position() <= 2]")
    print(f"🔍 识别到前2个产品分类LI数量：{len(main_li_list)}")

    # 2. 递归解析核心函数（修复层级匹配问题）
    def recursive_parse(li_node, parent_path):
        """
        递归解析单个LI节点
        :param li_node: 当前LI节点
        :param parent_path: 父级分类路径列表
        """
        # 关键修正1：只取当前LI节点的直接子级A标签（./a），而非所有层级
        a_tags = li_node.xpath("./a[contains(@class, 'default2mainBgHover')]")
        if not a_tags:
            return
        a_tag = a_tags[0]

        # 关键修正4：提取A标签内所有纯文本并拼接（处理text+span的情况）
        category_text_list = a_tag.xpath(".//text()")  # 取A标签内所有文本片段
        if not category_text_list:
            return
        # 拼接并清理文本
        category_name = "".join([text.strip() for text in category_text_list if text.strip()])
        category_name = category_name.replace("&amp;", "&").replace("  ", " ").strip()
        if not category_name:
            return

        # 拼接当前分类路径
        current_path = parent_path + [category_name]

        # 提取URL并补全
        href = a_tag.get("href", "").strip()
        full_url = f"{base_url}{href}" if href.startswith("/") else href

        # 关键修正2：只判断当前LI节点的直接子级UL（./ul），而非所有层级
        child_ul = li_node.xpath("./ul[contains(@class, 'dropdown-menu')]")
        is_leaf = len(child_ul) == 0  # 无直接子UL → 叶子节点

        if is_leaf:
            # 叶子节点：添加到结果列表
            leaf_node = {
                "url": full_url,
                "category": "^".join(current_path)
            }
            leaf_nodes.append(leaf_node)
            print(f"✅ 新增叶子节点：{leaf_node}")
        else:
            # 关键修正3：只取当前LI直接子UL下的直接子LI，而非所有层级
            child_li_list = li_node.xpath("./ul[contains(@class, 'dropdown-menu')]/li[contains(@class, 'sub_dropdown')]")
            for child_li in child_li_list:
                recursive_parse(child_li, current_path)

    # 3. 遍历前2个主分类LI进行解析
    for idx, main_li in enumerate(main_li_list):
        print(f"\n========== 开始解析第 {idx+1} 个主分类 ==========")
        recursive_parse(main_li, [])

    return leaf_nodes

if __name__ == "__main__":

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://en.unisonic.com.tw/cate-367402.htm",
        "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    }
    url = "https://en.unisonic.com.tw/product.htm"
    base_url = "https://en.unisonic.com.tw"
    response = requests.get(url,headers=headers)
    tree = etree.HTML(response.text)
    # print(response.text)
    products = tree.xpath("//a[contains(text(), 'Product')]/following-sibling::ul[1]")
    # if products:
    #     product_html = etree.tostring(products[0], encoding='utf-8', pretty_print=True).decode('utf-8')
    #     print("products的HTML内容：")
    #     print(product_html)
    # else:
    #     print("未找到匹配的ul节点")

    leaf_nodes = parse_product_leaf_nodes(products, base_url)

    # 5. 输出最终结果

    print(json.dumps(leaf_nodes, indent=2, ensure_ascii=False))
    print(f"\n========== 解析完成 ==========")
    print(f"📊 共解析出 {len(leaf_nodes)} 个叶子节点")

    file_path = "unisonic.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(leaf_nodes, f, indent=2, ensure_ascii=False)
