import os
import re
import json
import time

# import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from curl_cffi import requests

BASE_DOMAIN = "https://www.skyworksinc.com"
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://www.skyworksinc.com/Products/Cellular%20Amplifiers",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-bitness": "\"64\"",
    "sec-ch-ua-full-version-list": "\"Not(A:Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"144.0.7559.110\", \"Google Chrome\";v=\"144.0.7559.110\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-platform-version": "\"19.0.0\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
}


def update_skyworks_result(original_result):
    """
    处理原始result列表，爬取非family的URL节点
    :param original_result: 原始的产品列表（字典组成的列表，含url、category键）
    :return: 仅保留叶子节点的新result列表
    """
    final_result = []  # 最终的叶子节点结果
    # 遍历原始列表，分情况处理
    for item in original_result:
        item_url = item.get("url", "")
        item_category = item.get("category", "")
        # 校验必要的键，缺少则跳过（无url/category的项无保留意义）
        if not item_url or not item_category:
            print(f"跳过无效项：{item}（缺少url或category）")
            continue

        # 情况1：URL包含family，直接保留为叶子节点
        if "family" in item_url:
            final_result.append(item)
            print(f"保留family叶子节点：{item_category}")
            continue

        # 情况2：URL不包含family，发起请求尝试爬取三级节点
        try:
            # 发起GET请求，设置超时、自动重定向
            response = requests.get(
                url=item_url,
                headers=HEADERS,
                timeout=10,
                allow_redirects=True
            )
            response.raise_for_status()  # 捕获HTTP错误（404/500等）
            print(response)
            # response.encoding = response.apparent_encoding

            # 解析HTML
            soup = BeautifulSoup(response.text, "lxml")
            # 找到目标容器：col-sm-12 container-list
            container = soup.find("div", class_="col-sm-12 container-list")
            if not container:
                # 无目标容器 → 保留原二级节点
                final_result.append(item)
                print(f"无目标容器，保留原二级节点：{item_category} | URL：{item_url}")
                continue

            # 提取容器内的三级节点a标签
            third_level_a_list = container.find_all("a", class_="item-prod-family")
            if not third_level_a_list:
                # 有容器但无三级节点 → 保留原二级节点
                final_result.append(item)
                print(f"容器内无三级节点，保留原二级节点：{item_category} | URL：{item_url}")
                continue

            # 成功解析出三级节点 → 拼接新节点替换原二级节点，加入最终结果
            for a_tag in third_level_a_list:
                third_href = a_tag.get("href", "")
                third_title = a_tag.find("h4").get_text(strip=True) if a_tag.find("h4") else ""
                if not third_href or not third_title:
                    continue
                # 拼接绝对URL和层级category
                third_abs_url = urljoin(BASE_DOMAIN, third_href)
                third_category = f"{item_category}^{third_title}"
                final_result.append({
                    "url": third_abs_url,
                    "category": third_category
                })
            print(f"解析成功，替换为三级节点：{item_category} | 提取到{len(third_level_a_list)}个三级叶子节点")

        except requests.exceptions.RequestException as e:
            # 所有请求异常（超时/404/网络错误等）→ 保留原二级节点
            final_result.append(item)
            print(f"请求/解析异常，保留原二级节点：{item_category} | 原因：{str(e)[:80]} | URL：{item_url}")
            continue

    return final_result

def parse_product_categories(soup):
    result_list = []
    base_url = "https://www.skyworksinc.com"

    # 第一步：定位核心分类容器（id=collapse_Products，所有一级分类都在里面）
    root_container = soup.find("div", id="collapse_Products")
    if not root_container:
        return result_list

    # 第二步：遍历所有一级分类项（li.nav-item）
    first_cate_items = root_container.find_all("li", class_="nav-item")
    for first_item in first_cate_items:
        # 🔥 核心修正：用CSS选择器包含匹配，替代class_精确匹配，解决collapsed后缀问题
        # 只要a标签同时有nav-link和item-header-second两个class，不管有没有其他class都能找到
        first_a = first_item.select_one("a.nav-link.item-header-second")
        if not first_a:
            continue
        first_cate = first_a.get_text(strip=True)
        # 过滤无效一级分类（文本为空、Technology Standards直接跳过）
        if not first_cate or "Technology Standards" in first_cate:
            continue

        # 第三步：定位当前一级分类对应的二级叶子节点容器（div.third-level）
        leaf_container = first_item.find("div", class_="third-level")
        if not leaf_container:
            continue

        # 第四步：提取二级叶子节点（精准匹配ul>li>a，无下级）
        leaf_a_list = leaf_container.select("div.well > ul > li > a")
        if not leaf_a_list:
            continue

        # 第五步：遍历叶子节点，构造结果
        for leaf_a in leaf_a_list:
            leaf_url = leaf_a.get("href", "").strip()
            leaf_cate = leaf_a.get_text(strip=True)
            # 过滤无效数据
            if not leaf_url or not leaf_cate:
                continue
            # 按规则拼接：一级^二级
            full_url = f"{base_url}{leaf_url}"
            full_cate = f"{first_cate}^{leaf_cate}"
            result_list.append({
                "url": full_url,
                "category": full_cate
            })
    return result_list

if __name__ == "__main__":
    html_content ="""
    <div class="second-level collapse in" id="collapse_Products" aria-expanded="true" style="">
                                    <div class="well">
                                        <ul class="">
                                                <li class="nav-item" role="presentation">
                                                    <!-- 2nd level mobile navigation with 3rd level -->
                                                    <a class="nav-link item-header-second" role="button" data-toggle="collapse" href="#collapse_Amplifiers" aria-expanded="true" aria-controls="collapse_Amplifiers">
                                                        Amplifiers
                                                    </a>
                                                    <div class="third-level collapse in" id="collapse_Amplifiers" aria-expanded="true" style="">
                                                        <div class="well">
<ul>
    <li><a href="/Products/Cellular%20Amplifiers">Cellular PAs</a></li>
    <li><a href="/Product-Specification?family=Amplifiers&amp;categories=Gain%20Block%20(General%20Purpose)%20Amplifiers">Gain Block (General Purpose)</a></li>
    <li><a href="/en/Products/Amplifiers-WiFi">Wi-Fi Connectivity</a></li>
    <li><a href="/Product%20Specification?family=Amplifiers&amp;categories=BDS/GPS/GNSS%20Power%20Amplifiers;BDS/GPS/GNSS%20Power%20Amplifiers">BDS/GPS/GNSS</a></li>
    <li><a href="/Product%20Specification?family=Amplifiers&amp;categories=Low%20Noise%20Amplifiers;Low%20Noise%20Amplifiers">Low Noise Amplifiers (LNAs)</a></li>
    <li><a href="/Product%20Specification?family=Amplifiers&amp;categories=CATV%20Amplifiers;CATV%20Amplifiers;12v%20Line%20Amplifiers%20for%20HFC;24v%20Line%20Amplifiers%20for%20HFC;75%20Ohm%20Gain%20Blocks%20for%20HFC;Amplifiers%20for%20Set-top%20Box;CATV%20Driver%20Amplifier;FTTx/RFoG%20RF%20Amplifiers%20for%20HFC;Hybrid%20Line%20Amplifier%20Modules%20for%20HFC;Low-Noise%20Amplifier%20for%20Set-top%20Box;Upstream%20Amplifiers%20for%20HFC">CATV</a></li>
    <li><a href="/Product%20Specification?family=Amplifiers&amp;categories=Variable%20Gain%20Amplifiers%20(VGAs);Variable%20Gain%20Amplifiers%20(VGAs)">Variable Gain Amplifiers (VGAs)</a></li>
    <li><a href="/Product%20Specification?family=Amplifiers&amp;categories=Wireless%20Infrastructure%20/%20Small%20Cell%20Power%20Amplifiers;Wireless%20Infrastructure%20/%20Small%20Cell%20Power%20Amplifiers;Wireless%20Infrastructure%20/%20Small%20Cell%20Power%20Amplifiers;High%20Efficiency%20Linearizable%20Small%20Cell%20Power%20Amplifiers;High%20Linearity%20Small%20Cell%20Power%20Amplifiers;Small%20Cell%20Gain%20Blocks;WiMAX%20Power%20Amplifiers;High-efficiency%20Small%20Cell%20Power%20Amps%20for%205G">Wireless Infrastructure And Small Cells</a></li>
    <li><a href="/Product%20Specification?family=Amplifiers&amp;categories=Amplifiers%20for%20Smart%20Energy-Connected%20Home%20and%20Automation%20802.15.4,%20ISM%20and%20ZigBee%C2%AE;Amplifiers%20for%20Smart%20Energy-Connected%20Home%20and%20Automation%20802.15.4,%20ISM%20and%20ZigBee%C2%AE">Smart Energy - Connected Home And Automation 802.15.4, ISM And Zigbee®</a></li>
    <li><a href="/Product%20Specification?family=Amplifiers&amp;categories=High-efficiency%20Small%20Cell%20Power%20Amps%20for%205G">High-Efficiency Small Cell Power Amps For 5G</a></li>
</ul>
</div>
                                                    </div>
                                                </li>
                                                <li class="nav-item" role="presentation">
                                                    <!-- 2nd level mobile navigation with 3rd level -->
                                                    <a class="nav-link item-header-second collapsed" role="button" data-toggle="collapse" href="#collapse_AudioandRadio" aria-expanded="false" aria-controls="collapse_AudioandRadio">
                                                        Audio and Radio
                                                    </a>
                                                    <div class="collapse third-level" id="collapse_AudioandRadio">
                                                        <div class="well">
<ul>
    <li><a href="/en/System-Solutions/Audio">Audio Solutions</a></li>
    <li><a href="/Products/Audio-and-Radio-Automotive-Tuners">Automotive Tuners</a></li>
    <li><a href="/Products/Audio-and-Radio-Consumer-Digital-Radios">Consumer Digital Radios</a></li>
    <li><a href="/Products/Audio-and-Radio-Automotive-Digital-Data-Receivers">Automotive Digital Data Receivers</a></li>
    <li><a href="/Products/Audio-and-Radio-FM-Radios">FM Radios</a></li>
    <li><a href="/Products/Audio-and-Radio/Si824x-Class-D-Audio-Drivers">Audio Gate Drivers</a></li>
    <li><a href="/Products/Audio-and-Radio-Multiband-Radios">Multiband Radios</a></li>
    <li><a href="/Products/Audio-and-Radio-Automotive-Digital-Radio-Coprocessors">Automotive Digital Radio Coprocessors</a></li>
    <li><a href="/Products/Audio-and-Radio/Evaluation-Kits#collapseall">Evaluation Kits</a></li>
</ul>
</div>
                                                    </div>
                                                </li>
                                                <li class="nav-item" role="presentation">
                                                    <!-- 2nd level mobile navigation with 3rd level -->
                                                    <a class="nav-link item-header-second collapsed" role="button" data-toggle="collapse" href="#collapse_Attenuators" aria-expanded="false" aria-controls="collapse_Attenuators">
                                                        Attenuators
                                                    </a>
                                                    <div class="collapse third-level" id="collapse_Attenuators">
                                                        <div class="well">
<ul>
    <li><a href="/Product%20Specification?family=Attenuators&amp;categories=Digital%20Attenuators;Digital%20Attenuators">Digital Attenuators</a></li>
    <li><a href="/Product%20Specification?family=Attenuators&amp;categories=Voltage%20Variable%20Attenuators;Voltage%20Variable%20Attenuators;0.7%20-%205.0%20GHz%20Plastic%20Packaged%20Voltage%20Variable%20Attenuators%20-%20PIN%20Diode-Based;DC-6%20GHz%20Plastic%20Packaged%20Voltage%20Variable%20Attenuators%20-%20FET-Based">Voltage Variable Attenuators (VVAs)</a></li>
    <li><a href="/Product%20Specification?family=Attenuators&amp;categories=ATN3580%20Fixed%20Attenuator%20Pads">Fixed Attenuator Pads (ATN3580)</a></li>
    <li><a href="/Product%20Specification?family=Attenuators&amp;categories=ATN3590%20Fixed%20Attenuator%20Pads">Fixed Attenuator Pads (ATN3590)</a></li>
</ul>
</div>
                                                    </div>
                                                </li>
                                                <li class="nav-item" role="presentation">
                                                    <!-- 2nd level mobile navigation with 3rd level -->
                                                    <a class="nav-link item-header-second collapsed" role="button" data-toggle="collapse" href="#collapse_ClocksandTiming" aria-expanded="false" aria-controls="collapse_ClocksandTiming">
                                                        Clocks and Timing
                                                    </a>
                                                    <div class="collapse third-level" id="collapse_ClocksandTiming">
                                                        <div class="well">
<ul>
    <li><a href="/Products/Timing-Automotive-Timing">Automotive Timing</a></li>
    <li><a href="/Products/Timing-Clock-Buffers">Clock Buffers</a></li>
    <li><a href="/Products/Timing-Clock-Generators">Clock Generators</a></li>
    <li><a href="/Products/Timing-PCIe-Timing">PCIe Timing</a></li>
    <li><a href="/Products/Timing-Oscillators">Oscillators</a></li>
    <li><a href="/Products/Timing-IEEE-1588-and-Synchronous-Ethernet">Wireless 5G and Wireline Network Synchronization</a></li>
    <li><a href="/Products/Timing-Jitter-Attenuators">Jitter Attenuators</a></li>
    <!--<li><a href="/Products/Timing/CDR-and-PHY">CDR And PHY</a></li>-->
    <li><a href="/Products/Timing/RF-Synthesizers">RF Synthesizers</a></li>
    <li><a href="/Products/Timing/Evaluation-Kits#collapseall">Evaluation Kits</a></li>
    <li><a href="/Blog#tab-timing">Timing Blog</a></li>



</ul>
</div>
                                                    </div>
                                                </li>
                                                <li class="nav-item" role="presentation">
                                                    <!-- 2nd level mobile navigation with 3rd level -->
                                                    <a class="nav-link item-header-second collapsed" role="button" data-toggle="collapse" href="#collapse_Diodes" aria-expanded="false" aria-controls="collapse_Diodes">
                                                        Diodes
                                                    </a>
                                                    <div class="collapse third-level" id="collapse_Diodes">
                                                        <div class="well">
<ul>
    <li><a href="/Products/Limiter-Diodes">Limiter Diodes</a></li>
    <li><a href="/Products/PIN-Diodes">PIN Diodes</a></li>
    <li><a href="/Products/Schottky-Diodes">Schottky Diodes</a></li>
    <li><a href="/Products/Varactor-Diodes">Varactor Diodes</a></li>
    <li><a href="/en/Products/High%20reliability%20Diodes">High reliability Diodes</a></li>
    <li><a href="/en/Product-Specification?family=Diodes&amp;categories=Limiter%20Modules">Limiter Modules</a></li>
</ul>
</div>
                                                    </div>
                                                </li>
                                                <li class="nav-item" role="presentation">
                                                    <!-- 2nd level mobile navigation with 3rd level -->
                                                    <a class="nav-link item-header-second collapsed" role="button" data-toggle="collapse" href="#collapse_FrontEndModules" aria-expanded="false" aria-controls="collapse_FrontEndModules">
                                                        Front-End Modules
                                                    </a>
                                                    <div class="collapse third-level" id="collapse_FrontEndModules">
                                                        <div class="well">
<ul>
    <li><a href="/Products/Front-end-Modules-Cellular">Cellular</a></li>
    <li><a href="/Product%20Specification?family=Front-end%20Modules&amp;categories=Front-end%20Modules%20for%20Automotive;Front-end%20Modules%20for%20Automotive">Automotive</a></li>
    <li><a href="/Product-Specification?family=Front-end%20Modules&amp;categories=Front-end%20Modules%20for%20Cellular%20IoT%20and%20M2M">Cellular Iot</a></li>
    <li><a href="/Product%20Specification?family=Front-end%20Modules&amp;categories=BDS/GPS/GNSS%20Front-end%20Modules;BDS/GPS/GNSS%20Front-end%20Modules">Bds/Gps/Gnss</a></li>
    <li><a href="/Products/Front-end-Modules-WiFi">Wi-Fi Connectivity</a></li>
    <li><a href="/Product%20Specification?family=Front-end%20Modules&amp;categories=Diversity%20Receive%20Modules;Diversity%20Receive%20Modules">Diversity Receive</a></li>
    <li><a href="/Product-Specification?family=Front-end%20Modules&amp;categories=Front-end%20Modules%20for%20Massive-MIMO">Massive-MIMO</a></li>

    <li><a href="/Product%20Specification?family=Front-end%20Modules&amp;categories=Front-end%20Modules%20for%20Connected%20Home,%20Industrial,%20M2M,%20Medical,%20Smart%20Energy%20and%20Wearables;Front-end%20Modules%20for%20Connected%20Home,%20Industrial,%20M2M,%20Medical,%20Smart%20Energy%20and%20Wearables">Connected Home, Industrial, M2M, Medical, Smart Energy And Wearables</a></li>
    <li><a href="/Product%20Specification?family=Front-end%20Modules&amp;categories=BDS/GPS/GNSS%20Front-end%20Modules;BDS/GPS/GNSS%20Front-end%20Modules">CATV</a></li>
</ul>
</div>
                                                    </div>
                                                </li>
                                                <li class="nav-item" role="presentation">
                                                    <!-- 2nd level mobile navigation with 3rd level -->
                                                    <a class="nav-link item-header-second collapsed" role="button" data-toggle="collapse" href="#collapse_Filters" aria-expanded="false" aria-controls="collapse_Filters">
                                                        Filters
                                                    </a>
                                                    <div class="collapse third-level" id="collapse_Filters">
                                                        <div class="well">
<ul>
    <li><a href="/en/Product-Specification?family=Filters&amp;categories=BAW%20Filters">BAW Filters</a></li>
</ul>
</div>
                                                    </div>
                                                </li>
                                                <li class="nav-item" role="presentation">
                                                    <!-- 2nd level mobile navigation with 3rd level -->
                                                    <a class="nav-link item-header-second collapsed" role="button" data-toggle="collapse" href="#collapse_Isolation" aria-expanded="false" aria-controls="collapse_Isolation">
                                                        Isolation
                                                    </a>
                                                    <div class="collapse third-level" id="collapse_Isolation">
                                                        <div class="well">
<ul>
    <li><a href="/Products/Isolation-Automotive-Isolation">Automotive Isolation</a></li>
    <li><a href="/Products/Isolation-Digital-Isolators">Digital Isolators</a></li>
    <li><a href="/Products/Isolation-Isolated-Gate-Drivers">Isolated Gate Drivers</a></li>
    <li><a href="/Products/Isolation-Isolated-Analog-and-ADCs">Isolated Analog and ADCs</a></li>
    <li><a href="/Products/Isolation-Industrial-IO">Industrial I/O</a></li>
    <li><a href="/Products/Isolation-Isolated-FET-Drivers">Isolated FET Drivers</a></li>
    <li><a href="/en/Products/Isolation-Isolated-Transceivers">Isolated Transceivers</a></li>
    <li><a href="/Products/Isolation/Evaluation-Kits#collapseall">Evaluation Kits</a></li>
</ul>
</div>
                                                    </div>
                                                </li>
                                                <li class="nav-item" role="presentation">
                                                    <!-- 2nd level mobile navigation with 3rd level -->
                                                    <a class="nav-link item-header-second collapsed" role="button" data-toggle="collapse" href="#collapse_ModemsAndDAAs" aria-expanded="false" aria-controls="collapse_ModemsAndDAAs">
                                                        Modems And DAAs
                                                    </a>
                                                    <div class="collapse third-level" id="collapse_ModemsAndDAAs">
                                                        <div class="well">
<ul>
    <li><a href="/Products/Modems-and-DAAs/Data-and-Voice-Modems">Data And Voice Modems</a></li>
    <li><a href="/Products/Modems-and-DAAs/Fax-Modems">Fax Modems</a></li>
</ul>
</div>
                                                    </div>
                                                </li>
                                                <li class="nav-item" role="presentation">
                                                    <!-- 2nd level mobile navigation with 3rd level -->
                                                    <a class="nav-link item-header-second collapsed" role="button" data-toggle="collapse" href="#collapse_Optocouplers" aria-expanded="false" aria-controls="collapse_Optocouplers">
                                                        Optocouplers
                                                    </a>
                                                    <div class="collapse third-level" id="collapse_Optocouplers">
                                                        <div class="well">
<ul>
    <li><a href="/Product%20Specification?family=Optocouplers&amp;categories=Phototransistor%20Optocouplers;Phototransistor%20Optocouplers">Phototransistor Optocouplers</a></li>
    <li><a href="/Product%20Specification?family=Optocouplers&amp;categories=High-speed%20Optocouplers;High-speed%20Optocouplers">High-Speed Optocouplers</a></li>
    <li><a href="/Product%20Specification?family=Optocouplers&amp;categories=Low%20Input%20Current%20Photodarlington%20Optocouplers;Low%20Input%20Current%20Photodarlington%20Optocouplers">Low Input Current Photodarlington Optocouplers</a></li>
    <li><a href="/Product%20Specification?family=Optocouplers&amp;categories=High-speed%20Switching,%20High%20CMR,%20Logic%20Gate%20Optocouplers;High-speed%20Switching,%20High%20CMR,%20Logic%20Gate%20Optocouplers">High-Speed Switching, High CMR, Logic Gate Optocouplers</a></li>
    <li><a href="/Product%20Specification?family=Optocouplers&amp;categories=Schmitt%20Trigger%20Optocouplers;Schmitt%20Trigger%20Optocouplers">Schmitt Trigger Optocouplers</a></li>
    <li><a href="/Product%20Specification?family=Optocouplers&amp;categories=Linear%20Optocouplers;Linear%20Optocouplers">Linear Optocouplers</a></li>
    <li><a href="/Product%20Specification?family=Optocouplers&amp;categories=Photovoltaic%20Optocouplers;Photovoltaic%20Optocouplers">Photovoltaic Optocouplers</a></li>
    <li><a href="/Product%20Specification?family=Optocouplers&amp;categories=High-speed%20MOS-FET%20Driver;High-speed%20MOS-FET%20Driver">High-Speed MOS-FET Driver</a></li>
    <li><a href="/Articles/Aerospace%20and%20Defense%20Hi-Rel%20Custom%20solutions">Custom Solutions</a></li>
</ul>
</div>
                                                    </div>
                                                </li>
                                                <li class="nav-item" role="presentation">
                                                    <!-- 2nd level mobile navigation with 3rd level -->
                                                    <a class="nav-link item-header-second collapsed" role="button" data-toggle="collapse" href="#collapse_PowerManagement" aria-expanded="false" aria-controls="collapse_PowerManagement">
                                                        Power Management
                                                    </a>
                                                    <div class="collapse third-level" id="collapse_PowerManagement">
                                                        <div class="well">
<ul>
    <li><a href="/Product%20Specification?family=Power%20Management&amp;categories=Display%20and%20Lighting;Display%20and%20Lighting;LED%20Camera%20Flash%20Drivers;Charge%20Pump%E2%84%A2%20Camera%20LED%20Flash%20Drivers%20;Serial%20Boost%20Camera%20LED%20Flash%20Drivers%20;Mid%20to%20Large%20Screen%20LCD%20LED%20Backlight%20with%20PMW%20Interface;RGB%20LED%20Driver;White%20LED%20Drivers;Charge%20Pump%20Based%20White%20LED%20Backlight%20Drivers%20;Serial%20Boost%20White%20LED%20Backlight%20Drivers">Display And Lighting</a></li>
    <li><a href="/Product%20Specification?family=Power%20Management&amp;categories=Port%20Protection%20and%20Power%20Distribution;Port%20Protection%20and%20Power%20Distribution;Over%20Voltage%20Protection;Slew%20Rate%20Controlled">Port Protection And Power Distribution</a></li>
    <li><a href="/Product%20Specification?family=Power%20Management&amp;categories=Voltage%20Regulation;Voltage%20Regulation;RF%20PMIC;Step-Down%20Converters">Voltage Regulation</a></li>
</ul>
</div>
                                                    </div>
                                                </li>
                                                <li class="nav-item" role="presentation">
                                                    <!-- 2nd level mobile navigation with 3rd level -->
                                                    <a class="nav-link item-header-second collapsed" role="button" data-toggle="collapse" href="#collapse_PowerOverEthernet" aria-expanded="false" aria-controls="collapse_PowerOverEthernet">
                                                        Power Over Ethernet
                                                    </a>
                                                    <div class="collapse third-level" id="collapse_PowerOverEthernet">
                                                        <div class="well">
<ul>
    <li><a href="/Products/Power-Powered-Devices">Powered Devices</a></li>
    <li><a href="/Products/Power-PSE-Controllers-Power-Sourcing-Equipment">PSE Controllers - Power Sourcing Equipment</a></li>
    <li><a href="/Products/Power/Evaluation-Kits#collapseall">Evaluation Kits</a></li>
    <li><a href="/en/tools-and-training/PoE">PoE Training Videos</a></li>
</ul>
</div>
                                                    </div>
                                                </li>
                                                <li class="nav-item" role="presentation">
                                                    <!-- 2nd level mobile navigation with 3rd level -->
                                                    <a class="nav-link item-header-second collapsed" role="button" data-toggle="collapse" href="#collapse_RFPassives" aria-expanded="false" aria-controls="collapse_RFPassives">
                                                        RF Passives
                                                    </a>
                                                    <div class="collapse third-level" id="collapse_RFPassives">
                                                        <div class="well">
<ul>
    <li><a href="/Product%20Specification?family=RF%20Passives&amp;categories=MIS%20Silicon%20Chip%20Capacitors;MIS%20Silicon%20Chip%20Capacitors">MIS Silicon Chip Capacitors</a></li>
    <li><a href="/Product%20Specification?family=Switches&amp;categories=Smart%20Coupler;Smart%20Coupler">Couplers</a></li>
    <li><a href="/Product%20Specification?family=RF%20Passives&amp;categories=Power%20Dividers/Combiners;Power%20Dividers/Combiners;Active%20Splitters%20for%20Set-top%20Box;Power%20Dividers%20-%202%20Way">Power Dividers / Combiners</a></li>
</ul>
</div>
                                                    </div>
                                                </li>
                                                <li class="nav-item" role="presentation">
                                                    <!-- 2nd level mobile navigation with 3rd level -->
                                                    <a class="nav-link item-header-second collapsed" role="button" data-toggle="collapse" href="#collapse_Switches" aria-expanded="false" aria-controls="collapse_Switches">
                                                        Switches
                                                    </a>
                                                    <div class="collapse third-level" id="collapse_Switches">
                                                        <div class="well">
<ul>
    <li><a href="/Product%20Specification?family=Switches&amp;categories=Antenna%20Swap%20Switches;Antenna%20Swap%20Switches">Antenna Swap Switches</a></li>
    <li><a href="/Product%20Specification?family=Switches&amp;categories=Antenna%20Switch%20Modules;Antenna%20Switch%20Modules;Carrier%20Aggregation%20Switches;High%20Throw%20Count%20(%3E4T)%20Switches%20/%20Antenna%20Switch%20Modules%20(ASM)">Antenna Switch Modules</a></li>
    <li><a href="/Product%20Specification?family=Switches&amp;categories=Antenna%20Tuning%20Switches;Antenna%20Tuning%20Switches">Antenna Tuning Switches</a></li>
    <li><a href="/Product%20Specification?family=Switches&amp;categories=Carrier%20Aggregation%20Switches;Carrier%20Aggregation%20Switches">Carrier Aggregation</a></li>
    <li><a href="/Product%20Specification?family=Switches&amp;categories=Differential%20Receive%20Filter%20Switches;Differential%20Receive%20Filter%20Switches">Differential Receive Filter Switches</a></li>
    <li><a href="/Product%20Specification?family=Switches&amp;categories=DPDT%20Antenna%20Diversity%20Switches;DPDT%20Antenna%20Diversity%20Switches">DPDT Antenna Diversity Switches</a></li>
    <li><a href="/Product%20Specification?family=Switches&amp;categories=High%20Power%20SPDT%20and%20SPST%20PIN%20Diode%20Switches;High%20Power%20SPDT%20and%20SPST%20PIN%20Diode%20Switches">High Power SPDT And SPST Pin Diode Switches</a></li>
<!--    <li><a href="/Product%20Specification?family=Switches&amp;categories=High%20Reliability%20Switches;High%20Reliability%20Switches">High Reliability Switches</a></li>-->
    <li><a href="/Product%20Specification?family=Switches&amp;categories=Smart%20Coupler;Smart%20Coupler">Smart Coupler</a></li>
    <li><a href="/Product%20Specification?family=Switches&amp;categories=Band%20Distribution,%20General%20Purpose%20Signal%20Routing;Band%20Distribution,%20General%20Purpose%20Signal%20Routing;High%20Throw%20Count%20Switches%20(Band%20Distribution,%20Linear%20Tx/Rx,%20Rx%20Diversity,%20General%20Purpose%20Signal%20Routing);SP3T%20RF%20Switches;SP4T%20RF%20Switches;SPDT%20(SP2T)%20RF%20Switches;SPST%20RF%20Switches;Ultra%20Linear%20(SVLTE)%20Switches">Band Distribution &amp; General Purpose Switches</a></li>
</ul>
</div>
                                                    </div>
                                                </li>
                                                <li class="nav-item" role="presentation">
                                                    <!-- 2nd level mobile navigation with 3rd level -->
                                                    <a class="nav-link item-header-second collapsed" role="button" data-toggle="collapse" href="#collapse_TVAndVideo" aria-expanded="false" aria-controls="collapse_TVAndVideo">
                                                        TV And Video
                                                    </a>
                                                    <div class="collapse third-level" id="collapse_TVAndVideo">
                                                        <div class="well">
<ul>
    <li><a href="/en/Products/TV-and-Video-Digital-TV-and-Satellite-Demodulators">Digital TV And Satellite Demodulators</a></li>
    <li><a href="/en/Products/TV-and-Video-TV-Tuners">TV Tuners</a></li>
    <li><a href="/en/Products/TV-and-Video/Evaluation-Kits#collapseall">Evaluation Kits</a></li>
</ul>
</div>
                                                    </div>
                                                </li>
                                                <li class="nav-item" role="presentation">
                                                    <!-- 2nd level mobile navigation with 3rd level -->
                                                    <a class="nav-link item-header-second collapsed" role="button" data-toggle="collapse" href="#collapse_Voice" aria-expanded="false" aria-controls="collapse_Voice">
                                                        Voice
                                                    </a>
                                                    <div class="collapse third-level" id="collapse_Voice">
                                                        <div class="well">
<ul>
    <li><a href="/en/Products/Voice-ProSLIC-Voice-Solutions">ProSLIC Voice Solutions</a></li>
    <!--<li><a href="/en/Products/Voice/Si3000-Voice-Codecs">Si3000 Voice Codecs</a></li>-->
    <li><a href="/en/Products/Voice/Voice-DAAs">Voice DAAs</a></li>
    <li><a href="/en/Products/Voice/Evaluation-Kits">Evaluation Kits</a></li>
</ul>
</div>
                                                    </div>
                                                </li>

<li class="nav-item blue-item-mobile" role="presentation">
<a class="nav-link item-header-second collapsed " role="button" data-toggle="collapse" href="#collapseTechnologyStandards" aria-expanded="false" aria-controls="collapseTechnologyStandards">
Technology Standards
</a>
<div class="collapse third-level" id="collapseTechnologyStandards">
<div class="well">
<ul>
    <li><a href="/en/Technology-Standards/Bluetooth">Bluetooth</a></li>
    <!--<li><a href="#">Broadcast</a></li>-->
    <li><a href="/en/Technology-Standards/Cellular">Cellular</a></li>
    <li><a href="/en/Technology-Standards/GPS">GPS / GNSS</a></li>
    <li><a href="/en/Products/Timing-IEEE-1588-and-Synchronous-Ethernet">IEEE 1588</a></li>
    <li><a href="/en/Technology-Standards/LoRa">LoRa</a></li>
    <li><a href="/en/Application-Pages/PCI-Express-Learning-Center">PCI-Express</a></li>
    <li><a href="/en/products/Timing-SerDes">SerDes</a></li>
    <li><a href="/en/System-Solutions/Wi-Fi-Connectivity">Wi-Fi</a></li>
    <li><a href="/en/Technology-Standards/Wi-SUN">Wi-SUN</a></li>
    <li><a href="/en/Technology-Standards/Zigbee">Zigbee</a></li>
</ul>
</div>
</div>
</li>                                        </ul>
                                    </div>



                            </div>
    """

    soup = BeautifulSoup(html_content, "lxml")
    head_pro_node = soup.find("div", class_="head_pro flexlf")
    result = parse_product_categories(soup)
    print(json.dumps(result, indent=4, ensure_ascii=False))
    print(len(result))

    final_leaf_nodes = update_skyworks_result(result)
    # 打印最终结果
    print(f"\n===== 最终处理完成 =====")
    print(f"最终叶子节点总数：{len(final_leaf_nodes)}")
    for idx, node in enumerate(final_leaf_nodes, 1):
        print(f"{idx}. 分类：{node['category']}")
        print(f"   链接：{node['url']}\n")

    # 你的原有代码：final_leaf_nodes = update_skyworks_result(result)
    # =====================================
    # 新建空列表，用于存放更新后的节点（核心：用新列表替换原列表，实现节点更新）
    updated_leaf_nodes = []

    # 遍历原叶子节点，逐个处理
    for item in final_leaf_nodes:
        category = item["category"]
        url = item["url"]
        pageitemid_value = ""  # 初始化pageitemid

        # 你原有判断：url含family则打印，否则获取pageitemid
        if "family" in item["url"]:
            print("存在family", item["url"])
            # 含family的节点直接保留，加入新列表
            updated_leaf_nodes.append(item)
            continue
        else:
            try:
                # 发起请求（加请求头，避免反爬）
                time.sleep(1)
                response = requests.get(url, headers=HEADERS, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "lxml")

                # 获取pageitemid
                pageitemid_input = soup.find("input", id="pageitemid")
                pageitemid_value = pageitemid_input.get("value", "") if pageitemid_input else ""
                print(f"当前页面：{url}，pageitemid：{pageitemid_value if pageitemid_value else '空，解析下一层'}")

            except Exception as e:
                print(f"请求/解析{url}异常：{e}，保留原节点")
                # 异常情况直接保留原节点，加入新列表
                updated_leaf_nodes.append(item)
                continue

        # 核心判断：pageitemid有值 → 保留原节点
        if pageitemid_value:
            updated_leaf_nodes.append(item)
        # pageitemid无值 → 极简解析下一层（仅取h4产品名+对应url）
        else:
            try:
                # 重新请求页面（复用上面的soup，无需重复请求！）
                # 定位核心容器，找所有子分类a标签
                all_containers = soup.find_all("div", class_="col-sm-12 container-list")
                # 👉 修改2：初始化子a标签列表，存放所有容器的子链接
                all_sub_a_list = []
                # 👉 修改3：遍历所有容器，把每个容器的子a标签汇总到统一列表
                if all_containers:
                    for container in all_containers:
                        container_sub_a = container.find_all("a", class_="item-prod-family") if container else []
                        all_sub_a_list.extend(container_sub_a)
                    print(f"找到{len(all_containers)}个容器，共解析出{len(all_sub_a_list)}个下一层子节点，替换原节点")

                if all_sub_a_list:
                    print(f"找到{len(all_sub_a_list)}个下一层子节点，替换原节点")
                    # 遍历子a标签，仅提取h4产品名（如Si894x）+ 绝对URL
                    for sub_a in all_sub_a_list:
                        # 提取子分类名：仅取<h4>的内容（你要的Si892x/Si894x这种）
                        sub_cate = sub_a.find("h4").get_text(strip=True) if sub_a.find("h4") else "未知分类"
                        # 提取子URL并拼接为绝对地址
                        sub_href = sub_a.get("href", "").strip()
                        sub_url = f"{BASE_DOMAIN}{sub_href}" if sub_href and not sub_href.startswith("http") else url
                        # 生成子节点（分类名：原分类 > 子产品名，保持层级）
                        sub_item = {
                            "category": f"{category} > {sub_cate}",
                            "url": sub_url
                        }
                        # 子节点加入新列表（替换原节点）
                        updated_leaf_nodes.append(sub_item)
                else:
                    # 没找到下一层子节点，保留原节点
                    print(f"未找到下一层子节点，保留原节点：{url}")
                    updated_leaf_nodes.append(item)

            except Exception as e:
                print(f"解析下一层异常：{e}，保留原节点：{url}")
                updated_leaf_nodes.append(item)

    # 核心：用更新后的节点列表，覆盖原final_leaf_nodes（完成更新）
    final_leaf_nodes = updated_leaf_nodes
    # =====================================

    # （可选）打印更新后的最终节点，验证结果
    print(f"\n===== 节点更新完成，最终总数：{len(final_leaf_nodes)} =====")
    for idx, node in enumerate(final_leaf_nodes, 1):
        print(f"{idx}. 分类：{node['category']} | 链接：{node['url']}")

    base_path = "./seed_json"
    file_path = os.path.join(base_path, "skyworksinc.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(final_leaf_nodes, f, indent=2, ensure_ascii=False)