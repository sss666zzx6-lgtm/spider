# cookie_keep_alive.py（保存路径：/home/your_user/cookie_keep_alive.py）
import requests
import json
import time
import os

# ===================== 配置项（替换为你的实际值）=====================
# 1. 基础配置
BASE_DIR = "/home/your_user"  # Linux上的绝对路径
COOKIE_FILE = f"{BASE_DIR}/persist_cookies.json"  # 持久化Cookie的文件
LOG_FILE = f"{BASE_DIR}/cookie_keep_alive.log"  # 日志文件
TARGET_DOMAIN = "https://www.silan.com.cn"  # 目标网站域名
# 2. 轻量刷新请求的URL（选网站首页/个人中心，无副作用的GET接口）
REFRESH_URL = f"{TARGET_DOMAIN}/en/index.php/product/index.html"
# 3. 首次登录配置（仅需执行1次）
LOGIN_URL = f"{TARGET_DOMAIN}/login"  # 实际登录接口
LOGIN_DATA = {  # 登录参数
    "username": "你的账号",
    "password": "你的密码"
}


# ===================== 工具函数：日志输出 =====================
def log(msg):
    """输出日志到文件，带时间戳"""
    log_msg = f"[{time.ctime()}] {msg}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_msg)
    print(log_msg.strip())


# ===================== 核心函数1：首次登录并保存Cookie =====================
def first_login():
    """仅需执行1次：登录并保存Cookie到文件"""
    if os.path.exists(COOKIE_FILE):
        log("Cookie文件已存在，无需首次登录（如需重新登录，请删除persist_cookies.json）")
        return

    try:
        session = requests.Session()
        # 发送登录请求（根据实际登录方式调整：data/json）
        resp = session.post(LOGIN_URL, data=LOGIN_DATA, timeout=15)
        resp.raise_for_status()

        # 保存Cookie到文件（持久化）
        cookies = session.cookies.get_dict()
        with open(COOKIE_FILE, "w", encoding="utf-8") as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)

        log(f"首次登录成功，Cookie已保存到 {COOKIE_FILE}")
    except Exception as e:
        log(f"首次登录失败：{str(e)}")
        raise


# ===================== 核心函数2：轻量刷新Cookie（无需重新登录）=====================
def refresh_cookie():
    """加载保存的Cookie，发送轻量请求刷新有效期，更新Cookie"""
    # 1. 加载本地Cookie
    if not os.path.exists(COOKIE_FILE):
        log("未找到Cookie文件，请先执行首次登录！")
        first_login()  # 兜底：若Cookie文件丢失，自动执行首次登录
        return

    try:
        with open(COOKIE_FILE, "r", encoding="utf-8") as f:
            saved_cookies = json.load(f)
    except Exception as e:
        log(f"加载Cookie文件失败：{str(e)}")
        return

    # 2. 创建Session，加载Cookie并发送轻量刷新请求
    session = requests.Session()
    session.cookies.update(saved_cookies)  # 加载保存的Cookie
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/144.0.0.0 Safari/537.36",
        "Referer": TARGET_DOMAIN  # 增加Referer，模拟正常访问
    })

    try:
        # 发送轻量GET请求（刷新Cookie有效期，无副作用）
        resp = session.get(REFRESH_URL, timeout=10)
        resp.raise_for_status()

        # 3. 更新Cookie文件（服务端可能返回新的Cookie）
        new_cookies = session.cookies.get_dict()
        with open(COOKIE_FILE, "w", encoding="utf-8") as f:
            json.dump(new_cookies, f, ensure_ascii=False, indent=2)

        log(f"Cookie刷新成功 | 状态码：{resp.status_code} | Cookie数量：{len(new_cookies)}")
    except Exception as e:
        log(f"Cookie刷新失败：{str(e)}")
        # 兜底：刷新失败时尝试重新登录（避免Cookie彻底过期）
        log("尝试重新登录...")
        first_login()


# ===================== 主函数 =====================
if __name__ == "__main__":
    # 执行刷新逻辑（首次运行时会自动执行首次登录）
    refresh_cookie()