import json
import os
import re
import requests
from bs4 import BeautifulSoup
import time
import chardet


def extract_category_leaf_nodes(soup):

    leaf_nodes = []
    base_url = "https://www.xlsemi.com/"

    # 第一步：全局找所有叶子节点的<li>（核心特征：有<a>标签 + 无子女<ul>）
    all_li = soup.find_all("li")
    leaf_li_list = []
    for li in all_li:
        # 条件1：li下有<a>标签（有分类名/URL）
        a_tag = li.find("a")
        if not a_tag:
            continue
        # 条件2：li下无任何子<ul>（是叶子节点）
        child_ul = li.find("ul")
        if child_ul:
            continue
        # 条件3：分类名非空
        category_name = a_tag.get_text(strip=True)
        if not category_name:
            continue
        leaf_li_list.append(li)

    # 第二步：对每个叶子<li>，反向追溯所有父级分类名
    for leaf_li in leaf_li_list:
        a_tag = leaf_li.find("a")
        leaf_name = a_tag.get_text(strip=True)
        leaf_url = f"{base_url}{a_tag.get('href', '').strip()}"

        # 反向找所有父级分类名
        parent_categories = []
        current_node = leaf_li.parent  # 从叶子li的父节点开始往上找
        while current_node:
            # 找当前层级的分类名（找当前节点下的<li>里的<a>，且该<li>有子<ul>）
            if current_node.name == "ul":
                # 找该<ul>对应的父<li>（即包含这个<ul>的<li>）
                parent_li = current_node.find_parent("li")
                if parent_li:
                    parent_a = parent_li.find("a")
                    if parent_a:
                        parent_name = parent_a.get_text(strip=True)
                        if parent_name and parent_name not in parent_categories:
                            parent_categories.append(parent_name)
            # 往上找一级
            current_node = current_node.find_parent("ul")

        # 修正分类路径顺序（反向找的是倒序，需要反转）
        parent_categories.reverse()
        full_category = "^".join(parent_categories + [leaf_name])

        # 加入结果（去重）
        leaf_node = {
            "url": leaf_url,
            "category": full_category
        }
        if leaf_node not in leaf_nodes:
            leaf_nodes.append(leaf_node)
            print(f"解析叶子节点：{full_category} → {leaf_url}")

    # 统计
    print(f"解析统计：共解析 {len(leaf_nodes)} 个叶子节点")
    return leaf_nodes

if __name__ == "__main__":

    url = "https://www.xlsemi.com/products_MEMS_pressure_gauge.html"
    response = requests.get(url)

    # print(response.text)
    response.encoding = response.apparent_encoding
    # print(response.text)

    raw_html = response.text
    # 1. 替换掉所有<html>...</html>片段（反爬干扰）
    clean_html = re.sub(r'<html.*?</html>', '', raw_html, flags=re.DOTALL | re.IGNORECASE)
    # 2. 给干净的内容包裹一个<html>标签（让BeautifulSoup能正常解析）
    clean_html = f"<html>{clean_html}</html>"

    html_content = """
    <div class="widget_content">
<ul class="categories_list">
<li class="active"><a class="d_block f_size_large color_dark relative"><b>电源管理</b>
<span class="bg_light_color_1 r_corners f_right color_dark talign_c"></span></a>
<!--second level-->
<ul class="active">
<li class="active"><a href="products_DC_DC_buck_mv.html" class="d_block f_size_large color_dark relative"><b>DC-DC电源管理</b>
<span class="bg_light_color_1 r_corners f_right color_dark talign_c"></span></a>
<!--third level-->
<ul class="active">
<li class="active"><a href="products_DC_DC_buck_mv.html" class="d_block f_size_large color_dark relative"><b>降压型变换器</b>
<span class="bg_light_color_1 r_corners f_right color_dark talign_c"></span></a>
<!--four level-->
<ul class="active">
<li class="active" style="text-indent:1em"><a href="products_DC_DC_buck_mv.html" class="color_dark d_block">中压降压</a></li>
<li style="text-indent:1em"><a href="products_DC_DC_buck_mvsr.html" class="color_dark d_block">中压降压同步整流</a></li>
<li style="text-indent:1em"><a href="products_DC_DC_buck_hv.html" class="color_dark d_block">高压降压</a></li>
<li style="text-indent:1em"><a href="products_DC_DC_buck_hvsr.html" class="color_dark d_block">高压降压同步整流</a></li>
</ul>
</li>
<!--third level-->
<ul class="active">
<li class="active"><a href="products_DC_DC_boost_mv.html" class="d_block f_size_large color_dark relative"><b>升压型变换器</b>
<span class="bg_light_color_1 r_corners f_right color_dark talign_c"></span></a>
<!--four level-->
<ul class="active">
<li style="text-indent:1em"><a href="products_DC_DC_boost_mvsbd.html" class="color_dark d_block">中压升压（内置SBD）</a></li>
<li style="text-indent:1em"><a href="products_DC_DC_boost_mvsr.html" class="color_dark d_block">中压升压同步整流</a></li>
<li style="text-indent:1em"><a href="products_DC_DC_boost_hv.html" class="color_dark d_block">高压升压</a></li>
</ul>
</li>
</ul>
<li>
<!--third level-->
<ul class="active">
<li class="active"><a href="products_DC_DC_led_buck.html" class="d_block f_size_large color_dark relative"><b>LED驱动</b>
<span class="bg_light_color_1 r_corners f_right color_dark talign_c"></span></a>
<!--four level-->
<ul class="active">
<li style="text-indent:1em"><a href="products_DC_DC_led_buck.html" class="color_dark d_block">降压恒流驱动</a></li>
<li style="text-indent:1em"><a href="products_DC_DC_led_bucksr.html" class="color_dark d_block">降压同步整流恒流驱动</a></li>
<li style="text-indent:1em"><a href="products_DC_DC_led_boost.html" class="color_dark d_block">升压恒流驱动</a></li>
<li style="text-indent:1em"><a href="products_DC_DC_led_boostsbd.html" class="color_dark d_block">升压恒流驱动（内置SBD）</a></li>
<li style="text-indent:1em"><a href="products_DC_DC_led_backlight.html" class="color_dark d_block">背光驱动</a></li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
<li>
<!--second level-->
</li><li class="active"><a href="products_AC_DC_N_Isolated.html" class="d_block f_size_large color_dark relative"><b>AC-DC电源管理</b>
<span class="bg_light_color_1 r_corners f_right color_dark talign_c"></span></a>
<!--third level-->
<ul class="active">
<li><a href="products_AC_DC_N_Isolated.html" class="color_dark d_block">非隔离型变换器</a></li>
<li><a href="products_AC_DC_Isolated.html" class="color_dark d_block">隔离型变换器</a></li>
</ul>
</li>
<!--second level-->
<li class="active"><a href="products_BMS_monitors_balancers.html" class="d_block f_size_large color_dark relative"><b>BMS</b>
<span class="bg_light_color_1 r_corners f_right color_dark talign_c"></span></a>
<!--third level-->
<ul class="active">
<li><a href="products_BMS_monitors_balancers.html" class="color_dark d_block">电池监控与均衡器</a></li>
<li><a href="products_BMS_protectors.html" class="color_dark d_block">电池保护器</a></li>
<li><a href="products_BMS_active.html" class="color_dark d_block">主动均衡器</a></li>
</ul>
</li>
<!--second level-->
<li class="active"><a href="products_BMS_monitors_balancers.html" class="d_block f_size_large color_dark relative"><b>Motor Drivers</b>
<span class="bg_light_color_1 r_corners f_right color_dark talign_c"></span></a>
<!--third level-->
<ul class="active">
<li><a href="products_MD_IPM.html" class="color_dark d_block">IPM</a></li>

</ul>
</li>
</ul>
</li><li class="active">
<a class="f_size_large color_dark d_block relative"><b>信号链</b>
<span class="bg_light_color_1 r_corners f_right color_dark talign_c"></span></a>
<!--second level-->
<ul class="active">
<li class="active">
<a href="products_HBS.html" class="d_block f_size_large color_dark relative">直流电源载波通讯</a></li>

</ul>
</li>
<li class="active">
<a class="f_size_large color_dark d_block relative"><b>音频功放</b>
<span class="bg_light_color_1 r_corners f_right color_dark talign_c"></span></a>
<!--second level-->
<ul class="active">
<li class="active"><a href="products_AB_audio.html" class="d_block f_size_large color_dark relative">AB类音频功率放大器</a></li>
<li><a href="products_D_audio.html" class="d_block f_size_large color_dark relative">D类音频功率放大器</a></li>

</ul>
</li>
<li class="active">
<a class="f_size_large color_dark d_block relative"><b>MEMS传感器</b>
<span class="bg_light_color_1 r_corners f_right color_dark talign_c"></span></a>
<!--second level-->
<ul class="active">
<li class="active"><a href="products_MEMS_hall_switch.html" class="d_block f_size_large color_dark relative"><b>霍尔传感器</b>
<span class="bg_light_color_1 r_corners f_right color_dark talign_c"></span></a>
<!--third level-->
<ul class="active">
<li><a href="products_MEMS_hall_switch.html" class="color_dark d_block">霍尔开关传感器</a></li>
<li><a href="products_MEMS_linear_hall.html" class="color_dark d_block">线性霍尔传感器</a></li>
<li><a href="products_MEMS_motor_driver.html" class="color_dark d_block">霍尔开关电机驱动器</a></li>
<li><a href="products_MEMS_current_sensors.html" class="color_dark d_block">电流传感器</a></li>
</ul>
</li>
<!--second level-->
<li class="active">
</li><li class="active"><a href="products_MEMS_IR_NDIR.html" class="d_block f_size_large color_dark relative"><b>TMR磁传感器</b>
<span class="bg_light_color_1 r_corners f_right color_dark talign_c"></span></a>
<!--third level-->
<ul class="active">
<li><a href="products_MEMS_angle.html" class="color_dark d_block">TMR角度传感器</a></li>
</ul>
</li>
<!--second level-->
<li class="active">
</li><li class="active"><a href="products_MEMS_IR_NDIR.html" class="d_block f_size_large color_dark relative"><b>红外传感器</b>
<span class="bg_light_color_1 r_corners f_right color_dark talign_c"></span></a>
<!--third level-->
<ul class="active">
<li><a href="products_MEMS_IR_NDIR.html" class="color_dark d_block">非分光红外型气体探测器</a></li>
<li><a href="products_MEMS_IR_non_contact.html" class="color_dark d_block">非接触式温度传感器</a></li>
<li><a href="products_MEMS_IR_thermopile.html" class="color_dark d_block">非制冷红外热电堆阵列探测器</a></li>
<li><a href="products_MEMS_IR_Vox.html" class="color_dark d_block">非制冷氧化钒红外焦平面探测器</a></li>
</ul>
</li>
<!--second level-->
<li class="active">
</li><li class="active"><a href="products_MEMS_pressure_gauge.html" class="d_block f_size_large color_dark relative"><b>压力传感器</b>
<span class="bg_light_color_1 r_corners f_right color_dark talign_c"></span></a>
<!--third level-->
<ul class="active">
<li><a href="products_MEMS_pressure_gauge.html" class="color_dark d_block" style="color:#4268d6">表压传感器</a></li>
<li><a href="products_MEMS_pressure_absolute.html" class="color_dark d_block">绝压传感器</a></li>
</ul>
</li>
</ul>
</li>
<li class="active">

</li>

</ul></div>
    """

    soup = BeautifulSoup(html_content, "lxml")
    leaf_nodes = extract_category_leaf_nodes(soup)

    # 打印结果+验证数量
    print(json.dumps(leaf_nodes, indent=4, ensure_ascii=False))
    print(f"\n最终叶子节点数量：{len(leaf_nodes)}")

    base_path = "./seed_json"
    file_path = os.path.join(base_path, "xlsemi.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(leaf_nodes, f, indent=2, ensure_ascii=False)