import requests


headers = {
    "accept": "text/html, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://www.rohm.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.rohm.com/products/power-management/switching-regulators/buck-step-down/external-fet-nonsynchronous/bd63536fj-product",
    "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}
cookies = {
    "$JSESSIONID": "257A9A0234784CC3FFFC9C5674172C40.prod-app-2",
    "COOKIE_SUPPORT": "true",
    "GUEST_LANGUAGE_ID": "en_US",
    "ASLBSA": "00034bd7091876efe701f4f038f9fde27e563081a29610d28cbc689fd7f5b8813714",
    "ASLBSACORS": "00034bd7091876efe701f4f038f9fde27e563081a29610d28cbc689fd7f5b8813714",
    "geoLocation": "IN",
    "_gcl_au": "1.1.98241441.1767074429",
    "_ga": "GA1.1.1364922702.1767074430",
    "_mkto_trk": "id:247-PYD-578&token:_mch-rohm.com-9ef3bf1ae3c2bf2152b6fc915b83159c",
    "recentclicklist": "P\\u0021bd63536fj\\u00211030\\u0021true\\u0021true\\u00211767074752153",
    "LFR_SESSION_STATE_10140": "1767074752657",
    "OptanonConsent": "isGpcEnabled=0&datestamp=Tue+Dec+30+2025+14%3A12%3A00+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202507.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=cf633c0f-ca8f-4323-a6f7-975c648918f0&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=JP%3B13",
    "OptanonAlertBoxClosed": "2025-12-30T06:12:00.156Z",
    "_ga_B7YTXS509X": "GS2.1.s1767074429$o1$g1$t1767075145$j8$l0$h786927399"
}
# url = "https://www.rohm.com/html/json_req.php?url=http%3A//10.100.2.14/solr/rohm-prod/select/%3Fstart%3D0%26rows%3D10%26wt%3Djson%26json.nl%3Dmap%26facet%3Don%26facet.mincount%3D1%26facet.field%3DPartNumber_copy%26facet.field%3DProductSupplyStatusText_copy%26facet.field%3DProductSupplyStatusText_copy%26facet.field%3DProductGradeText_copy%26facet.field%3DChannel_num%26facet.field%3DIntegratedfetController_copy%26facet.field%3DBuckBoostBuckboostInverting_copy%26facet.field%3DVoltageIn1Min_num%26facet.field%3DVoltageIn1Max_num%26facet.field%3DVoltageOut1Min_num%26facet.field%3DVoltageOut1Max_num%26facet.field%3DCurrentOut1Max_num%26facet.field%3DVoltageIn2Min_num%26facet.field%3DVoltageIn2Max_num%26facet.field%3DVoltageOut2Min_num%26facet.field%3DVoltageOut2Max_num%26facet.field%3DCurrentOut2Max_num%26facet.field%3DVoltageIn3Min_num%26facet.field%3DVoltageIn3Max_num%26facet.field%3DVoltageOut3Min_num%26facet.field%3DVoltageOut3Max_num%26facet.field%3DCurrentOut3Max_num%26facet.field%3DSwitchFrequencyMax_num%26facet.field%3DSynchronousAsynchronous_copy%26facet.field%3DTechnology_copy%26facet.field%3DLightLoadMode_copy%26facet.field%3DEnTerminal_copy%26facet.field%3DPgood_copy%26facet.field%3DOperatingTemperatureMinIncludeJunctionTemperature_copy%26facet.field%3DOperatingTemperatureMaxIncludeJunctionTemperature_copy%26facet.field%3DPackageShortCode_copy%26facet.field%3DSmallReel_copy%26facet.field%3DThermalLink_copy%26facet.field%3DSpiceLink_copy%26facet.field%3DSupportPeriod_num%26facet.field%3DCommonStandard_copy%26facet.field%3DSaftyStandard_copy%26facet.field%3DRohmSolutionSimulatorLink_copy%26facet.field%3DEvaluationBoardLink_copy%26facet.field%3DPackageDimension_copy%26facet.field%3DIsRohsText_copy%26facet.field%3DPS_PartNodeCode%26sort%3DProductSupplyStatus_num%20desc%2C%20ProductDisplayFlag_num%20desc%2C%20PS_PartNumber%20asc%26q%3D%28PS_ProductDivisionCode%3A103030%20OR%20PS_ProductGroupCode%3A103030%20OR%20PS_ProductFamilyCode%3A103030%20OR%20PS_ProductTypeCode%3A103030%20OR%20PS_ProductSubTypeCode%3A%20103030%29%20AND%20ProductDisplayFlag_num%3A%5B1%20TO%20*%5D%20AND%20PS_PartStatus%3A60%20NOT%20TemplateViewName%3AViewWP_Part_Transistor_Template_200850&jsonp_callback=jQuery35108162906223089124_1767094458528&_=1767094458529"
params = {
    "p_p_id": "com_rohm_product_detail_web_RohmProductDetailWebPortlet",
    "p_p_lifecycle": "2",
    "p_p_state": "normal",
    "p_p_mode": "view",
    "p_p_resource_id": "detail/getDocumentsResourceData",
    "p_p_cacheability": "cacheLevelPagebd63536fj"
}
data = {
    "partNumber": "bd63536fj",
    "pageViewType": "tableView"
}
# url = "https://www.rohm.com/html/json_req.php?_=1767094458529&jsonp_callback=jQuery35108162906223089124_1767094458528&url=http%3A//10.100.2.14/solr/rohm-prod/select/%3Fstart%3D0%26rows%3D10%26wt%3Djson%26json.nl%3Dmap%26facet%3Don%26facet.mincount%3D1%26facet.field%3DPartNumber_copy%26facet.field%3DProductSupplyStatusText_copy%26facet.field%3DProductSupplyStatusText_copy%26facet.field%3DProductGradeText_copy%26facet.field%3DChannel_num%26facet.field%3DIntegratedfetController_copy%26facet.field%3DBuckBoostBuckboostInverting_copy%26facet.field%3DVoltageIn1Min_num%26facet.field%3DVoltageIn1Max_num%26facet.field%3DVoltageOut1Min_num%26facet.field%3DVoltageOut1Max_num%26facet.field%3DCurrentOut1Max_num%26facet.field%3DVoltageIn2Min_num%26facet.field%3DVoltageIn2Max_num%26facet.field%3DVoltageOut2Min_num%26facet.field%3DVoltageOut2Max_num%26facet.field%3DCurrentOut2Max_num%26facet.field%3DVoltageIn3Min_num%26facet.field%3DVoltageIn3Max_num%26facet.field%3DVoltageOut3Min_num%26facet.field%3DVoltageOut3Max_num%26facet.field%3DCurrentOut3Max_num%26facet.field%3DSwitchFrequencyMax_num%26facet.field%3DSynchronousAsynchronous_copy%26facet.field%3DTechnology_copy%26facet.field%3DLightLoadMode_copy%26facet.field%3DEnTerminal_copy%26facet.field%3DPgood_copy%26facet.field%3DOperatingTemperatureMinIncludeJunctionTemperature_copy%26facet.field%3DOperatingTemperatureMaxIncludeJunctionTemperature_copy%26facet.field%3DPackageShortCode_copy%26facet.field%3DSmallReel_copy%26facet.field%3DThermalLink_copy%26facet.field%3DSpiceLink_copy%26facet.field%3DSupportPeriod_num%26facet.field%3DCommonStandard_copy%26facet.field%3DSaftyStandard_copy%26facet.field%3DRohmSolutionSimulatorLink_copy%26facet.field%3DEvaluationBoardLink_copy%26facet.field%3DPackageDimension_copy%26facet.field%3DIsRohsText_copy%26facet.field%3DPS_PartNodeCode%26sort%3DProductSupplyStatus_num%20desc%2C%20ProductDisplayFlag_num%20desc%2C%20PS_PartNumber%20asc%26q%3D%28PS_ProductDivisionCode%3A103030%20OR%20PS_ProductGroupCode%3A103030%20OR%20PS_ProductFamilyCode%3A103030%20OR%20PS_ProductTypeCode%3A103030%20OR%20PS_ProductSubTypeCode%3A%20103030%29%20AND%20ProductDisplayFlag_num%3A%5B1%20TO%20*%5D%20AND%20PS_PartStatus%3A60%20NOT%20TemplateViewName%3AViewWP_Part_Transistor_Template_200850"
url = "https://www.rohm.com/products/power-management/switching-regulators"
response = requests.get(url)

print(response.text)
print(response)
# print("Python requests的UA：", response.request.headers['User-Agent'])