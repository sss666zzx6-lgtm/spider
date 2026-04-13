import json
from list_parse import parse_product_data_from,application_level_mapping
from product_parse import parse_product_detail
from common.utils.logger import get_logger
# from common.mongo.clean_run import manage_complete_run
from common.mq.mq_producer import ProducerManager
from common.config.settings import settings
from common.utils.create_darwin_api import create_api

logger = get_logger("product-run")

if __name__ == "__main__":
    # url = "https://www.silergy.com/list/294"
    # product_data = parse_product_data_from(url)
    # print(json.dumps(product_data, indent=4, ensure_ascii=False))

    headers = {
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
    }

    producer = ProducerManager.create_producer(config_key="producer-silergy",
                                               topic=settings.MQ_TASK_TOPIC_NAME,
                                               vpc=False)

    with open("silergy.json", "r", encoding="utf-8") as f:
        seed_data = json.load(f)
        for item in seed_data:
            path = item["url"]
            category = item["category"]
            product_data = parse_product_data_from(path)
            logger.info(f"{path}共提取到 {len(product_data)} 个产品数据：")
            for idx, prod in enumerate(product_data, 1):
                ppn = prod["part_number"]
                application_level = application_level_mapping(prod["part_type"])
                product_url = f"https://www.silergy.com/productsview/{ppn}"
                datasheet = prod["datasheet"]

                fieldMap = parse_product_detail(product_url, ppn, application_level,category=category,datasheet_id=datasheet)
                if fieldMap:
                    # if idx < 15:
                    #     continue
                    if idx > 3:
                        break
                    logger.info(f"{ppn}解析完成")
                    print(fieldMap)
                    datasheet_url = fieldMap["datasheets"][0]["raw_path"]
                    print(datasheet_url)
                    custom_map = {"category": "datasheet"}
                    # create_api(plan_id="8b7e8a806c217c04f4e6c5063e08e6a2", path=datasheet_url, custom_map=custom_map,
                    #            headers=headers, fetch_method=2)
                    fieldMap_2 = {
                                    "field_map": fieldMap,
                                  }
                    messages = {
                        "body": fieldMap_2,
                        "topic": settings.MQ_TASK_TOPIC_NAME,
                        "tag": settings.MQ_TASK_TAG,
                    }
                    producer.send_message(**messages)
                    # manage_complete_run(fieldMap)

                else:
                    logger.info(f"{ppn}解析结果为空")
            break

        producer.shutdown()



