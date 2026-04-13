import json
from common.utils.logger import get_logger
# from common.core.clean_run import manage_complete_run
from common.mq.mq_producer import ProducerManager
from list_parse import parse_product_list
from common.config.settings import settings

logger = get_logger("firstsilicon-product-run")


if __name__ == "__main__":
    producer = ProducerManager.create_producer(config_key="producer-firstsilicon",
                                               topic=settings.MQ_TASK_TOPIC_NAME,
                                               vpc=False)
    with open("firstsilicon.json", "r", encoding="utf-8") as f:
        seed_data = json.load(f)
        for item in seed_data:
            path = item["url"]
            category = item["category"]
            result_field = parse_product_list(path, category=category)

            logger.info(f"\n共提取到 {len(result_field)} 个产品的 fieldMap---{path}")
            for i, fm in enumerate(result_field):
                # print(f"\n第{i + 1} 个产品的 fieldMap：")
                # print(json.dumps(fm, ensure_ascii=False, indent=4))
                if fm:
                    logger.info(f"{fm}解析完成")
                    print(fm)
                    messages = {
                        "body": fm,
                        "topic": settings.MQ_TASK_TOPIC_NAME,
                        "tag": "producer=firstsilicon",
                    }
                    producer.send_message(**messages)
                    # manage_complete_run(fm)
                else:
                    logger.info(f"{fm}解析结果为空")

        producer.shutdown()