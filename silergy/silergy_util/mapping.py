

def product_status(raw_status: str | None) -> str:

    status_mapping = {
        "预发布": "新产品",
        "正在供货": "量产",
        # "not recommended for new designs": "不推荐新设计",
        # "last time buy": "最后购买",
        # "obsolete": "停产",
    }
    if not raw_status:
        return "未知状态"

    key = raw_status.strip().lower()
    return status_mapping.get(key, "未知状态")


def application_level_mapping(raw_level: str | None) -> str:

    level_mapping = {
        "consumer": "消费级",
        "ndustrial": "工业级",
        "automotive": "车规级",
        # "hiRel enhanced product": "军工级",
        # "military": "军工级",
        # "space": "航天级",
        # "catalog": "消费级"
    }
    # 入参空/None/空白字符串，直接返回未知等级
    if not raw_level:
        return "未知等级"
    # 统一去首尾空格 + 转小写，再匹配映射表
    key = raw_level.strip().lower()
    # 无匹配则返回默认值"未知等级"
    return level_mapping.get(key, "未知等级")


# print(product_status("预发布"))
