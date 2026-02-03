import os
import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse_sidebar_category(soup):
    """
    解析侧边栏分类菜单，提取叶子节点的URL和层级分类名
    :param soup: BeautifulSoup解析后的对象（已加载目标HTML）
    :return: 叶子节点列表，每个元素为{"url": "", "category": ""}
    """
    # 初始化结果列表
    leaf_nodes = []
    # 1. 找到最外层根菜单节点（唯一id，精准定位）
    root_ul = soup.find("ul", id="menu-sidebar-pages-products")
    if not root_ul:
        print("未找到根菜单节点：ul#menu-sidebar-pages-products")
        return leaf_nodes

    # 2. 遍历所有一级分类li（根节点下的直接子li）
    first_level_li_list = root_ul.find_all("li", recursive=False)
    for first_li in first_level_li_list:
        # 提取一级分类名称（去除前后空格，处理特殊字符）
        first_a = first_li.find("a", recursive=False)  # 只找一级li下的直接a标签
        if not first_a:
            continue
        first_level_name = first_a.get_text(strip=True)
        # 3. 找到当前一级分类下的二级子菜单
        sub_ul = first_li.find("ul", class_="sub-menu")
        if not sub_ul:
            continue
        # 4. 遍历二级子菜单的叶子节点li
        leaf_li_list = sub_ul.find_all("li")
        for leaf_li in leaf_li_list:
            # 提取叶子节点的a标签
            leaf_a = leaf_li.find("a")
            if not leaf_a:
                continue
            # 提取叶子URL（示例中已是绝对地址，直接用）
            leaf_url = leaf_a.get("href", "").strip()
            # 提取二级分类名称
            second_level_name = leaf_a.get_text(strip=True)
            # 过滤空URL/空分类名，避免无效数据
            if not leaf_url or not second_level_name:
                continue
            # 拼接层级分类名：一级^二级
            category = f"{first_level_name}^{second_level_name}"
            # 构造结果字典并添加
            leaf_nodes.append({
                "url": leaf_url,
                "category": category
            })
    return leaf_nodes

if __name__ == "__main__":

    html_content = """
    <ul id="menu-sidebar-pages-products" class="menu"><li id="menu-item-136" class="menu-item menu-item-type-post_type menu-item-object-page current-page-ancestor current-menu-ancestor current-menu-parent current-page-parent current_page_parent current_page_ancestor menu-item-has-children menu-item-136"><a style="text-decoration: none;">Protection &amp; System Monitoring</a>
<ul class="sub-menu">
	<li id="menu-item-139" class="menu-item menu-item-type-post_type menu-item-object-page current-menu-item page_item page-item-64 current_page_item menu-item-139"><a href="https://www.kinet-ic.com/protection-system-monitoring/overvoltage-and-surge-protection-ics/" aria-current="page">Overvoltage and Surge Protection ICs</a></li>
	<li id="menu-item-141" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-141"><a href="https://www.kinet-ic.com/protection-system-monitoring/usb-data-line-protection-ics/">USB Data Line Protection ICs</a></li>
	<li id="menu-item-137" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-137"><a href="https://www.kinet-ic.com/protection-system-monitoring/emi-esd-suppression/">EMI/ESD Suppression</a></li>
	<li id="menu-item-140" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-140"><a href="https://www.kinet-ic.com/protection-system-monitoring/reset-ics/">Smart Push Button Reset ICs</a></li>
</ul>
</li>
<li id="menu-item-3065" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children menu-item-3065"><a style="text-decoration: none;">Interface &amp; Isolation</a>
<ul class="sub-menu">
	<li id="menu-item-3126" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-3126"><a href="https://www.kinet-ic.com/interface-isolation/gpio/">GPIO</a></li>
	<li id="menu-item-138" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-138"><a href="https://www.kinet-ic.com/interface-isolation/load-switches/">Load Switch and eFuse</a></li>
</ul>
</li>
<li id="menu-item-128" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children menu-item-128"><a style="text-decoration: none;">Display Power</a>
<ul class="sub-menu">
	<li id="menu-item-129" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-129"><a href="https://www.kinet-ic.com/display-power/camera-led-flash-drivers/">Camera LED Flash Drivers</a></li>
	<li id="menu-item-132" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-132"><a href="https://www.kinet-ic.com/display-power/rgb-led-driver-ics/">RGB LED Driver ICs</a></li>
	<li id="menu-item-131" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-131"><a href="https://www.kinet-ic.com/display-power/led-backlight-drivers-ics/">LED Backlight Drivers ICs</a></li>
	<li id="menu-item-130" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-130"><a href="https://www.kinet-ic.com/display-power/lcd-bias-supply-ics/">LCD Bias Supply ICs</a></li>
</ul>
</li>
<li id="menu-item-125" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children menu-item-125"><a style="text-decoration: none;">DC to DC Conversion</a>
<ul class="sub-menu">
	<li id="menu-item-126" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-126"><a href="https://www.kinet-ic.com/dc-to-dc-converters/non-isolated-dc-dc-conversion/">Non-Isolated DC-DC Conversion</a></li>
	<li id="menu-item-10313" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-10313"><a href="https://www.kinet-ic.com/dc-to-dc-converters/isolated-dc-dc-conversion/">Isolated DC-DC Conversion</a></li>
</ul>
</li>
<li id="menu-item-5140" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children menu-item-5140"><a style="text-decoration: none;">Charging</a>
<ul class="sub-menu">
	<li id="menu-item-5141" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-5141"><a href="https://www.kinet-ic.com/charging/wireless-power-receiver/">Wireless Power Receiver</a></li>
</ul>
</li>
<li id="menu-item-12621" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children menu-item-12621"><a style="text-decoration: none;">Power Over Ethernet</a>
<ul class="sub-menu">
	<li id="menu-item-12623" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-12623"><a href="https://www.kinet-ic.com/power-over-ethernet/poe-pd-controllers/">PoE PD Controllers</a></li>
	<li id="menu-item-12702" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-12702"><a href="https://www.kinet-ic.com/power-over-ethernet/poe-modules/">PoE Modules</a></li>
</ul>
</li>
</ul>
    """
    soup = BeautifulSoup(html_content, "lxml")
    head_pro_node = soup.find("div", class_="head_pro flexlf")
    result = parse_sidebar_category(soup)
    print(json.dumps(result, indent=4, ensure_ascii=False))
    base_path = "./seed_json"
    file_path = os.path.join(base_path, "kinet.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)


