import requests
from curl_cffi import requests
import re

payload  = {
    "requests": [
        {
            "indexName": "prod_main_en",
            "params": "facetingAfterDistinct=true&facets=%5B%22fDocType.lvl0%22%2C%22fFeatured%22%5D&filters=type%3A'Document'%20AND%20(nid%3A25570833%20OR%20nid%3A25577814)%20AND%20NOT%20staging%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=15&maxValuesPerFacet=100&page=0&query="
        }
        # {
        #     "indexName": "prod_main_en",
        #     "params": "facetingAfterDistinct=true&facets=%5B%22fDocType.lvl0%22%2C%22fFeatured%22%5D&filters=type%3A'Document'%20AND%20(nid%3A25541531%20OR%20nid%3A25557166%20OR%20nid%3A25557171)%20AND%20NOT%20staging%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=15&maxValuesPerFacet=100&page=0&query="
        # },
        # {
        #     "indexName": "prod_main_en_documents",
        #     "params": "facetingAfterDistinct=true&facets=%5B%22fDocType.lvl0%22%2C%22fFeatured%22%5D&filters=(nid%3A25541531)%20AND%20type%3A'Document'%20AND%20NOT%20staging%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=5&maxValuesPerFacet=100&page=0&query="
        # },
        # {
        #     "indexName": "prod_main_en_documents",
        #     "params": "facetingAfterDistinct=true&facets=%5B%22fDocType.lvl0%22%2C%22fFeatured%22%5D&filters=(nid%3A25541531%20OR%20nid%3A25557166%20OR%20nid%3A25557171)%20AND%20fDocType.lvl0%3A'Application%20Notes%20%26%20White%20Papers'%20AND%20type%3A'Document'%20AND%20NOT%20staging%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=5&maxValuesPerFacet=100&page=0&query="
        # },
        # {
        #     "indexName": "prod_main_en_documents",
        #     "params": "facetingAfterDistinct=true&facets=%5B%22fDocType.lvl0%22%2C%22fFeatured%22%5D&filters=(nid%3A25541531%20OR%20nid%3A25557166%20OR%20nid%3A25557171)%20AND%20fDocType.lvl0%3A'Datasheets'%20AND%20type%3A'Document'%20AND%20NOT%20staging%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=5&maxValuesPerFacet=100&page=0&query="
        # },
        # {
        #     "indexName": "prod_main_en_documents",
        #     "params": "facetingAfterDistinct=true&facets=%5B%27fDocType.lvl0%27%2C%27fFeatured%27%5D&filters=(nid%3A25570833+OR+nid%3A25577814)%20AND%20fDocType.lvl0%3A%27Datasheets%27%20AND%20type%3A%27Document%27%20AND%20NOT%20staging%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=5&maxValuesPerFacet=100&page=0&query="
        # }

        # {
        #     "indexName": "prod_main_en_documents",
        #     "params": "facetingAfterDistinct=true&facets=%5B%22fDocType.lvl0%22%2C%22fFeatured%22%5D&filters=(nid%3A25541531%20OR%20nid%3A25557166%20OR%20nid%3A25557171)%20AND%20fDocType.lvl0%3A'Errata%20%26%20Technical%20Updates'%20AND%20type%3A'Document'%20AND%20NOT%20staging%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=5&maxValuesPerFacet=100&page=0&query="
        # },
        # {
        #     "indexName": "prod_main_en_documents",
        #     "params": "facetingAfterDistinct=true&facets=%5B%22fDocType.lvl0%22%2C%22fFeatured%22%5D&filters=(nid%3A25541531%20OR%20nid%3A25557166%20OR%20nid%3A25557171)%20AND%20fDocType.lvl0%3A'Manuals%20%26%20Guides'%20AND%20type%3A'Document'%20AND%20NOT%20staging%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=5&maxValuesPerFacet=100&page=0&query="
        # },
        # {
        #     "indexName": "prod_main_en_documents",
        #     "params": "facetingAfterDistinct=true&facets=%5B%22fDocType.lvl0%22%2C%22fFeatured%22%5D&filters=(nid%3A25541531%20OR%20nid%3A25557166%20OR%20nid%3A25557171)%20AND%20fDocType.lvl0%3A'Marketing%20Collateral'%20AND%20type%3A'Document'%20AND%20NOT%20staging%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=5&maxValuesPerFacet=100&page=0&query="
        # },
        # {
        #     "indexName": "prod_main_en_documents",
        #     "params": "facetingAfterDistinct=true&facets=%5B%22fDocType.lvl0%22%2C%22fFeatured%22%5D&filters=(nid%3A25541531%20OR%20nid%3A25557166%20OR%20nid%3A25557171)%20AND%20fDocType.lvl0%3A'Models'%20AND%20type%3A'Document'%20AND%20NOT%20staging%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=5&maxValuesPerFacet=100&page=0&query="
        # },
        # {
        #     "indexName": "prod_main_en_documents",
        #     "params": "facetingAfterDistinct=true&facets=%5B%22fDocType.lvl0%22%2C%22fFeatured%22%5D&filters=(nid%3A25541531%20OR%20nid%3A25557166%20OR%20nid%3A25557171)%20AND%20fDocType.lvl0%3A'Other'%20AND%20type%3A'Document'%20AND%20NOT%20staging%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=5&maxValuesPerFacet=100&page=0&query="
        # },
        # {
        #     "indexName": "prod_main_en_documents",
        #     "params": "facetingAfterDistinct=true&facets=%5B%22fDocType.lvl0%22%2C%22fFeatured%22%5D&filters=(nid%3A25541531%20OR%20nid%3A25557166%20OR%20nid%3A25557171)%20AND%20fDocType.lvl0%3A'Product%20Notices%20(PCN%2C%20EOL%2C%20etc)'%20AND%20type%3A'Document'%20AND%20NOT%20staging%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=5&maxValuesPerFacet=100&page=0&query="
        # },
        # {
        #     "indexName": "prod_main_en_documents",
        #     "params": "facetingAfterDistinct=true&facets=%5B%22fDocType.lvl0%22%2C%22fFeatured%22%5D&filters=(nid%3A25541531%20OR%20nid%3A25557166%20OR%20nid%3A25557171)%20AND%20fDocType.lvl0%3A'Package%20%26%20Pinout%20Diagrams'%20AND%20type%3A'Document'%20AND%20NOT%20staging%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=5&maxValuesPerFacet=100&page=0&query="
        # },
        # {
        #     "indexName": "prod_main_en_documents",
        #     "params": "facetingAfterDistinct=true&facets=%5B%22fDocType.lvl0%22%2C%22fFeatured%22%5D&filters=(nid%3A25541531%20OR%20nid%3A25557166%20OR%20nid%3A25557171)%20AND%20fDocType.lvl0%3A'Quality%20%26%20Reliability'%20AND%20type%3A'Document'%20AND%20NOT%20staging%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=5&maxValuesPerFacet=100&page=0&query="
        # },
        # {
        #     "indexName": "prod_main_en_documents",
        #     "params": "facetingAfterDistinct=true&facets=%5B%22fDocType.lvl0%22%2C%22fFeatured%22%5D&filters=(nid%3A25541531%20OR%20nid%3A25557166%20OR%20nid%3A25557171)%20AND%20fDocType.lvl0%3A'Schematics%20%26%20Design%20Files'%20AND%20type%3A'Document'%20AND%20NOT%20staging%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=5&maxValuesPerFacet=100&page=0&query="
        # },
        # {
        #     "indexName": "prod_main_en_documents",
        #     "params": "facetingAfterDistinct=true&facets=%5B%22fDocType.lvl0%22%2C%22fFeatured%22%5D&filters=(nid%3A25541531%20OR%20nid%3A25557166%20OR%20nid%3A25557171)%20AND%20fDocType.lvl0%3A'Software%2C%20Tools%2C%20%26%20Sample%20Code'%20AND%20type%3A'Document'%20AND%20NOT%20staging%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=5&maxValuesPerFacet=100&page=0&query="
        # },
        # {
        #     "indexName": "prod_main_en_documents",
        #     "params": "facetingAfterDistinct=true&facets=%5B%22fDocType.lvl0%22%2C%22fFeatured%22%5D&filters=(nid%3A25541531%20OR%20nid%3A25557166%20OR%20nid%3A25557171)%20AND%20fDocType.lvl0%3A'Tool%20News'%20AND%20type%3A'Document'%20AND%20NOT%20staging%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=5&maxValuesPerFacet=100&page=0&query="
        # },
        # {
        #     "indexName": "prod_main_en_documents",
        #     "params": "facetingAfterDistinct=true&facets=%5B%22fDocType.lvl0%22%2C%22fFeatured%22%5D&filters=(nid%3A25541531%20OR%20nid%3A25557166%20OR%20nid%3A25557171)%20AND%20fDocType.lvl0%3A'Certificate'%20AND%20type%3A'Document'%20AND%20NOT%20staging%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=5&maxValuesPerFacet=100&page=0&query="
        # }
    ]
}

headers = {
    # "Content-Type": "application/json",
    # 注意：Algolia接口通常需要认证，若请求失败，需补充这两个头（需要获取对应的ID和Key）：
    "x-algolia-application-id": "KJ220GAQ35",
    "x-algolia-api-key": "YjFlY2I5NTUxM2ZlN2RkMmRmNmRhNjM2MDA1ZmNmMTRmODE0NTA5N2ViNmM1YTEwNjg2NjE0MzcxNzc3NzgyY2ZpbHRlcnM9cHVibGljbHlMaXN0ZWQlM0F0cnVlK09SK2RvY0FjY2VzcyUzQWxvY2stYW5vbnltb3VzK09SK2RvY0FjY2VzcyUzQW5vLWxvY2srT1IrTk9UK2J1bmRsZSUzQWRvY3VtZW50"
}

# 发送POST请求
url = "https://kj220gaq35-1.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.22.1)%3B%20Browser%3B%20instantsearch.js%20(4.80.0)%3B%20JS%20Helper%20(3.26.0)"
response = requests.post(url, headers=headers, json=payload)

# 打印响应结果
print(response.json())


a = {
    "results": [
        {
            "hits": [
                {
                    "dDate": "2025-10-29T07:00:00Z",
                    "fPill": [
                        "Documents"
                    ],
                    "nid": "25577814",
                    "documentRevision": "",
                    "fileExt": "PDF",
                    "dFileSize": "219 KB",
                    "isSample": false,
                    "isGeneratedAbstract": false,
                    "softwareAndToolsType": null,
                    "isSoftwareAndTools": false,
                    "prodStatusPriority": null,
                    "orderables4": null,
                    "fFeaturedST": [],
                    "search_api_datasource": "entity:node",
                    "body": "",
                    "extra": {
                        "title": "PCN25021 - Addition of assembly facility and Datasheet Revision for listed Renesas QFN and TQFN packaged devices",
                        "field_meta_keyword": "",
                        "document_body": "x0153118",
                        "categories": "product change notice"
                    },
                    "agileId": "X0153118",
                    "fProdCat": {
                        "lvl0": [
                            "Power Management",
                            "Interface"
                        ],
                        "lvl1": [
                            "Power Management > Battery Management ICs",
                            "Interface > USB Products",
                            "Power Management > DC/DC Converters"
                        ],
                        "lvl2": [
                            "Power Management > Battery Management ICs > Battery Charger ICs",
                            "Interface > USB Products > Power Management",
                            "Power Management > DC/DC Converters > Step-down (Buck)"
                        ],
                        "lvl3": [
                            "Interface > USB Products > Power Management > USB-C Power",
                            "Power Management > DC/DC Converters > Step-down (Buck) > Buck Controllers (External FETs)"
                        ],
                        "lvl4": [
                            "Interface > USB Products > Power Management > USB-C Power > USB-C & Power Delivery"
                        ]
                    },
                    "fileType": "Product Change Notice",
                    "fileTypeId": 611,
                    "orderables": null,
                    "orderables8": null,
                    "originalFileName": "PCN25021 customer notice.pdf",
                    "translationLinks": [],
                    "date": 1761721200,
                    "relatedCat": [
                        79,
                        481251,
                        481261,
                        77,
                        25573527,
                        1614886,
                        481581,
                        481321,
                        481351,
                        481366
                    ],
                    "indexed": 1762548558,
                    "indexedFrom": {
                        "time": "2025-11-07 20:49:18 UTC",
                        "server": "www.renesas.com",
                        "request_uri": "/",
                        "user_agent": "Symfony",
                        "php_self": "/app/vendor/bin/drush"
                    },
                    "title": "PCN25021 - Addition of assembly facility and Datasheet Revision for listed Renesas QFN and TQFN packaged devices",
                    "linkAttributes": {
                        "data-doc": "25577814",
                        "data-doc-lang": "en",
                        "data-external-doc": 0,
                        "data-file-extension": "pdf",
                        "data-nid": "25577814",
                        "data-secure": 0,
                        "data-uuid": "b7fb504d-741e-4b51-97fb-ae315bcfe337",
                        "hreflang": "en",
                        "rel": "",
                        "title": "PCN25021 - Addition of assembly facility and Datasheet Revision for listed Renesas QFN and TQFN packaged devices"
                    },
                    "docAccess": "no-lock",
                    "bundle": "document",
                    "orderables9": null,
                    "tornado": {
                        "app": [],
                        "appTech": null,
                        "compilerType": [],
                        "docTypeLv2": "",
                        "func": [],
                        "func2": [],
                        "famName": [],
                        "ideType": [],
                        "revision": "",
                        "sampleDesc": "",
                        "fileType": "Product Change Notice",
                        "fileSubtype": ""
                    },
                    "objectID": "25577814:pdf",
                    "orderables6": null,
                    "documentId": [],
                    "fFeatured": [],
                    "fDocType": {
                        "lvl0": "Product Notices (PCN, EOL, etc)",
                        "lvl1": "Product Notices (PCN, EOL, etc) > Product Change Notice"
                    },
                    "relatedSoft": [],
                    "search_api_id": "entity:node/25577814:en",
                    "search_api_language": "en",
                    "source": "renesas.com",
                    "dEyebrow": "Product Change Notice",
                    "url": "/document/pcn/pcn25021-addition-assembly-facility-and-datasheet-revision-listed-renesas-qfn-and-tqfn-packaged",
                    "originalLang": "en",
                    "orderables1": null,
                    "contentGroup": [],
                    "bundleScore": 50,
                    "type": "Document",
                    "staging": false,
                    "orderables5": null,
                    "lastRevised": 1761721200,
                    "orderables2": null,
                    "relatedDoc": [],
                    "_snippetResult": {
                        "title": {
                            "value": "PCN25021 - Addition of assembly facility and Datasheet Revision for listed Renesas QFN and TQFN packaged devices",
                            "matchLevel": "none"
                        },
                        "body": {
                            "value": "",
                            "matchLevel": "none"
                        }
                    },
                    "abstract": "",
                    "_highlightResult": {
                        "title": {
                            "value": "PCN25021 - Addition of assembly facility and Datasheet Revision for listed Renesas QFN and TQFN packaged devices",
                            "matchLevel": "none",
                            "matchedWords": []
                        },
                        "body": {
                            "value": "",
                            "matchLevel": "none",
                            "matchedWords": []
                        }
                    },
                    "created": 1761833714,
                    "orderables3": null,
                    "filePath": "private://docs/X015/X0153118/REN_PCN25021_PCN_20251029.pdf",
                    "fileSize": 219,
                    "userGroup": [],
                    "relatedDocLinks": [],
                    "changed": 1761870205,
                    "orderables7": null,
                    "isModel": false
                },
                {
                    "bundle": "document",
                    "staging": false,
                    "created": 1739898665,
                    "orderables9": null,
                    "relatedDoc": [],
                    "relatedSoft": [],
                    "search_api_id": "entity:node/25570833:en",
                    "bundleScore": 50,
                    "lastRevised": 1761634800,
                    "fDocType": {
                        "lvl0": "Datasheets",
                        "lvl1": "Datasheets > Datasheet"
                    },
                    "search_api_language": "en",
                    "orderables3": null,
                    "originalFileName": "RAA489300-Datasheet-20251028.pdf",
                    "nid": "25570833",
                    "indexedFrom": {
                        "time": "2025-10-28 15:42:27 UTC",
                        "server": "www.renesas.com",
                        "user": "user",
                        "request_uri": "/document/add?auth_token=46c4aa9ca8d73b76c54d27777a0856344c6358bcd6a3909792f99d4dc087e6a8&_format=xml&hash=8656a0048f372834a63eb97f96c0b21556c9c4144349a938e7c5fde1d243266d&parts=1&part=1",
                        "user_agent": "Java1.8.0_66",
                        "php_self": "/index.php"
                    },
                    "abstract": "The RAA489300 is a high-performance buck controller optimized for 3-level topology, delivering exceptional efficiency and reduced inductance. It supports seamless switching mode transitions, passthrough mode, and USB PD compliance with PPS/AVS. Advanced Renesas R3™ technology ensures fast response, low power loss, and robust protection features.",
                    "dDate": "2025-10-28T07:00:00Z",
                    "title": "RAA489300 Datasheet",
                    "extra": {
                        "title": "RAA489300 Datasheet",
                        "field_meta_keyword": "",
                        "document_body": "x0147573",
                        "categories": "datasheet"
                    },
                    "fFeatured": [
                        "25574025"
                    ],
                    "fileTypeId": 421,
                    "tornado": {
                        "app": [],
                        "appTech": null,
                        "compilerType": [],
                        "docTypeLv2": "",
                        "func": [],
                        "func2": [],
                        "famName": [],
                        "ideType": [],
                        "revision": "Rev.2.00",
                        "sampleDesc": "",
                        "fileType": "Datasheet",
                        "fileSubtype": ""
                    },
                    "changed": 1761666144,
                    "orderables5": null,
                    "orderables7": null,
                    "fileSize": 3369,
                    "fFeaturedST": [],
                    "isGeneratedAbstract": false,
                    "userGroup": [],
                    "objectID": "25570833",
                    "isSoftwareAndTools": false,
                    "contentGroup": [],
                    "type": "Document",
                    "dEyebrow": "Datasheet",
                    "orderables1": null,
                    "documentRevision": "",
                    "dFileSize": "3.29 MB",
                    "isModel": false,
                    "search_api_datasource": "entity:node",
                    "body": "",
                    "documentId": [
                        "R16DS0221EU0200",
                        "R16DS0221EU",
                        "R16DS0221"
                    ],
                    "fileExt": "PDF",
                    "softwareAndToolsType": null,
                    "date": 1761634800,
                    "orderables4": null,
                    "docAccess": "no-lock",
                    "relatedCat": [
                        79,
                        481321,
                        481351,
                        481366,
                        77,
                        25573527,
                        1614886,
                        481581
                    ],
                    "source": "renesas.com",
                    "originalLang": "en",
                    "agileId": "X0147573",
                    "translationLinks": [],
                    "fProdCat": {
                        "lvl0": [
                            "Power Management",
                            "Interface"
                        ],
                        "lvl1": [
                            "Power Management > DC/DC Converters",
                            "Interface > USB Products"
                        ],
                        "lvl2": [
                            "Power Management > DC/DC Converters > Step-down (Buck)",
                            "Interface > USB Products > Power Management"
                        ],
                        "lvl3": [
                            "Power Management > DC/DC Converters > Step-down (Buck) > Buck Controllers (External FETs)",
                            "Interface > USB Products > Power Management > USB-C Power"
                        ],
                        "lvl4": [
                            "Interface > USB Products > Power Management > USB-C Power > USB-C & Power Delivery"
                        ]
                    },
                    "relatedDocLinks": [],
                    "fPill": [
                        "Documents",
                        "Datasheet"
                    ],
                    "orderables": null,
                    "orderables8": null,
                    "linkAttributes": {
                        "data-doc": "25570833",
                        "data-doc-lang": "en",
                        "data-external-doc": 0,
                        "data-file-extension": "pdf",
                        "data-nid": "25570833",
                        "data-secure": 0,
                        "data-uuid": "566750b5-0964-434a-bea1-f6828e2ebdc0",
                        "hreflang": "en",
                        "rel": "",
                        "title": "RAA489300 Datasheet"
                    },
                    "indexed": 1761666147,
                    "prodStatusPriority": null,
                    "isSample": false,
                    "url": "/document/dst/raa489300-datasheet",
                    "filePath": "private://docs/X014/X0147573/REN_RAA489300_DST_20251028.pdf",
                    "fileType": "Datasheet",
                    "_snippetResult": {
                        "title": {
                            "value": "RAA489300 Datasheet",
                            "matchLevel": "none"
                        },
                        "body": {
                            "value": "",
                            "matchLevel": "none"
                        }
                    },
                    "_highlightResult": {
                        "title": {
                            "value": "RAA489300 Datasheet",
                            "matchLevel": "none",
                            "matchedWords": []
                        },
                        "body": {
                            "value": "",
                            "matchLevel": "none",
                            "matchedWords": []
                        },
                        "documentId": [
                            {
                                "value": "R16DS0221EU0200",
                                "matchLevel": "none",
                                "matchedWords": []
                            },
                            {
                                "value": "R16DS0221EU",
                                "matchLevel": "none",
                                "matchedWords": []
                            },
                            {
                                "value": "R16DS0221",
                                "matchLevel": "none",
                                "matchedWords": []
                            }
                        ]
                    },
                    "orderables2": null,
                    "orderables6": null,
                    "partNumber": [
                        "raa",
                        "raa4",
                        "raa48",
                        "raa489",
                        "raa4893",
                        "raa48930",
                        "raa489300",
                        "raa489300a",
                        "raa489300a3",
                        "raa489300ar",
                        "raa489300a3g",
                        "raa489300arg",
                        "raa489300a3gn",
                        "raa489300argn",
                        "raa489300a3gnp",
                        "raa489300argnp",
                        "raa489300a3gnp#a",
                        "raa489300a3gnp#h",
                        "raa489300argnp#a",
                        "raa489300argnp#h",
                        "raa489300a3gnp#aa",
                        "raa489300a3gnp#ha",
                        "raa489300argnp#aa",
                        "raa489300argnp#ha",
                        "raa489300a3gnp#aa0",
                        "raa489300a3gnp#ha0",
                        "raa489300argnp#aa0",
                        "raa489300argnp#ha0"
                    ]
                }
            ],
            "nbHits": 2,
            "hitsPerPage": 15,
            "index": "prod_main_en",
            "page": 0,
            "nbPages": 1,
            "processingTimeMS": 3,
            "processingTimingsMS": {
                "_request": {
                    "roundTrip": 11
                },
                "total": 3
            },
            "exhaustiveNbHits": true,
            "exhaustiveTypo": true,
            "facets_stats": {
                "fFeatured": {
                    "min": 25574025,
                    "max": 25574025,
                    "avg": 25574025,
                    "sum": 25574025
                }
            },
            "query": "",
            "params": "facetingAfterDistinct=true&facets=%5B%22fDocType.lvl0%22%2C%22fFeatured%22%5D&filters=type%3A%27Document%27+AND+%28nid%3A25570833+OR+nid%3A25577814%29+AND+NOT+staging%3Atrue&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=15&maxValuesPerFacet=100&page=0&query",
            "facets": {
                "fFeatured": {
                    "25574025": 1
                },
                "fDocType.lvl0": {
                    "Datasheets": 1,
                    "Product Notices (PCN, EOL, etc)": 1
                }
            },
            "renderingContent": {},
            "exhaustive": {
                "facetsCount": true,
                "nbHits": true,
                "typo": true
            },
            "exhaustiveFacetsCount": true
        }
    ]
}