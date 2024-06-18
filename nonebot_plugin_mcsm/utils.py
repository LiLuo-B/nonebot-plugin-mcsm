from datetime import datetime


def get_error_message(status_code: int) -> str:
    if status_code == 400:
        return "请求参数不正确"
    elif status_code == 403:
        return "权限不足"
    elif status_code == 500:
        return "程序错误"
    return "响应正常"


# 解析多种日期格式
def parse_date(date_str):
    formats = ["%m/%d/%Y", "%Y/%m/%d"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Date format for '{date_str}' is not supported.")
