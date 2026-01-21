from fake_useragent import UserAgent
import random

def get_random_ua():
    """获取随机User-Agent（带异常兜底）"""
    try:
        # 初始化UA对象，自动缓存最新UA列表
        ua = UserAgent()
        # 随机选择：可选chrome/firefox/safari/edge/mobile等类型
        return random.choice([
            ua.chrome,    # Chrome浏览器
            # ua.firefox,   # Firefox浏览器
            # ua.safari,    # Safari浏览器
            # ua.edge,      # Edge浏览器
        ])
    except Exception as e:
        # 网络失败时，用手动UA兜底（避免程序崩溃）
        print(f"获取UA失败：{e}，使用兜底UA")
        fallback_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        return fallback_ua

# 测试使用
if __name__ == "__main__":
    random_ua = get_random_ua()
    print("随机UA：", random_ua)