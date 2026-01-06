import requests


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "Cache-Control": "no-cache",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
}
cookies = {
    "ai_user": "6Wk8jId5aNtncMBY/8u6by|2025-12-15T03:52:09.687Z",
    "AMCV_936D1C8B532955E20A490D4D%40AdobeOrg": "MCMID|56699349493087147082767729761020801187",
    "OptanonAlertBoxClosed": "2025-12-15T03:52:24.972Z",
    "kndctr_936D1C8B532955E20A490D4D_AdobeOrg_consent": "general%3Din",
    "s_inv": "0",
    "dmdbase": "isp%20visitor%7Cisp%20visitor%7Cisp%20visitor%7Cbot%7Cisp%20visitor%7Cisp%20visitor%7Cisp%20visitor%7Cisp%20visitor%7Cisp%20visitor%7Cisp%20visitor%7Cisp%20visitor",
    "AKA_A2": "A",
    "bm_ss": "ab8e18ef4e",
    "_ALGOLIA": "anonymous-3e047f74-56ff-40be-ada2-927382f5d1d4",
    "mboxEdgeCluster": "32",
    "kndctr_936D1C8B532955E20A490D4D_AdobeOrg_identity": "CiY1NjY5OTM0OTQ5MzA4NzE0NzA4Mjc2NzcyOTc2MTAyMDgwMTE4N1ITCOqaiIGyMxABGAEqBEpQTjMwAPAB1pKN1rIz",
    "kndctr_936D1C8B532955E20A490D4D_AdobeOrg_cluster": "jpn3",
    "s_vnc365": "1797306746314&vn=2",
    "s_ivc": "true",
    "ab.storage.deviceId.f84605d7-94fc-4b32-85e1-1714d5b1624b": "g%3A59408b93-14b3-64b2-4e29-500752aee810%7Ce%3Aundefined%7Cc%3A1765949019221%7Cl%3A1765949019221",
    "shell#lang": "en",
    "FedAuthentication": "UserGeoIPCountry=&UserGeoIpMarket=&UserGeoIpAccount=&UserGeoIpSubIndustry=&Audience=&AudienceSegment=&City=&State=&Fortune1000=&AnnualSales=",
    "_gcl_au": "1.1.1022835588.1765950066",
    "QSI_HistorySession": "https%3A%2F%2Fwww.analog.com%2Fcn%2Fproduct-category%2Fpower.html~1765949029072%7Chttps%3A%2F%2Fwww.analog.com%2Fcn%2Fproduct-category%2Fled-drivers.html~1765949033743%7Chttps%3A%2F%2Fwww.analog.com%2Fcn%2Fproduct-category%2Fbattery-management.html~1765949196168%7Chttps%3A%2F%2Fwww.analog.com%2Fcn%2Fproducts%2Fadbms2950b.html~1765949209639%7Chttps%3A%2F%2Fwww.analog.com%2Fcn%2Fresources%2Fevaluation-hardware-and-software%2Fevaluation-boards-kits%2Feval-ess1-sys.html~1765949326856%7Chttps%3A%2F%2Fwww.analog.com%2Fcn%2Fresources%2Fevaluation-hardware-and-software%2Fevaluation-boards-kits%2Feval-adbms2950-basic%2Fsample-buy.html~1765949364719%7Chttps%3A%2F%2Fwww.analog.com%2Fcn%2Findex.html~1765949958904%7Chttps%3A%2F%2Fwww.analog.com%2Fcn%2Fproduct-category%2Fpower.html%23subcategories~1765949976768%7Chttps%3A%2F%2Fwww.analog.com%2Fcn%2Fparametricsearch%2F2458~1765950007605%7Chttps%3A%2F%2Fwww.analog.com%2Fcn%2Fproduct-category%2Fpower.html~1765950031476%7Chttps%3A%2F%2Fwww.analog.com%2Fcn%2Fproduct-category%2Fbattery-management.html~1765950044952%7Chttps%3A%2F%2Fwww.analog.com%2Fcn%2Fparametricsearch%2F3675~1765950048914%7Chttps%3A%2F%2Fwww.analog.com%2Fen%2Fproduct-category%2Factive-filters.html~1765950103655%7Chttps%3A%2F%2Fwww.analog.com%2Fen%2Fparametricsearch%2F2391%23%2F~1765950110401%7Chttps%3A%2F%2Fwww.analog.com%2Fen%2Fproduct-category%2Factive-filters.html~1765950130725%7Chttps%3A%2F%2Fwww.analog.com%2Fcn%2Fparametricsearch%2F3675%23%2F~1765950157193%7Chttps%3A%2F%2Fwww.analog.com%2Fen%2Fparametricsearch%2F2391%23%2F~1765950231959%7Chttps%3A%2F%2Fwww.analog.com%2Fcn%2Fproduct-category%2Fbattery-management.html~1765950328309%7Chttps%3A%2F%2Fwww.analog.com%2Fen%2Findex.html~1765950866520%7Chttps%3A%2F%2Fwww.analog.com%2Fen%2Fproduct-category%2Famplifiers.html~1765950878595%7Chttps%3A%2F%2Fwww.analog.com%2Fen%2Fparametricsearch%2F2391%23%2F~1765950900003%7Chttps%3A%2F%2Fwww.analog.com%2Fen%2Fproduct-category%2Famplifiers.html~1765950973686",
    "bm_so": "07EE88A5CF49B54E26DC5739257532D01007BA7E1CC693FABDFD7C75B235CD6D~YAAQDoyUG31ECtSaAQAAME/iKgaMwxqFJybPKqrSHL+3YyEfcgtVtsSDeMSFFCoCwzyZ6TUyuOLoWFbCZTyd8Pf7OCXjCSE2IMFqC9kFH6Rw2VHfPGZe+LHHMEM3rYQfsyDuTVyhKrJfMqX47yvDMR+sMBRiR4wgwwR326viVWCFrKq+wPshtGkU8RSETKaUWmxILWQhhzilTKC7IKhyVM//rdB4nsA6uqciup/7A04yBr51j3/YuPk6ReWN6E096E8JrG94uhyFYtlMkPSfGo9WyLGIPPQl2v4tydJGIAh9ha/+LFmPjxrt6C4uAo7+lVIoqdexw+cADy2UkqX4RjZt4A9zsB+cHGtpbj1fa1QDFIJ3LBYUwizRjKUBQMmDzsP9Q/NvKvGNynJ8pur61FH9p6iljINoMj7MROq4gTT2UW7RFh0a7DyuAM2c780+accGhN315k51vFJghuX7",
    "bm_lso": "07EE88A5CF49B54E26DC5739257532D01007BA7E1CC693FABDFD7C75B235CD6D~YAAQDoyUG31ECtSaAQAAME/iKgaMwxqFJybPKqrSHL+3YyEfcgtVtsSDeMSFFCoCwzyZ6TUyuOLoWFbCZTyd8Pf7OCXjCSE2IMFqC9kFH6Rw2VHfPGZe+LHHMEM3rYQfsyDuTVyhKrJfMqX47yvDMR+sMBRiR4wgwwR326viVWCFrKq+wPshtGkU8RSETKaUWmxILWQhhzilTKC7IKhyVM//rdB4nsA6uqciup/7A04yBr51j3/YuPk6ReWN6E096E8JrG94uhyFYtlMkPSfGo9WyLGIPPQl2v4tydJGIAh9ha/+LFmPjxrt6C4uAo7+lVIoqdexw+cADy2UkqX4RjZt4A9zsB+cHGtpbj1fa1QDFIJ3LBYUwizRjKUBQMmDzsP9Q/NvKvGNynJ8pur61FH9p6iljINoMj7MROq4gTT2UW7RFh0a7DyuAM2c780+accGhN315k51vFJghuX7~1765951033666",
    "sxa_site": "AnalogWeb-CN",
    "ak_bmsc": "F4AEC52404AEF51BFAAA376082C0AF70~000000000000000000000000000000~YAAQPD8uF+7N9iWbAQAAgH/iKh5T0ICA9ZiHvwFkPCY6/IJ0UzSNO2SRXKoYdAznQtDkFfowXNNB7JiYLKyrXatqLPhCPTtqH+XRmkXUv8ShL3/PcFHdMB6fb/tZMa2JXYDqOSiNt4rXRKgEMhK4Rx/7MqKlCmCd6Byj+Iz/bHhStxRrA5FnsaNPbsgQ3HuEm4QrDmly31Cr0FrI0KlwRVjJJDrAsBbpaNbIgrTJBiQoGVW8UgyF760g60XibU1pxz7GzffwDuvireqCyAVcjjgusrOxtQOHIyvvvDptPchsu9PN4sBo2AU6GfFZ1WaWyfnwM9BowYLL3TFArftq8yA0APzakuQ3W2LOoJg=",
    "bm_s": "YAAQDoyUGwBLCtSaAQAAv4DiKgQf6qL/EDPKodt75++VTOPa2O4dVMKgdBoHaPOjae+zFnQcxr0rI9zWa4W9vfExXj/WVGvOl9tFIR0U9WJ54NuiENLHsSquodkDydP+AhrVgBzz5mrXnIC4pv7wc9sIVRTZJcL3KBTJuZffQrwvj/XTQ3Wn5ms5Xc9Eyyx762nlo+qeGKrFdqwtp9ctqv8vOjaCWMO5Mx+ou8kPbYqEhuZyJNZkJImNzsxZ54IZjNEsLWenylGwMrefZ6s584tTCzaawkFQBOs+9LzQ2Q+0oFyl1F2F5R3XGHBB8qrjqUzR7uiZ+T/Y1Zb/FJhp/SwHPagUJIxx3IiA4Zl9SsAyIQzhHO4StvoXwshIsAJuXTBgiqiKOOlxEXUz7z01b52F4bsyoJsQ4PangSE0zaFvgPLYiDodJdkc2l8FDnB/fMEJrWa0O2VHJL2aspsE3YfvsYEsmM6nDlQ9wVO8hgjLC2f4XR0hkFVJChmOB1k6JsaHMYGS7ws7hGa6k4rciqyPKnr8NqvHW2DnEI6Ae/OW+sHsgDloV+KPe4fwvjm+LD5tUm4aUA==",
    "mbox": "session%2356699349493087147082767729761020801187%2DUulLuJ%231765952906",
    "ai_session": "5nmOHEg/f6Wyk/2H7mu9rQ|1765948997616|1765951045450",
    "OptanonConsent": "isGpcEnabled=0&datestamp=Wed+Dec+17+2025+13%3A57%3A25+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202307.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=41be4d82-7e1e-45df-ba41-e32e5940b1b7&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&geolocation=JP%3B13&AwaitingReconsent=false",
    "s_tslv": "1765951049441",
    "ab.storage.sessionId.f84605d7-94fc-4b32-85e1-1714d5b1624b": "g%3A862b9029-1110-fcb6-8408-c82614ae3103%7Ce%3A1765952850016%7Cc%3A1765949019219%7Cl%3A1765951050016",
    "cto_bundle": "ISdgsV9ocDJWYXIxeUhobmttclFNVVFwa1JkcGdIamJ6SXZublUxRFppZTlaWTg0UVhoa1UlMkJwYjRoVmgzMTQ4Qlpta3VNSzRrJTJCcUc5WU5KN2lTTzlkeEVKUG1PMjJ0V0ptY1F1bjA1N2RFbkZEV0dXRTBXVnl3dTJUUFB4cFU1UzRSaEswMDgxcDklMkIzQ0NkaXhlbSUyRkQ2QTA0QSUzRCUzRA",
    "_abck": "0724C014F3E1DB6CB443C75218DD2D4B~-1~YAAQPD8uF5fS9iWbAQAAStjiKg8J1nVTHG6Rukn/NW0f/IMqYvOTv8NWWNOqDUsMYMZOg/tIwdsxVh0YINq2MCOv01mx5P5kCKwHVuSoCFEa76saSQfmxeqsiVTgJascmOwjEYC9f/1fgqNwOHI9U7/qvOQX8d0vSb42CkD188I/CNx+vWOHtB4mYbDIeynV9i+1fvxZoubHxSYKyptbdKDpYFCPY5dquabqfVfvUpBO6tSyIZHq0KFkYMSlSoF3+WMXs2eNol/y7qSymyR4VKYdKdYvqHUZ/KLYCdrV9bcB90xGd5PuBx2+Ikb0E8vtIcgx2J7fxnou7M88Gx9NFsSheyGQLBcrmD5haWE7ETp39uXErB3jilfwbbVG8Ui2t2WTJ+DrEaP+ymlDhwPldExY/d7sR1BDxgbSlmRzbNJ7qHs4fwmxMdDckId9MmR4em0VWN5JLsA=~-1~-1~-1~-1~-1",
    "bm_sz": "0266839993C5F57B25182128F59ADD9F~YAAQPD8uF5jS9iWbAQAAStjiKh5wf83ejwf8CO4rSpDs+4qGfV3Mp8JY7gUSzVcChKg6XtTxerr6HKNlIv9D4DzI55HsZX3VT32JRxwmNXJX/RQMNWrSqxZTfrP9kdnSaW98d0wkchGncwqmo2tVCO6tSzeUU6jv9faxn8ykMnNYnrpul8pums8o5Kb4t9gm84UzR14BL5RKwOhO5Qbx/2BH2qqJc0nKtliwpH5FOOdnr/CRkEFlxPC01x5pxFkzDwVU1zj135pkLVL+PKGS1rur0c5G17RwPdBKTu2f+VFpoy05tWjlcuJRiNGdWD5iYDjX9FI9eICZv0z343K18eYlVw/g/jCf4zVLaAHY~4536642~3290928",
    "bm_sv": "9F31E5BB1510B0657BE6AE6F3E35A38F~YAAQDoyUG4FXCtSaAQAAYtniKh67rons7URTeGSgSLUoktk089x20zcK6pZd1sUd14YRzVlg8v/MF28sWm9GUGM6n64/F1p+4N+30TSbRULhtD1dINcLL4WKUO5coWhY0jG3PTB+pSaB4sscw+80TVYGuXHybf/Cg8j44lxZbp51rLcgaDmegWzZVXEkjh6E/1KCXEL9Yn0X1v/4hd7gLoIrX3yZHoi1EUWaX9wuoYQvkF7IzV/c3rHVLAhadbvAb08=~1",
    "RT": "\"z=1&dm=www.analog.com&si=886343a4-80cb-4e82-8674-e232cadd72dc&ss=mj9kk7t5&sl=3&tt=165m&bcn=%2F%2F684d0d42.akstat.io%2F&ld=13e74&ul=14295\""
}
url = "https://www.analog.com/en/products/ADH675S.html"
response = requests.get(url, headers=headers)

print(response.text)
print(response)

# res = requests.get('https://www.analog.com/cdp/ecommdata/en/ADA4620-2.js?v99')
# print(res.json())



# a = {
#     "countries": [
#         {
#             "key": "UNITED STATES",
#             "value": "US"
#         },
#         {
#             "key": "AFGHANISTAN",
#             "value": "AF"
#         },
#         {
#             "key": "ALAND ISLANDS",
#             "value": "AX"
#         },
#         {
#             "key": "ALBANIA",
#             "value": "AL"
#         },
#         {
#             "key": "ALGERIA",
#             "value": "DZ"
#         },
#         {
#             "key": "AMERICAN SAMOA",
#             "value": "AS"
#         },
#         {
#             "key": "ANDORRA",
#             "value": "AD"
#         },
#         {
#             "key": "ANGOLA",
#             "value": "AO"
#         },
#         {
#             "key": "ANGUILLA",
#             "value": "AI"
#         },
#         {
#             "key": "ANTARCTICA",
#             "value": "AQ"
#         },
#         {
#             "key": "ANTIGUA AND BARBUDA",
#             "value": "AG"
#         },
#         {
#             "key": "ARGENTINA",
#             "value": "AR"
#         },
#         {
#             "key": "ARMENIA",
#             "value": "AM"
#         },
#         {
#             "key": "ARUBA",
#             "value": "AW"
#         },
#         {
#             "key": "AUSTRALIA",
#             "value": "AU"
#         },
#         {
#             "key": "AUSTRIA",
#             "value": "AT"
#         },
#         {
#             "key": "AZERBAIJAN",
#             "value": "AZ"
#         },
#         {
#             "key": "BAHAMAS",
#             "value": "BS"
#         },
#         {
#             "key": "BAHRAIN",
#             "value": "BH"
#         },
#         {
#             "key": "BANGLADESH",
#             "value": "BD"
#         },
#         {
#             "key": "BARBADOS",
#             "value": "BB"
#         },
#         {
#             "key": "BELGIUM",
#             "value": "BE"
#         },
#         {
#             "key": "BELIZE",
#             "value": "BZ"
#         },
#         {
#             "key": "BENIN",
#             "value": "BJ"
#         },
#         {
#             "key": "BERMUDA",
#             "value": "BM"
#         },
#         {
#             "key": "BHUTAN",
#             "value": "BT"
#         },
#         {
#             "key": "BOLIVIA",
#             "value": "BO"
#         },
#         {
#             "key": "BOSNIA AND HERZEGOVINA",
#             "value": "BA"
#         },
#         {
#             "key": "BOTSWANA",
#             "value": "BW"
#         },
#         {
#             "key": "BOUVET ISLAND",
#             "value": "BV"
#         },
#         {
#             "key": "BRAZIL",
#             "value": "BR"
#         },
#         {
#             "key": "BRITISH INDIAN OCEAN TERRITORY",
#             "value": "IO"
#         },
#         {
#             "key": "BRUNEI DARUSSALAM",
#             "value": "BN"
#         },
#         {
#             "key": "BULGARIA",
#             "value": "BG"
#         },
#         {
#             "key": "BURKINA FASO",
#             "value": "BF"
#         },
#         {
#             "key": "BURUNDI",
#             "value": "BI"
#         },
#         {
#             "key": "CAMBODIA",
#             "value": "KH"
#         },
#         {
#             "key": "CAMEROON",
#             "value": "CM"
#         },
#         {
#             "key": "CANADA",
#             "value": "CA"
#         },
#         {
#             "key": "CAPE VERDE",
#             "value": "CV"
#         },
#         {
#             "key": "CAYMAN ISLANDS",
#             "value": "KY"
#         },
#         {
#             "key": "CENTRAL AFRICAN REPUBLIC",
#             "value": "CF"
#         },
#         {
#             "key": "CHAD",
#             "value": "TD"
#         },
#         {
#             "key": "CHILE",
#             "value": "CL"
#         },
#         {
#             "key": "CHINA",
#             "value": "CN"
#         },
#         {
#             "key": "CHRISTMAS ISLAND",
#             "value": "CX"
#         },
#         {
#             "key": "COCOS ISLANDS",
#             "value": "CC"
#         },
#         {
#             "key": "COLOMBIA",
#             "value": "CO"
#         },
#         {
#             "key": "COMOROS",
#             "value": "KM"
#         },
#         {
#             "key": "CONGO",
#             "value": "CG"
#         },
#         {
#             "key": "CONGO, THE DEMOCRATIC REPUBLIC OF THE",
#             "value": "CD"
#         },
#         {
#             "key": "COOK ISLANDS",
#             "value": "CK"
#         },
#         {
#             "key": "COSTA RICA",
#             "value": "CR"
#         },
#         {
#             "key": "COTE D'IVOIRE",
#             "value": "CI"
#         },
#         {
#             "key": "CROATIA",
#             "value": "HR"
#         },
#         {
#             "key": "CYPRUS",
#             "value": "CY"
#         },
#         {
#             "key": "CZECH REPUBLIC",
#             "value": "CZ"
#         },
#         {
#             "key": "DENMARK",
#             "value": "DK"
#         },
#         {
#             "key": "DJIBOUTI",
#             "value": "DJ"
#         },
#         {
#             "key": "DOMINICA",
#             "value": "DM"
#         },
#         {
#             "key": "DOMINICAN REP.",
#             "value": "DO"
#         },
#         {
#             "key": "ECUADOR",
#             "value": "EC"
#         },
#         {
#             "key": "EGYPT",
#             "value": "EG"
#         },
#         {
#             "key": "EL SALVADOR",
#             "value": "SV"
#         },
#         {
#             "key": "EQUATORIAL GUINEA",
#             "value": "GQ"
#         },
#         {
#             "key": "ERITREA",
#             "value": "ER"
#         },
#         {
#             "key": "ESTONIA",
#             "value": "EE"
#         },
#         {
#             "key": "ETHIOPIA",
#             "value": "ET"
#         },
#         {
#             "key": "FALKLAND ISLANDS (MALVINAS)",
#             "value": "FK"
#         },
#         {
#             "key": "FAROE ISLANDS",
#             "value": "FO"
#         },
#         {
#             "key": "FIJI",
#             "value": "FJ"
#         },
#         {
#             "key": "FINLAND",
#             "value": "FI"
#         },
#         {
#             "key": "FRANCE",
#             "value": "FR"
#         },
#         {
#             "key": "FRENCH GUIANA",
#             "value": "GF"
#         },
#         {
#             "key": "FRENCH POLYNESIA",
#             "value": "PF"
#         },
#         {
#             "key": "FRENCH SOUTHERN TERRITORIES",
#             "value": "TF"
#         },
#         {
#             "key": "GABON",
#             "value": "GA"
#         },
#         {
#             "key": "GAMBIA",
#             "value": "GM"
#         },
#         {
#             "key": "GEORGIA",
#             "value": "GE"
#         },
#         {
#             "key": "GERMANY",
#             "value": "DE"
#         },
#         {
#             "key": "GHANA",
#             "value": "GH"
#         },
#         {
#             "key": "GIBRALTAR",
#             "value": "GI"
#         },
#         {
#             "key": "GREECE",
#             "value": "GR"
#         },
#         {
#             "key": "GREENLAND",
#             "value": "GL"
#         },
#         {
#             "key": "GRENADA",
#             "value": "GD"
#         },
#         {
#             "key": "GUADELOUPE",
#             "value": "GP"
#         },
#         {
#             "key": "GUAM",
#             "value": "GU"
#         },
#         {
#             "key": "GUATEMALA",
#             "value": "GT"
#         },
#         {
#             "key": "GUERNSEY",
#             "value": "GG"
#         },
#         {
#             "key": "GUINEA",
#             "value": "GN"
#         },
#         {
#             "key": "GUINEA-BISSAU",
#             "value": "GW"
#         },
#         {
#             "key": "GUYANA",
#             "value": "GY"
#         },
#         {
#             "key": "HAITI",
#             "value": "HT"
#         },
#         {
#             "key": "HEARD ISLAND AND MCDONALD ISLANDS",
#             "value": "HM"
#         },
#         {
#             "key": "HONDURAS",
#             "value": "HN"
#         },
#         {
#             "key": "HONG KONG",
#             "value": "HK"
#         },
#         {
#             "key": "HUNGARY",
#             "value": "HU"
#         },
#         {
#             "key": "ICELAND",
#             "value": "IS"
#         },
#         {
#             "key": "INDIA",
#             "value": "IN"
#         },
#         {
#             "key": "INDONESIA",
#             "value": "ID"
#         },
#         {
#             "key": "IRELAND",
#             "value": "IE"
#         },
#         {
#             "key": "ISLE OF MAN",
#             "value": "IM"
#         },
#         {
#             "key": "ISRAEL",
#             "value": "IL"
#         },
#         {
#             "key": "ITALY",
#             "value": "IT"
#         },
#         {
#             "key": "JAMAICA",
#             "value": "JM"
#         },
#         {
#             "key": "JAPAN",
#             "value": "JP"
#         },
#         {
#             "key": "JERSEY",
#             "value": "JE"
#         },
#         {
#             "key": "JORDAN",
#             "value": "JO"
#         },
#         {
#             "key": "KAZAKHSTAN",
#             "value": "KZ"
#         },
#         {
#             "key": "KENYA",
#             "value": "KE"
#         },
#         {
#             "key": "KIRIBATI",
#             "value": "KI"
#         },
#         {
#             "key": "KUWAIT",
#             "value": "KW"
#         },
#         {
#             "key": "KYRGYZSTAN",
#             "value": "KG"
#         },
#         {
#             "key": "LAOS",
#             "value": "LA"
#         },
#         {
#             "key": "LATVIA",
#             "value": "LV"
#         },
#         {
#             "key": "LEBANON",
#             "value": "LB"
#         },
#         {
#             "key": "LESOTHO",
#             "value": "LS"
#         },
#         {
#             "key": "LIBERIA",
#             "value": "LR"
#         },
#         {
#             "key": "LIBYA",
#             "value": "LY"
#         },
#         {
#             "key": "LIECHTENSTEIN",
#             "value": "LI"
#         },
#         {
#             "key": "LITHUANIA",
#             "value": "LT"
#         },
#         {
#             "key": "LUXEMBOURG",
#             "value": "LU"
#         },
#         {
#             "key": "MACAO",
#             "value": "MO"
#         },
#         {
#             "key": "MACEDONIA",
#             "value": "MK"
#         },
#         {
#             "key": "MADAGASCAR",
#             "value": "MG"
#         },
#         {
#             "key": "MALAWI",
#             "value": "MW"
#         },
#         {
#             "key": "MALAYSIA",
#             "value": "MY"
#         },
#         {
#             "key": "MALDIVES",
#             "value": "MV"
#         },
#         {
#             "key": "MALI",
#             "value": "ML"
#         },
#         {
#             "key": "MALTA",
#             "value": "MT"
#         },
#         {
#             "key": "MARSHALL ISLANDS",
#             "value": "MH"
#         },
#         {
#             "key": "MARTINIQUE",
#             "value": "MQ"
#         },
#         {
#             "key": "MAURITANIA",
#             "value": "MR"
#         },
#         {
#             "key": "MAURITIUS",
#             "value": "MU"
#         },
#         {
#             "key": "MAYOTTE",
#             "value": "YT"
#         },
#         {
#             "key": "MEXICO",
#             "value": "MX"
#         },
#         {
#             "key": "MICRONESIA, FEDERATED STATES OF",
#             "value": "FM"
#         },
#         {
#             "key": "MOLDOVA",
#             "value": "MD"
#         },
#         {
#             "key": "MONACO",
#             "value": "MC"
#         },
#         {
#             "key": "MONGOLIA",
#             "value": "MN"
#         },
#         {
#             "key": "MONTENEGRO",
#             "value": "ME"
#         },
#         {
#             "key": "MONTSERRAT",
#             "value": "MS"
#         },
#         {
#             "key": "MOROCCO",
#             "value": "MA"
#         },
#         {
#             "key": "MOZAMBIQUE",
#             "value": "MZ"
#         },
#         {
#             "key": "MYANMAR",
#             "value": "MM"
#         },
#         {
#             "key": "NAMIBIA",
#             "value": "NA"
#         },
#         {
#             "key": "NAURU",
#             "value": "NR"
#         },
#         {
#             "key": "NEPAL",
#             "value": "NP"
#         },
#         {
#             "key": "NETHERLANDS",
#             "value": "NL"
#         },
#         {
#             "key": "NETHERLANDS ANTILLES",
#             "value": "AN"
#         },
#         {
#             "key": "NEW CALEDONIA",
#             "value": "NC"
#         },
#         {
#             "key": "NEW ZEALAND",
#             "value": "NZ"
#         },
#         {
#             "key": "NICARAGUA",
#             "value": "NI"
#         },
#         {
#             "key": "NIGER",
#             "value": "NE"
#         },
#         {
#             "key": "NIGERIA",
#             "value": "NG"
#         },
#         {
#             "key": "NIUE",
#             "value": "NU"
#         },
#         {
#             "key": "NORFOLK ISLAND",
#             "value": "NF"
#         },
#         {
#             "key": "NORTHERN MARIANA ISLANDS",
#             "value": "MP"
#         },
#         {
#             "key": "NORWAY",
#             "value": "NO"
#         },
#         {
#             "key": "OMAN",
#             "value": "OM"
#         },
#         {
#             "key": "PAKISTAN",
#             "value": "PK"
#         },
#         {
#             "key": "PALAU",
#             "value": "PW"
#         },
#         {
#             "key": "PANAMA",
#             "value": "PA"
#         },
#         {
#             "key": "PAPUA NEW GUINEA",
#             "value": "PG"
#         },
#         {
#             "key": "PARAGUAY",
#             "value": "PY"
#         },
#         {
#             "key": "PERU",
#             "value": "PE"
#         },
#         {
#             "key": "PHILIPPINES",
#             "value": "PH"
#         },
#         {
#             "key": "POLAND",
#             "value": "PL"
#         },
#         {
#             "key": "PORTUGAL",
#             "value": "PT"
#         },
#         {
#             "key": "PUERTO RICO",
#             "value": "PR"
#         },
#         {
#             "key": "QATAR",
#             "value": "QA"
#         },
#         {
#             "key": "REUNION",
#             "value": "RE"
#         },
#         {
#             "key": "ROMANIA",
#             "value": "RO"
#         },
#         {
#             "key": "RWANDA",
#             "value": "RW"
#         },
#         {
#             "key": "SAINT HELENA",
#             "value": "SH"
#         },
#         {
#             "key": "SAINT KITTS AND NEVIS",
#             "value": "KN"
#         },
#         {
#             "key": "SAINT LUCIA",
#             "value": "LC"
#         },
#         {
#             "key": "SAINT PIERRE AND MIQUELON",
#             "value": "PM"
#         },
#         {
#             "key": "SAINT VINCENT AND THE GRENADINES",
#             "value": "VC"
#         },
#         {
#             "key": "SAMOA",
#             "value": "WS"
#         },
#         {
#             "key": "SAN MARINO",
#             "value": "SM"
#         },
#         {
#             "key": "SAO TOME AND PRINCIPE",
#             "value": "ST"
#         },
#         {
#             "key": "SAUDI ARABIA",
#             "value": "SA"
#         },
#         {
#             "key": "SENEGAL",
#             "value": "SN"
#         },
#         {
#             "key": "SERBIA",
#             "value": "RS"
#         },
#         {
#             "key": "SEYCHELLES",
#             "value": "SC"
#         },
#         {
#             "key": "SIERRA LEONE",
#             "value": "SL"
#         },
#         {
#             "key": "SINGAPORE",
#             "value": "SG"
#         },
#         {
#             "key": "SLOVAKIA",
#             "value": "SK"
#         },
#         {
#             "key": "SLOVENIA",
#             "value": "SI"
#         },
#         {
#             "key": "SOLOMON ISLANDS",
#             "value": "SB"
#         },
#         {
#             "key": "SOMALIA",
#             "value": "SO"
#         },
#         {
#             "key": "SOUTH AFRICA",
#             "value": "ZA"
#         },
#         {
#             "key": "SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS",
#             "value": "GS"
#         },
#         {
#             "key": "SOUTH KOREA",
#             "value": "KR"
#         },
#         {
#             "key": "SPAIN",
#             "value": "ES"
#         },
#         {
#             "key": "SRI LANKA",
#             "value": "LK"
#         },
#         {
#             "key": "SUDAN",
#             "value": "SD"
#         },
#         {
#             "key": "SURINAME",
#             "value": "SR"
#         },
#         {
#             "key": "SVALBARD AND JAN MAYEN",
#             "value": "SJ"
#         },
#         {
#             "key": "SWAZILAND",
#             "value": "SZ"
#         },
#         {
#             "key": "SWEDEN",
#             "value": "SE"
#         },
#         {
#             "key": "SWITZERLAND",
#             "value": "CH"
#         },
#         {
#             "key": "TAIWAN",
#             "value": "TW"
#         },
#         {
#             "key": "TAJIKISTAN",
#             "value": "TJ"
#         },
#         {
#             "key": "TANZANIA",
#             "value": "TZ"
#         },
#         {
#             "key": "THAILAND",
#             "value": "TH"
#         },
#         {
#             "key": "TIMOR-LESTE",
#             "value": "TL"
#         },
#         {
#             "key": "TOGO",
#             "value": "TG"
#         },
#         {
#             "key": "TOKELAU",
#             "value": "TK"
#         },
#         {
#             "key": "TONGA ISLANDS",
#             "value": "TO"
#         },
#         {
#             "key": "TRINIDAD AND TOBAGO",
#             "value": "TT"
#         },
#         {
#             "key": "TUNISIA",
#             "value": "TN"
#         },
#         {
#             "key": "TURKEY",
#             "value": "TR"
#         },
#         {
#             "key": "TURKMENISTAN",
#             "value": "TM"
#         },
#         {
#             "key": "TURKS AND CAICOS ISLANDS",
#             "value": "TC"
#         },
#         {
#             "key": "TUVALU",
#             "value": "TV"
#         },
#         {
#             "key": "UGANDA",
#             "value": "UG"
#         },
#         {
#             "key": "UKRAINE",
#             "value": "UA"
#         },
#         {
#             "key": "UNITED ARAB EMIRATES",
#             "value": "AE"
#         },
#         {
#             "key": "UNITED KINGDOM",
#             "value": "GB"
#         },
#         {
#             "key": "UNITED STATES MINOR OUTLYING ISLANDS",
#             "value": "UM"
#         },
#         {
#             "key": "URUGUAY",
#             "value": "UY"
#         },
#         {
#             "key": "UZBEKISTAN",
#             "value": "UZ"
#         },
#         {
#             "key": "VANUATU",
#             "value": "VU"
#         },
#         {
#             "key": "VENEZUELA",
#             "value": "VE"
#         },
#         {
#             "key": "VIETNAM",
#             "value": "VN"
#         },
#         {
#             "key": "VIRGIN ISLANDS, BRITISH",
#             "value": "VG"
#         },
#         {
#             "key": "VIRGIN ISLANDS, U.S.",
#             "value": "VI"
#         },
#         {
#             "key": "WALLIS,FUTUNA",
#             "value": "WF"
#         },
#         {
#             "key": "WESTERN SAHARA",
#             "value": "EH"
#         },
#         {
#             "key": "ZAMBIA",
#             "value": "ZM"
#         },
#         {
#             "key": "ZIMBABWE",
#             "value": "ZW"
#         },
#         {
#             "key": "YEMEN",
#             "value": "YE"
#         }
#     ],
#     "buyFilters": [
#         "pins",
#         "packingQty",
#         "package",
#         "tempRange"
#     ],
#     "evalFilters": [],
#     "labels": {
#         "backToPurchaseOptions": "Back to Purchase Options",
#         "noneAvailable": "None Available",
#         "updateQuantityLabel": "Update Quantity",
#         "selectAPurchaseOptionLabel": "Select a Purchase Option",
#         "pricePerUnitFullLabel": "Price per Unit",
#         "stockInfoLabel": "The inventory displayed is a snapshot in time. The timing of your order, quantities, and other factors may affect actual delivery. Delivery dates will be emailed to you once your order is confirmed.",
#         "estimatedShipDateLabel": "Estimated Ship Date",
#         "returnToProductPage": "Return to Product Page",
#         "sampleAndBuyNotAvailable": "Sample & Buy not available for this product",
#         "recommendedForNewDesignsDescription": "This product has been released to the market. The data sheet contains all final specifications and operating conditions.  For new designs, ADI recommends utilization of these products.",
#         "recommendedForNewDesigns": "Recommended for New Designs",
#         "preReleaseDescription": "This product is new and engineering validation may still be underway. Quantities may be limited and design specifications may change while we ready the product for release to production.",
#         "productionDescription": "At least one model within this product family is in production and available for purchase. The product is appropriate for new designs but newer alternatives may exist.",
#         "obsoleteDescription": "The models in this product family are no longer available.",
#         "notRecommendedForNewDesignsDescription": "This designates products ADI does not recommend broadly for new designs.",
#         "lastTimeBuyDescription": "All products in this family will be obsolete soon. Please contact ADI Sales or Distributors to arrange for final purchases and read our Obsolescence Information to review the time periods for placing final orders and receiving final shipments.",
#         "automotive": "Automotive",
#         "sampleAndBuy": "Sample & Buy",
#         "searchPartModel": "Search Part Model",
#         "resetTable": "Reset Table",
#         "requestQuote": "Request Quote",
#         "pricingOptions": "Purchase Options",
#         "noParts2": "Try adjusting your filters or click “Reset” to view all available options",
#         "noParts1": "We couldn’t find any parts that match your current criteria.",
#         "filterParts": "Filter Parts",
#         "lastTimeShip": "Last Time Ship",
#         "notRecommendedForNewDesigns": "Not recommended for New Designs",
#         "customerPartNumber": "Customer Part No. ",
#         "estimatedDeliveryDateLabel": "Estimated Delivery Date",
#         "estDeliveryDate": "Est Delivery Date",
#         "availableLabel": "Available",
#         "stockVisibilityLabel": "Inventory shown here is a snapshot in time. Timing of order, quantities and other factors may impact actual delivery. Delivery dates will be emailed to you once your order is confirmed.",
#         "scNCNRNotificationaddcartLabel": "This item delivery cannot be pushed out, canceled, or returned, as per ADI's <a href=\"{url}\" target=\"_blank\">Terms & Conditions</a>",
#         "warningNCNRLabel": "This item is NCNR and its delivery cannot be pushed out, cancelled or returned as per ADI's <a href=\"https://www.analog.com/en/support/terms-and-conditions.html\" target=\"_blank\">Terms & Conditions</a>",
#         "noneSelected": "None selected",
#         "prodValidationError": "Please contact Customer Service for assistance. (Error: {errorCode})",
#         "requiresQuoteLabel": "This product requires a quote. Kindly contact customer service to proceed.",
#         "getADIQuote": "<a href=\"#\" target=\"_blank\">Get an ADI Quote</a><i class=\"ri-external-link-line\"></i>",
#         "continue": "Continue",
#         "selectCountryTitle": "Please select a country/region to view available inventory.",
#         "selectCountryContent": "You can also {loginButton} to your myAnalog account to enable all buy features, ability to sign up for model specific notifications, and more.",
#         "mustSelectCountry": "You must select a country/region to continue.",
#         "mustSelectModel": "You have to select a model to proceed",
#         "circuitTitle": "Sample Products",
#         "evalTitle": "Evaluation Boards",
#         "pdpTitle": "Part Models",
#         "softwareTitle": "Buy",
#         "selectModelNumber": "Select Model Number",
#         "selectModels": "Available Models",
#         "availableModels": "Available Product Models to Sample",
#         "abandonedCartPriceErrorLabel": "There was a price change for at least one line item. Please review your cart again before proceeding to checkout.",
#         "abandonedCartQuoteExpireLabel": "The quote that was previously applied to your cart has expired and has been removed.",
#         "aboutProjectLabel": "About Your Project",
#         "aCountryMustBeSelected": "A country must be selected to view available inventory.",
#         "Add_x0020_Freight_x0020_Forwarder": "Add Freight Forwarder",
#         "addAddressLabel": "Add Address",
#         "addBillingAddressLabel": "Add Billing Address",
#         "addDeliveryLabel": "+Add Delivery",
#         "addFreightForwarderLabel": "Add Freight Forwarder",
#         "addItemLabel": "Add Item",
#         "addLabel": "Add",
#         "addNewAddressLabel": "Add New Address",
#         "addNewFreightForwardLabel": "Add New Freight Forwarder",
#         "address1Label": "Street Address 1",
#         "address2Label": "Street Address 2",
#         "addressBlockErrLabel": "We apologize, but we are unable to process your order due to a delivery block on your account. Please contact our support team for assistance.",
#         "addressBookLabel": "Address Book",
#         "addressErrorLabel": "The address could not be saved.",
#         "addSelectFreightForwarderLabel": "Add/Select Freight Forwarder",
#         "addShippingAddressLabel": "Add Shipping Address",
#         "addSuccess": "{model} has been added to your cart.",
#         "addToCartLabel": "Add To Cart",
#         "adiStandardShippingDescriptionLabel": "ADI Standard Shipping - Shipping charges will be provided upon order confirmation.",
#         "alertBoxLabel": "are not available to ship immediately.You can add an additional line at MOQ after you ‘Add item’ to cart",
#         "all": "All",
#         "allfieldsarerequired": "All fields are required",
#         "alphaNumericPatternErrorLabel": "This field only allows Numbers and characters.",
#         "alreadyInCartErrLabel": "Item already in cart",
#         "altTextAmexLabel": "Amex card",
#         "altTextMasterLabel": "Master card",
#         "altTextVisaLabel": "Visa Card",
#         "AndTextLabel": "-AND-",
#         "apply": "Apply",
#         "applyFullEditBtnLabel": "Edit Quote",
#         "applyFullQuoteBtnLabel": "Apply Quote",
#         "applyPayByTermURLLabel": "https://eramoa.dnb.com/eram-oa/eramOA/Analog+Devices/authenticateToken?token=DRhGDyOhPbJKyaIQxQbSoQ%3D%3D&database=eje7piA1aySx8qKGZNpQz3NT1Yb2iUMTFVc12KXvc80%3D",
#         "applyPayTermLabel": "Want to pay by terms?",
#         "applyQuoteBtnLabel": "Apply Quotes",
#         "applyQuoteLabel": "Apply Quote",
#         "asapLabel": "ASAP",
#         "attentionFNameLabel": "Attention To: First Name",
#         "attentionLNameLabel": "Attention To: Last Name",
#         "automotiveOnly": "Automotive Only",
#         "availableInventory": "{stock} Available",
#         "billingAddressLabel": "Billing Address",
#         "blankTargetLabel": "_blank",
#         "breakNotAllowed": "Unit quantity must be a multiple of {packingCount}",
#         "buyNowPrice": "Buy Now",
#         "buyOnLineDisclaimerLabel": "Analog Devices offers most models for purchase (credit card orders only) to qualified customers in",
#         "buyOnlineLabel": "About Buying Online",
#         "buyOnLineSecondTxtLabel": "For more information about buying online",
#         "buyOnLineThirdTxtLabel": "Orders placed by unauthorized distributors/resellers will be cancelled.",
#         "calculatedAtOrderConfirmationLabel": "Calculated upon order confirmation",
#         "cancelLabel": "Cancel",
#         "canOrderErrorMessageLabel": "is not available and has been removed from your cart. Please review your cart and checkout again.",
#         "careOfLabel": "Care of",
#         "ccLabel": "Credit Card: One Time Payment",
#         "charLimitErrorLabel": "The character limit for this field is",
#         "checkOutBackToCartLabel": "Back to Shopping Cart",
#         "checkoutLabel": "Checkout",
#         "checkStock": "Distributor Stock",
#         "chinaBody": "For orders shipping to other countries or regions, please toggle to \"Outside of Mainland China\"",
#         "chinaHeader": "Shipping to Mainland China",
#         "clickFreightForwardAddrLabel": "Click on an address box below to see the related freight forwarders.",
#         "clickHereLabel": "click here",
#         "clickHereUrlLabel": "https://www.analog.com/en/support/customer-service-resources/sales/buy-products.html",
#         "close": "close",
#         "closeFullWidthLabel": "close-full-width-modal",
#         "closeLabel": "Close",
#         "commercialAgreement": "There is a commercial agreement linked to <a href=\"{url}\">your account</a>. You can select it at checkout.",
#         "companyLabel": "Company",
#         "companyNameLabel": "Company Name",
#         "confirmAndGoLabel": "Confirm & Proceed to Payment",
#         "confirmPayLabel": "Confirm & Pay",
#         "ContactDistribution": "Contact Distribution",
#         "continueShoppingLabel": "Continue Shopping",
#         "countryCodeLabel": "Country Code",
#         "ctaApplyPayTermLabel": "Apply Here",
#         "currencyCodeLabel": "USD",
#         "currencySymbolLabel": "$",
#         "customerPartNoLabel": "Customer Part Number",
#         "customerServiceLabel": "Customer Service >",
#         "decrementQuantityLabel": "decrement item quantity",
#         "definitionReel": "A length of empty tape at the beginning and end, known respectively as a leader and trailer, enables the use of automated assembly equipment. The tape is wound onto a plastic reel according to Electronics Industries Alliance (EIA) standards.<br><br>Reel size, pitch, quantity, orientation, and other detailed information is usually found toward the end of the part's datasheet.",
#         "definitionTape": "definitionTape",
#         "definitionTapeAndReel": "A length of empty tape at the beginning and end, known respectively as a leader and trailer, enables the use of automated assembly equipment. The tape is wound onto a plastic reel according to Electronics Industries Alliance (EIA) standards.<br><br>Reel size, pitch, quantity, orientation, and other detailed information is usually found toward the end of the part's datasheet.",
#         "definitionTray": "Tray usually refers to a JEDEC standard matrix tray, measuring 12.7x5.35 inches and either 0.25 or 0.40 inches tall. Trays are usually constructed from plastic, but aluminum is permissible. JEDEC trays contain slots to allow air to pass vertically and are rated for at least 140<sup>°</sup>C to allow drying of parts in industrial ovens. Trays are stackable and feature a chamfered corner indicating the orientation of pin one of the parts.<br><br>Trays are packaged according to the ESD (Electro Static Discharge) and MSL (Moisture Sensitivity Level) protection requirements.",
#         "definitionTube": "A tube is a rigid extruded plastic package designed to fit the profile of the part and protect the leads. Tubes ship with the exact number of parts ordered and a rubber plug or plastic peg in each end to prevent the parts from sliding out.<br><br>Tubes are packaged according to the ESD (Electro Static Discharge) and MSL (Moisture Sensitivity Level) protection requirements.",
#         "describeProjectLabel": "Describe Project",
#         "eachLabel": "Each",
#         "editAddressLabel": "Edit Address",
#         "editLabel": "Edit",
#         "editRemoveLabel": "Edit/Remove",
#         "effectiveDateLabel": "Effective Date",
#         "email": "Email",
#         "emailIdLabel": "Email Address",
#         "endCustomerInfoLabel": "End Customer Info",
#         "endCustomerLabel": "End Customer",
#         "enterPartNoLabel": "Enter Part Number",
#         "enterQtyLabel": "Enter Quantity",
#         "errorMessagePartOneLabel": "The request failed as the service is temporarily unavailable.",
#         "errorMessagePartTwoLabel": "Please try again later.",
#         "errorWarningLabel": "error warning",
#         "expirationDateLabel": "Expiration Date",
#         "filter": "Filter",
#         "filters": "Filters",
#         "fNameOrlNameLabel": "First Name/Last Name",
#         "freightForwarderLabel": "Freight Forwarder",
#         "freightForwardersLabel": "Freight Forwarders",
#         "freightFwdNotAvailLabel": "There are no freight forwarders associated with this shipping address.",
#         "genericPatternErrorLabel": "This field cannot contain special characters.",
#         "genericPatternNameErrorLabel": "This field cannot contain special characters or numbers.",
#         "goToDisti": "Check Distributor Website",
#         "headerLogoAltLabel": "Short Header ADI Logo",
#         "help": "Help",
#         "hyphen": "-",
#         "incrementQuantityLabel": "increment item quantity",
#         "info": "Info",
#         "inStockLabel": "In Stock",
#         "invalidOrderableItemError": "Please enter a valid orderable part number.",
#         "invalidZipErrorLabel": "Please enter a valid zip code.",
#         "itemLabel": "Item",
#         "itemNotAvailableForDistLabel": "This Product cannot be added by distributor",
#         "itemquantityExceededLabel": "Quantity requested is not available",
#         "itemsLabel": "Items",
#         "lastTimeBuy": "Last Time Buy",
#         "leadTimeLabel": "Lead Time # Weeks",
#         "leadTimeNotAvailableLabel": "Lead Time Not Available",
#         "leadTimePrefixLabel": "Lead Time",
#         "leadTimeSuffixLabel": "Weeks",
#         "listNowBodyLabel": "Add parts to your cart at standard price and lead time.",
#         "listNowLabel": "List Price",
#         "listPrice1k": "1Ku",
#         "listPrice500": "500u",
#         "loginButton": "Log in",
#         "loginOrRegisterLabel": "Log in or Register for an Account",
#         "loginToYourAccount": "{loginButton} to your myAnalog account to enable all features",
#         "model": "Part Model",
#         "modelLabel": "Model",
#         "modelNoLabel": "Type Model Number",
#         "modelNotAvailableLabel": "Model Not Available For Purchase.",
#         "modelNotFoundLabel": "Model number not found.",
#         "modelNUrlLabel": "https://maxim.modeln.com/login",
#         "momErrorMessageLabel": "Quantity must meet order multiple of",
#         "moqErrorLabel1": "Quantity must meet MOQ",
#         "moqErrorLabel2": "and order multiple of",
#         "mulDeliveriesLabel": "Multiple Deliveries",
#         "multipleDeliveryTitleLabel": "Use the fields below to split your order into multiple deliveries with different delivery dates and quantities",
#         "myAnalogLogin": "Log in to your myAnalog account to enable all features",
#         "myCmpnyLabel": "My Company",
#         "nameLabel": "name",
#         "needMore": "Need more than 1,000 units? <a href=\"#\" target=\"_blank\">Get an ADI Quote</a><i class=\"ri-external-link-line\"></i>",
#         "newaddProductLabel": "New Item Added",
#         "newItemAddedLabel": "New Item Added",
#         "nextStepLabel": "Next Step",
#         "noData": "There are no parts matching your criteria. Please update or reset the applied filters.",
#         "noExistingQuoteLabel": "No existing quotes",
#         "noItemsCartLabel": "No item in cart",
#         "nonStandardShippingDescriptionLabel": "Shipping charges to be applied based on your company's carrier agreement.",
#         "noRecordTotalLabel": "$0.00",
#         "noReferrerLabel": "noreferrer",
#         "numericErrorLabel": "This field cannot contain numeric characters.",
#         "obsolete": "Obsolete",
#         "onlyNumbersPatternErrorLabel": "This field only allows numbers.",
#         "oooLabel": "Out of Stock",
#         "optionalLabel": "Optional",
#         "optionLabel": "Option",
#         "optionsErrPartLabel": "This quantity may result in a broken package - to avoid breaking, enter a multiple of ",
#         "optionsErrPartOneLabel": "Quantities may be adjusted to meet MOQ",
#         "optionsErrPartTwoLabel": "and order multiples of",
#         "orderComplianceLabel": "Order Compliance",
#         "orderDetailsHeadLabel": "Order Contact Details",
#         "orderSummaryLabel": "Order Summary",
#         "outOfStock": "Out of Stock",
#         "outOfStockErrorMessageLabel": "is out of stock and has been removed from your cart. Please review your cart and checkout again.",
#         "packageQuantity": "Package Quantity",
#         "packageType": "Package Type",
#         "packageTypeLabel": "Package Type",
#         "partModels": "Part Models",
#         "partNoLabel": "Part Number",
#         "partQuotedLabel": "Part Quoted",
#         "payByTermLabel": "Pay by Term",
#         "paymentCreditLimitLabel": "Credit Line: ",
#         "paymentHeaderTextLabel": "Select Payment Method",
#         "paymentMethodLabel": "Payment Method",
#         "paymentSubHeaderTextLabel": "All transactions are secure and encrypted.",
#         "pcn": "PCN",
#         "pcnPdn": "PCN/PDN",
#         "pcsLabel": "pcs",
#         "pdn": "PDN",
#         "phoneNoLabel": "Phone Number",
#         "phoneNumberPatternErrorLabel": "This field cannot contain string.",
#         "pieceQuantityLabel": "Piece Quantity",
#         "pins": "Pins",
#         "placeholderCountryCodeLabel": "Select Country Code",
#         "placeholderFNameLabel": "First Name",
#         "placeholderLNameLabel": "Last Name",
#         "placeholderStateProvinceLabel": "Select State/Province",
#         "placeOrderCtaLabel": "Place Order",
#         "preRelease": "Pre-Release",
#         "price": "Price",
#         "pricePerPieceLabel": "Price/Piece",
#         "pricePerQtyMxm": "Qty | Price (USD)",
#         "pricePerUnitLabel": "Price/Unit",
#         "pricePieceLabel": "Price/Piece",
#         "priceRangeUnavailable": "Price Range Unavailable",
#         "priceRowNotFoundLabel": "Product is not available for purchase",
#         "priceStartingFrom": "Starting from",
#         "priceUnavailable": "Price unavailable",
#         "priceUnavailableLabel": "Quote Required",
#         "print": "Print",
#         "production": "Production",
#         "purchaseOrderNumberLabel": "Purchase Order Number",
#         "qty": "Quantity",
#         "qtyLabel": "Qty",
#         "quantityBodyLabel": "Update quantity to view purchasing options",
#         "quantityExceedsErrorLabel": "Quantity Exceeds the Total Quantity",
#         "quantityLabel": "Quantity",
#         "quickAddLabel": "Quick Add",
#         "quickShipCopyLabel": "This option provides the fastest method to receive parts on your dock. Complete or partial quantities may be provided.",
#         "quickShipLabel": "Quick Ship",
#         "quoteAltLabel": "quote-status-icon",
#         "quoteAppliedLabel": "Quote Applied",
#         "quoteComplianceErrLabel": "The quote has been removed as the piece quantity does not meet quote compliance.",
#         "quotedPriceBodyLabel": "Apply a quote to proceed to cart. Order is shipped subject to available inventory or standard lead time.",
#         "quotedPriceLabel": "Quoted Price",
#         "quoteNumberLabel": "Quote Number",
#         "quoteOnlyProductErrMsgLabel": "This part number must be purchased through an existing active quote. Please select a quote to continue.",
#         "quoteOnlySignInErrLabel": "Please sign in and apply a quote to proceed with this item.",
#         "quoteQtyComplianceErrLabel": "Quantity must meet order compliance of",
#         "quoteStatusLabel": "Quote Status",
#         "radioIconAltLabel": "selected-radio-icon",
#         "remainingLabel": "Remaining",
#         "removeQuoteLabel": "Remove Quote",
#         "remQtyLabel": "Remaining Quantity",
#         "repCodeMissingLabel": "Please contact Customer Service for assistance. (Error: Rep Code Not Found)",
#         "reqDateToolTipLabel": "You can edit requested delivery date in the cart.",
#         "reqDeliveryDateLabel": "Req Delivery Date",
#         "reqDelvDateLabel": "Request Delivery Date",
#         "reqtQuoteLabel": "Request Quote",
#         "requestDeliveryDateLabel": "Requested Delivery Date",
#         "requestedByLabel": "Requested By",
#         "requestedOnLabel": "Requested On",
#         "requestQuoteLabel": "Request a Quote",
#         "requiredFieldLabel": "This field is required",
#         "resaleCopyLabel": "If you select this box, you must provide a valid, signed and dated resale certificate to the Analog Devices US Tax Department. We cannot accept a copy of the resale certificate registration. By Fax: 781-461-4360. By Email: us.taxdepartment@analog.com",
#         "resaleTitleLabel": "I have a Resale Certificate for this address",
#         "roHN": "N",
#         "roHNo": "No",
#         "rohs": "RoHS",
#         "roHSE": "E",
#         "rohsOnly": "RoHs Only",
#         "roHSY": "Y",
#         "roHSYes": "Yes",
#         "save": "Save",
#         "saveAddressLabel": "Save Address",
#         "saved": "saved",
#         "saveLabel": "Save",
#         "schoolNameLabel": "School Name",
#         "select": "Select",
#         "selectACountry": "Select a Country/Region",
#         "selectAll": "Select All",
#         "selectCategoryLabel": "Select Application",
#         "selectCountryRegionLabel": "Country/Region",
#         "selectCountryRegionPlaceholder": "Select Country",
#         "selectCountryUrlLabel": "https://www.analog.com/en/support/customer-service-resources/customer-service/view-shipping-options-rates.html",
#         "selectDateLabel": "Please select a date",
#         "selectDeliveryDateLabel": "Select Delivery Date",
#         "selectDeliveryDatesLabel": "Select Delivery Dates",
#         "selectDistributor": "Select Distributor",
#         "selectedCount": "{count} Selected",
#         "selectedPriceLabel": "Selected pricing",
#         "selectPackageLabel": "Select Package",
#         "selectQuantityLabel": "Select Quantity",
#         "selectQuoteLabel": "Select Quote",
#         "selectShippingMethodLabel": "Select Shipping Method",
#         "sellerWarranty": "Seller Provided Warranty",
#         "shipdescriptionLabel": "Shipping charges to be applied based on customer routing guide",
#         "shipNowBodyLabel": "Ship Now orders will ship immediately, once processed, from current available inventory, and cannot be pushed out or cancelled.",
#         "shipNowBodyTwoLabel": "Ship Now availability may vary and the pricing reflects an adder for faster service levels.",
#         "shipNowLabel": "Ship Now",
#         "shipNowMobileBodyLabel": "Ship Now orders will ship immediately, once processed, from current available inventory, and cannot be pushed out or cancelled.Ship Now availability may vary and the pricing reflects an adder for faster service levels.",
#         "shipNowTextLabel": "Ship Now Price",
#         "shippingAddressLabel": "Shipping Address",
#         "shippingLabel": "Shipping",
#         "shippingMethodLabel": "Shipping Method",
#         "shippingNotIncludedLabel": "Shipping is not included",
#         "shipsIn1To2Days": "Ships in 1-2 business days",
#         "shipsInDays": "Ships in {range} business weeks",
#         "shoppingCartLabel": "Shopping Cart",
#         "singDeliveryLabel": "Single Delivery",
#         "singleDeliveryTitleLabel": "Use the field below to request a specific delivery date. Requested date isn’t guaranteed.",
#         "sms": "SMS",
#         "somethingWentWrong": "Something went wrong. Please try again later.",
#         "sort": "Sort by {column}",
#         "standardCopyLabel": "This option provides the most cost efficient method through orders placed at lead time.",
#         "standardLabel": "Standard",
#         "stateProvinceLabel": "State/Province",
#         "stockInfo": "Stock Info",
#         "submittedDateLabel": "Submitted Date",
#         "subscribe": "Subscribe<br>PCN/PDN",
#         "subtotal": "Subtotal",
#         "subTotalLabel": "Subtotal",
#         "supplier": "Supplier",
#         "supportUrlLabel": "https://support.analog.com/en-US/",
#         "switchToEnglish": "Switch to English",
#         "taxableLabel": "Taxable",
#         "taxesLabel": "Taxes",
#         "taxExemptLabel": "Tax Exempt Certificate",
#         "tempRange": "Temp Range",
#         "termLabel": "Term",
#         "testBillAttentionTextLabel": "testBillAttention",
#         "test-label": "test",
#         "testShipAttentionTextLabel": "testShipAttention",
#         "thisWillBreakPackage": "This quantity will result in a broken package - to avoid breaking, enter a multiple of {packingCount}",
#         "title": "Title",
#         "tNcLineOneLabel": "I accept this order per Analog Devices, Inc.’s standard Terms & Conditions (incorporated herein by reference)",
#         "tNcLineTwoLabel": "For purchased items, I agree to pay shipping and handling charges, taxes, duties and other government assessments.",
#         "totalDoesNoyIncludeTaxLabel": "Total does not include taxes and shipping.",
#         "totalLabel": "Total",
#         "totalQuantityLabel": "Total Quantity",
#         "townCityLabel": "City, Town",
#         "townCityPlaceholder": "City",
#         "tryAgainLabel": "Please try again",
#         "unableToRetrieveData": "Unable to retrieve inventory.<br /> Please try again in a few moments.",
#         "unitLabel": "Units",
#         "unitPriceLabel": "Unit Price",
#         "unitPricing": "Unit Pricing (RMB)",
#         "unitQuantity": "Unit Quantity",
#         "unitQuantityLabel": "Unit Quantity",
#         "unSelectedRadioAltLabel": "unSelected-radio-icon",
#         "updateLabel": "Update",
#         "uploadCertLabel": "Upload Resale Certificate",
#         "validEmailLabel": "Please enter a valid email address.",
#         "valueLabel": "Value",
#         "vatIdCopyLabel": "Please do not include the two-character country prefix. Please note that you will be charged VAT if you do not enter a valid VAT ID.",
#         "vatIdErrorMsgLabel": "Please enter a valid VAT ID",
#         "vatIDLabel": "VAT ID (Optional)",
#         "vatIdPlaceholderLabel": "VAT ID",
#         "viewCart": "View Cart",
#         "viewInCart": "View in Cart",
#         "viewInventory": "View Inventory",
#         "viewLess": "View Less",
#         "viewMore": "View More",
#         "viewPriceInCart": "View Price in Cart",
#         "viewQuoteDetailsLabel": "View Quote Details",
#         "yes": "Yes",
#         "youMustLogin": "A myAnalog account is required.<br />You must <a href=\"{url}\">Log in/Register</a> before proceeding",
#         "yourPrivacy": "We respect you privacy and will not share your information outside of Analog Devices.\",\t     \"adiWillSendYouANote\": \"ADI will send you a notification as soon as this product is back in stock",
#         "zipPostalCodeLabel": "Postal Code",
#         "addedToCart": "Added to Cart",
#         "addToCart": "Add to Cart",
#         "aMyAnalogAccountForCheckout": "A myAnalog account is required for Checkout. <a>Log in/Register</a> now for faster checkout and the best user experience.",
#         "breakPackage": "Break Package",
#         "buyFromDistributors": "Buy from Distributors ({inventory})",
#         "buyingRequirements": "Analog Devices Buy Online requires ordering in Multiples of {number}",
#         "cancel": "Cancel",
#         "cantAddToCart": "Unable to add, \\\\\\\"{model}\\\\\\\" to your cart. Please try again later.",
#         "changeNotification": "Product/Process Change Notification",
#         "contactADI": "Contact ADI",
#         "continueShopping": "Continue Shopping",
#         "description": "Description",
#         "distributionOnly": "Distribution Only",
#         "emailAddress": "Email Address",
#         "inventory": "Inventory",
#         "itemsSelected": "{count} Samples Selected",
#         "lifeCycle": "Life Cycle",
#         "listPrice": "List Price",
#         "multiplesOf": "Multiple of {number}",
#         "notifyMe": "Notify Me",
#         "notifyMeWhenAvailable": "Notify Me When Available",
#         "package": "Package",
#         "packingQty": "Packing Qty",
#         "pcnNotifications": "PCN Notifications",
#         "pieceQty": "Piece Quantity",
#         "pleaseSelectACountry": "Please Select a Country",
#         "pricePerQty": "Qty | Price (USD)\"",
#         "priceRange": "Price Range",
#         "publicationDate": "Publication Date",
#         "purchase": "Purchase",
#         "requestNotifications": "Subscribe to PCN/PDN notifications",
#         "sample": "Sample",
#         "saveToMyAnalog": "Save to myAnalog",
#         "applyFilters": "Apply Filters",
#         "availability": "Avail: {date}",
#         "isQuoteRequiredLabel": "This model requires a quote to purchase. <br/><a href=\"#\" target=\"_blank\">Get an ADI Quote</a><i class=\"ri-external-link-line\"></i>",
#         "brokenPackageAvailableLabel": "Quantities must be adjusted to meet MOQ ({MOQ}) and order multiples of {X}.  Broken package options are available in the cart.",
#         "brokenPackageNotAvailableLabel": "Quantities must be adjusted to meet MOQ ({MOQ}) and order multiples of {X}.",
#         "NoPackageQtyEnforcedLabel": "Quantities must be adjusted to meet MOQ ({MOQ}).",
#         "softwarePackageTypeLabel": "N/A",
#         "contactADIDescription": "Contact ADI",
#         "lastTimeShipDescription": ""
#     },
#     "buyModels": [
#         {
#             "description": null,
#             "model": "ADA4620-2ARZ",
#             "package": "8-Lead SOIC",
#             "packingUrl": "/media/en/package-pcb-resources/package/pkg_pdf/soic_narrow-r/r_8.pdf",
#             "packingQty": "Tube,98",
#             "moqOEM": 1,
#             "ncnrFlag": false,
#             "uomMaintained": true,
#             "minOrderQty": 98,
#             "listPrice500": "3.63",
#             "listPrice1k": "2.79",
#             "packingOption": "Tube",
#             "packageType": "R-8",
#             "pcn": [],
#             "pdn": [],
#             "pins": "8",
#             "pricePerQty": [
#                 {
#                     "price": "8.17000",
#                     "quantity": "1"
#                 },
#                 {
#                     "price": "5.48000",
#                     "quantity": "10"
#                 },
#                 {
#                     "price": "3.99357",
#                     "quantity": "98"
#                 },
#                 {
#                     "price": "3.68898",
#                     "quantity": "196"
#                 },
#                 {
#                     "price": "3.53432",
#                     "quantity": "294"
#                 },
#                 {
#                     "price": "3.48750",
#                     "quantity": "588"
#                 }
#             ],
#             "rohs": "roHSY",
#             "lifeCycle": "production",
#             "tempRange": "-40°C to 125°C",
#             "automotive": false,
#             "hidePriceByQtyThreshold": null,
#             "listPrice1": "6.28",
#             "leadTime": 39,
#             "canQuote": true,
#             "canOrder": true,
#             "quoteRequired": false
#         },
#         {
#             "description": null,
#             "model": "ADA4620-2ARZ-R7",
#             "package": "8-Lead SOIC",
#             "packingUrl": "/media/en/package-pcb-resources/package/pkg_pdf/soic_narrow-r/r_8.pdf",
#             "packingQty": "Reel,1000",
#             "moqOEM": 1,
#             "ncnrFlag": false,
#             "uomMaintained": true,
#             "minOrderQty": 1000,
#             "listPrice500": "3.63",
#             "listPrice1k": "2.79",
#             "packingOption": "Reel",
#             "packageType": "R-8",
#             "pcn": [],
#             "pdn": [],
#             "pins": "8",
#             "pricePerQty": [
#                 {
#                     "price": "3.48750",
#                     "quantity": "1000"
#                 }
#             ],
#             "rohs": "roHSY",
#             "lifeCycle": "production",
#             "tempRange": "-40°C to 125°C",
#             "automotive": false,
#             "hidePriceByQtyThreshold": null,
#             "listPrice1": "6.28",
#             "leadTime": 39,
#             "canQuote": true,
#             "canOrder": true,
#             "quoteRequired": false
#         },
#         {
#             "description": null,
#             "model": "ADA4620-2ARZ-RL",
#             "package": "8-Lead SOIC",
#             "packingUrl": "/media/en/package-pcb-resources/package/pkg_pdf/soic_narrow-r/r_8.pdf",
#             "packingQty": "Reel,2500",
#             "moqOEM": 1,
#             "ncnrFlag": false,
#             "uomMaintained": true,
#             "minOrderQty": 2500,
#             "listPrice500": "3.63",
#             "listPrice1k": "2.79",
#             "packingOption": "Reel",
#             "packageType": "R-8",
#             "pcn": [],
#             "pdn": [],
#             "pins": "8",
#             "pricePerQty": [],
#             "rohs": "roHSY",
#             "lifeCycle": "production",
#             "tempRange": "-40°C to 125°C",
#             "automotive": false,
#             "hidePriceByQtyThreshold": "2500",
#             "listPrice1": "6.28",
#             "leadTime": 39,
#             "canQuote": true,
#             "canOrder": true,
#             "quoteRequired": false
#         }
#     ],
#     "buyParameters": [
#         "model",
#         "listPrice",
#         "stockInfo",
#         "pins",
#         "tempRange",
#         "packageType",
#         "package",
#         "rohs",
#         "automotive"
#     ],
#     "buySortable": [
#         "packageType"
#     ],
#     "evalModels": [],
#     "evalParameters": [
#         "supplier",
#         "stockInfo",
#         "unitQuantity",
#         "listPrice"
#     ],
#     "evalSortable": [
#         "model",
#         "rohs"
#     ],
#     "softwareModels": [],
#     "softwareParameters": [
#         "description",
#         "supplier",
#         "listPrice"
#     ],
#     "softwareFilters": [],
#     "softwareSortable": [
#         "model",
#         "rohs"
#     ],
#     "ModelJsonObject": null,
#     "LabelsLists": null,
#     "circuitModels": [],
#     "circuitParameters": [
#         "description",
#         "availableModels"
#     ],
#     "circuitFilters": [],
#     "circuitSortable": [],
#     "description": "",
#     "ManufacturerType": "",
#     "generic": "ADA4620-2",
#     "GenericCode": "",
#     "productLifeCycleStatus": "Recommended for New Designs",
#     "env": "live"
# }