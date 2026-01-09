# import requests
#
#
# url = "https://www.infineon.com/part/TLE9012DQU"
# response = requests.get(url)
#
# print(response.text)
# print(response)


import requests
import hashlib
import ceshi
import time


def solve_pow_challenge(base, target_hash):
    """
    解决pow挑战：找到answer使得sha256(base + answer) <= target_hash
    """
    target_int = int(target_hash, 16)

    # 尝试从0开始递增
    for answer in range(1000000):  # 限制尝试次数
        test_str = base + str(answer)
        hash_result = hashlib.sha256(test_str.encode()).hexdigest()

        if int(hash_result, 16) <= target_int:
            print(f"找到答案: {answer}, 哈希: {hash_result}")
            return str(answer)

    return None


def get_cookie_with_pow():
    # 第一次请求：获取挑战
    url = "https://www.monolithicpower.com/_fs-ch-1T1wmsGaOgGaSxcX/fst-post-back"

    # 初始载荷
    initial_payload = {
        "token": "AbgMmh3uAMYXQMqUyO_eZ5eGZ4DPj6wWFBsCrIPxeLqm2Qqs3IpE14N5j7jytcPnf242UxjVWfo9x3SkEum3-WQ9C2GlZqPXLPv7chQiRm-IcMhSm3kdCnJ5nRBRTkEL_Y6-lRyPlAxChiBjWnQE37GRRqR5cYUl_3RawtdEFC_SpxqSyU9B3855zyJg9dHqt6BndCvvmi3Jj9sSHP6n3T87rD2qp0CBSikS-hsOsWXxZhXIVnsPXQbhMbE9jIA--xwxEnVL9h61heYVftoKynipzC1gcPXYHLVEZcqUacX7el7JrtFBa1JDf992lAF5tR8FgoPYKSRnI8dCLvDDUCPEogKqad_ImB_nGSGPrQNls2YTTcNdQT1JCgZK5WBaVXXDal96MNkQAadisgI-1IFcQXupWgYLATFg8A8NX_Jpqn5L",
        "data": [
            {
                "ty": "pow",
                "base": "gYvAZCT5WijdsOQp",
                "answer": "tl",
                "hmac": "e6c33bb5197ccf9718e2c6807557de91b49ca9f15dd79c2ac9a5783a1937cc55",
                "expires": "1766744021"
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    print("发送第一次请求...")
    response = requests.post(url, json=initial_payload, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        print("第一次响应:", json.dumps(response_data, indent=2))

        # 提取挑战数据
        if "ch" in response_data and len(response_data["ch"]) > 0:
            challenge = response_data["ch"][0]
            if challenge["ty"] == "pow":
                base = challenge["data"]["base"]
                target_hash = challenge["data"]["hash"]
                hmac = challenge["data"]["hmac"]
                expires = challenge["data"]["expires"]
                token = response_data["tok"]

                print(f"\n获取到pow挑战:")
                print(f"base: {base}")
                print(f"target_hash: {target_hash}")
                print(f"hmac: {hmac}")
                print(f"expires: {expires}")
                print(f"token: {token[:50]}...")

                # 解决pow挑战
                print("\n开始计算pow答案...")
                start_time = time.time()
                answer = solve_pow_challenge(base, target_hash)
                end_time = time.time()

                if answer:
                    print(f"计算完成! 耗时: {end_time - start_time:.2f}秒")

                    # 第二次请求：提交答案获取cookie
                    second_payload = {
                        "token": token,
                        "data": [
                            {
                                "ty": "pow",
                                "base": base,
                                "answer": answer,
                                "hmac": hmac,
                                "expires": expires
                            }
                        ]
                    }

                    print("\n发送第二次请求获取cookie...")
                    second_response = requests.post(url, json=second_payload, headers=headers)

                    if second_response.status_code == 200:
                        print(f"第二次响应状态码: {second_response.status_code}")

                        # 检查是否有Set-Cookie
                        if 'Set-Cookie' in second_response.headers:
                            set_cookie = second_response.headers['Set-Cookie']
                            print(f"\n成功获取Set-Cookie:")
                            print(set_cookie)

                            # 提取特定cookie
                            cookie_name = "_fs_ch_cp_79UUvfpJ5mWYtLQv"
                            if cookie_name in set_cookie:
                                cookie_start = set_cookie.find(cookie_name) + len(cookie_name) + 1
                                cookie_end = set_cookie.find(";", cookie_start)
                                cookie_value = set_cookie[cookie_start:cookie_end]
                                print(f"\n提取的 {cookie_name}: {cookie_value}")
                                return cookie_value
                            else:
                                print(f"未找到 {cookie_name} cookie")
                        else:
                            print("第二次响应中未找到Set-Cookie")
                            print("响应头:", dict(second_response.headers))
                            print("响应内容:", second_response.text)
                    else:
                        print(f"第二次请求失败，状态码: {second_response.status_code}")
                else:
                    print("未能解决pow挑战")
            else:
                print(f"挑战类型不是pow: {challenge['ty']}")
        else:
            print("响应中没有挑战数据")
    else:
        print(f"第一次请求失败，状态码: {response.status_code}")

    return None


# 运行
if __name__ == "__main__":
    cookie = get_cookie_with_pow()
    if cookie:
        print(f"\n最终获取的cookie值: {cookie}")
    else:
        print("未能获取cookie")



