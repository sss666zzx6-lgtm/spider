import requests
import json

from firstsilicon_add import category

if __name__ == '__main__':
    url = "https://www.wolfspeed.com/slice-data/HEADER-1773154614415.json"
    response = requests.get(url=url)
    print(response.json())
    print(response.status_code)
    category = []
    response_json = response.json()

    result = response_json.get("result", {})  # 取result，默认空字典
    data = result.get("data", {})  # 取data，默认空字典
    navigation = data.get("navigation", {})  # 取navigation，默认空字典
    nodes = navigation.get("nodes", [])

    for node in nodes:
        languageCode = node.get("languageCode")
        if languageCode == "en":
            components = node.get("components", {})
            mainMenu = components.get("mainMenu", [])
            for main in mainMenu:
                dropdownLabel = main.get("dropdownLabel")
                if dropdownLabel == "Products":
                    subNavItems = main.get("subNavItems", [])
                    for subNavItem in subNavItems:
                        linkLabel = subNavItem.get("linkLabel")
                        linkUrl = subNavItem.get("linkUrl")
                        if linkLabel == "Reference Designs":
                            break
                        else:
                            category.append({
                                "category": linkLabel,
                                "url": linkUrl,
                            })

    print(json.dumps(category, indent=2, ensure_ascii=False))
    file_path = "wolfspeed.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(category, f, indent=2, ensure_ascii=False)