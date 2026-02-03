# -*- coding: utf-8 -*-
"""
@Time    : 2025/12/29 15:12
@Author  : Jason
@Ver     : Python3.13
"""
from typing import Dict
import requests

AK = "DS8StmIbggLY"
SK = "29a67a532b4245f774ae890cf1e6e731"
base_url = "https://darwin.lumychip.com"


def create_api(plan_id: str, path: str, custom_map: Dict,
               headers=None,
               http_request=None, request_body=None):
    api_link = f"{base_url}/api/auth/seed/add"
    data = {
        "url": path,
        "plan_id": plan_id,
        "access_key": AK,
        "secret_key": SK,
        "custom_map": custom_map,
        "timeout": 30000,
        # "normalize":False,
        "allow_dispatch": False,
    }
    if headers:
        data["headers"] = headers
    if http_request:
        data["http_request"] = http_request
    if request_body:
        data["request_body"] = request_body
    response = requests.put(api_link, json=data)
    print(response.text)

