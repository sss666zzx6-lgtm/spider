from patchright.sync_api import sync_playwright
import time
import random
import os
from curl_cffi import requests


# def login_renesas():
#     with sync_playwright() as p:
#         # 1. 启动浏览器（设置代理、语言，模拟海外环境）
#         browser = p.chromium.launch(
#             headless=False,
#         )
#         # 设置浏览器语言为英文（适配外国网站）
#         context = browser.new_context()
#         page = context.new_page()
#
#         page.goto("https://www.renesas.com/en/oauth2/default/v1/authorize?client_id=0oa2ixjskq8o2hdJB357&response_type=code&scope=openid%20email%20phone%20profile%20MyRenesasUserInfo&redirect_uri=https%3A//www.renesas.com/openid-connect/renesas_okta&state=vemf_qRRQv1nzt2ZPIvBIkoSzJlCnKsOVlcIWSTZ4X0")
#
#         # # 定位按钮：用你截图里的文本“Log in to myInfineon”
#         # login_button_selector = 'text=Log in to myInfineon'
#         # page.wait_for_selector(login_button_selector, state='visible', timeout=20000)
#         # page.click(login_button_selector)
#         # print("✅ 已进入英飞凌首页并点击登录按钮")
#
#         #
#         input("\n浏览器已保持打开，按回车键关闭浏览器并退出脚本...")





def login_renesas():
    with sync_playwright() as p:
        # 使用系统安装的 Chrome，而不是 patchright 的 Chromium
        browser = p.chromium.launch(
            headless=False,
            channel='chrome',  # 使用系统 Chrome

        )

        context = browser.new_context(
        )

        # 添加反检测脚本
        context.add_init_script("""
            // 删除 webdriver 标志
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });

            // 添加插件
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });

            // 添加语言
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'zh', 'en']
            });

            // 伪造 chrome 对象
            window.chrome = {
                runtime: {},
                loadTimes: function() {},
                csi: function() {},
                app: {}
            };

            // 删除 automation 相关属性
            delete navigator.__proto__.webdriver;
        """)

        page = context.new_page()

        # 先访问主页，建立信任
        print("访问主页...")
        page.goto("https://www.renesas.cn/zh", wait_until='domcontentloaded')

        # 模拟人类行为：随机滚动
        for _ in range(3):
            page.mouse.move(random.randint(100, 800), random.randint(100, 600))
            time.sleep(random.uniform(0.5, 1.5))

        # 点击登录链接（如果有的话）或等待一段时间
        time.sleep(3)

        # 再访问登录页
        print("访问登录页...")
        login_url = "https://www.renesas.cn/zh/oauth2/default/v1/authorize?client_id=0oa2ixjskq8o2hdJB357&response_type=code&scope=openid%20email%20phone%20profile%20MyRenesasUserInfo&redirect_uri=https%3A//www.renesas.com/openid-connect/renesas_okta&state=YDnhah_khehgo1THWy6pW2xHKzZdkZ-aVvGWqcqwk3A"

        page.goto(login_url, wait_until='networkidle', timeout=60000)

        # 等待更长时间让 Cloudflare 验证
        time.sleep(5)

        # 截图查看状态
        page.screenshot(path='status.png')
        print("已截图保存为 status.png")

        print("页面标题:", page.title())
        print("当前URL:", page.url)

        input("\n按回车键关闭浏览器...")



def verify_cookie(cookie):
    headers = {
        # "cookie": """kapa_ab_group=control; nmstat=16dce3a3-2c23-15d2-1e61-a1736d3b5475; ELOQUA=GUID=D5880C96D8114262829A97FB0D0A1FD9; ren_usr_pr=0; notice_preferences=2:; notice_gdpr_prefs=0,1,2:; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3; _ga=GA1.1.252753382.1765965542; IDT-Language=zh; MkHcLang=zh-CN; MkHcCurrencyId=USD; notice_behavior=expressed,eu; _ALGOLIA=anonymous-3755666a-0b13-482f-bee3-4cef80c7daa9; Hm_lvt_b99db6af50ce7be250cabdfa36f447da=1768273379,1768464776,1768541212,1770721347; HMACCOUNT=045E38B63DFCF0FA; _clck=6prpxc%5E2%5Eg3h%5E0%5E2206; ELQCOUNTRY=CN; _ga_5JDBBP5TWD=GS2.1.s1770782282$o1$g0$t1770782282$j60$l0$h0; currentpath=/zh/support/document-search; TAsessionID=26ebf285-c4f6-4d81-a85c-652c04bcc592|EXISTING; _gcl_au=1.1.299705081.1765965542.427803347.1770788128.1770788127; myr=102-jzEmU6KS1Su-yw8-ovthw; sid=102-jzEmU6KS1Su-yw8-ovthw; xids=1021VJyYq3NQ0iwz8Qh700dPw; JSESSIONID=9F504AC50571D676D2CAE9D93EC72EDF; idx=eyJ6aXAiOiJERUYiLCJ2ZXIiOiIxIiwiYWxpYXMiOiJlbmNyeXB0aW9ua2V5Iiwib2lkIjoiMDBvMWNneDRvNHlBYXBZMmgzNTciLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiZGlyIiwieHNpZCI6ImlkeG4wcUgxcXFCVHFHdlNuMXB1anI4Y3cifQ..3hGujvolnYGimcd0.YjtQD3Ql3EDFZVAhufXurC3l9s4UtIQIqffvU1MF8E3QvEmQJPgi4Y09xAMuFPOZN09-3GPrpjmiek9DnrM9C9ixWgU_PQSJeRnIfKbhQmKYe1hZF9VXjCWn5PLvt7M_vv2njSiXzE-xxIQCXaMmAKArJiIgkMHvSLA7uvZc8r4dC3cLLfZiNDnw4_5BjYVU0DCsjIofUsaZU2B4mUjk-Pf1H6Z3dNWgZmDlIAL4pjcbWTS3UGHii4xLPjYeL1qDce_sLIi6uOzYhmrYG7BSx95ZdYvRV6UHYBnHKwqLMNpM1-NUA9NqbYHZcxv9VU7hbufkbRB59-rBh31eyfOqVpKCC_zlAdiW3CvEZM_0jGsqWXz1zSEj7fDi8Ya3SpqwEPV2AtBWcIYf-UgNEiO0yB6xq64qFeN89YoKZXv1EbzsQ-PvMRubues_GgYOz8cyRGk5eyMIzRx_MN-wai2FNRhW0Cmj40MZ4tI8XNglNQR8bWtX7wdvqeKJVRJoUZceiQM6Rx5Mzageyl4CnYaRth6Q0gNXkgtBhsdPNdje3vXTo5sY1uRaRl7SLtpNMD7CQR5mFQF8Zw0g9bDv4o-eTgZopAVlxE2RFF0YyO1hxLQN7x4GmXpGXl2f50GuwZFxtuoToVpV-XMxgVSkNG__cxX40aLd9giHoxfrfz2Y0K0xUiXDFisMIeysSfxesRct_SupjV1ORvsWHVU4HiSCxJUwkWXP2cxlu-ZlgGIPjWuG33ClNTMKJKdjIpjn-NeSZNSw9OlxOWLvZb6anWQH4QQzuU2ZWvt5xkztbz-EYGddHpp6KiiPvMzfXr3tVcBj_nL2Is_ajBT0dIDGmWisoxQPa6A98y3A2Krm1DP8UWWz86M3qQ7AQLzJWpd_2_HFP2KZoU-gV6_7PkiGmw595slwFwJLYGqVr1uzpDHkwvbbnA.pW91hHCtXClXXixCRdc-Lg; DT=DI1pIJ833EcQO22y7M2l60c4Q; proximity_400d32b72c8ba6f4d4a8984df2612eb0=eyJ6aXAiOiJERUYiLCJwMnMiOiJObk9OdzU4Q0lHR29WbGQ1WUV0ZmxRIiwicDJjIjoxMDAwLCJ2ZXIiOiIxIiwiZW5jIjoiQTI1NkdDTSIsImFsZyI6IlBCRVMyLUhTNTEyK0EyNTZLVyJ9._i0U8IRV39xF0cgP1W53TVNo1BemYQPPAJ1zIBWOrM9QRZxgX6OLxw.78ruqytMMty4uZmU.p33nIq_0TjicUwicbqhtJrusaE_WsxPlOEzThV4XFUuME-Ff29tffU9X3mDD4uF2tMnKjx71J4TaRDn7mPw0-j5pDJeeFOzFxzKaq2o7dx55bYHeFG77LvbzY81OY1dRQCF0RX52D3k-3yay8hECiRThorx6SJTpDdR69XaP57WURw.kfL6gIWiP-JqkqV7LU4nMQ; SSESSf924456a8134245645d3d9c6c79ad01a=snqbcae2onqpdqqbp5sg7nko27; uid=6930727; ldoc=25547336-en; referrer_path=/products/rbc220a75f3jws; Hm_lpvt_b99db6af50ce7be250cabdfa36f447da=1770788622; _uetsid=fcb290d0066f11f1924a456922007945; _uetvid=5b154240db2f11f09bdabd14e06f1c08; _clsk=da0mjv%5E1770788623386%5E18%5E1%5Ez.clarity.ms%2Fcollect; _ga_D1706WVDQV=GS2.1.s1770787935$o63$g1$t1770788639$j60$l0$h0; __cf_bm=YBEGf5qYeSnOtT3akfRLitUzR6lX_XDt6G3KWoHzHAk-1770788880-1.0.1.1-PlmohbnmHlhwd_cPq6dTf3wG5P2V7ARA09yTIK4WXbSJSMN73uT77s.cGzQkPPTlHL6sD.nTpqJ1GApMrZC..VoDMpa8E_u3LDcLXQ9zJzY""",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    }


    pdf_url = "https://www.renesas.cn/zh/document/dst/cl8060-datasheet"
    # cl8060
    save_path = "cl8060_datasheet.pdf"
    response = requests.get(
        pdf_url,
        headers=headers,
        # cookies=cookies,
        stream=True,
    )
    print(response)


if __name__ == "__main__":
    login_renesas()

