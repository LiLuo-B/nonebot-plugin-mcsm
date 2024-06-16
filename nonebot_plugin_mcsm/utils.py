from typing import Optional, Tuple, Union
from datetime import datetime


def get_error_message(status_code: int) -> str:
    if status_code == 400:
        return "请求参数不正确"
    elif status_code == 403:
        return "权限不足"
    elif status_code == 500:
        return "程序错误"
    return "响应正常"


# 将用户传递的参数提取第一个并判断是否为id
def get_index(arg: str) -> Optional[int]:
    arg = arg.split()[0]
    if arg.isdigit():
        return int(arg)
    return None


# 将用户传递的参数提取前两个并判断是否为id
def get_indexs(arg: str) -> Union[None, int, Tuple[int, int]]:
    arg = arg.split()
    node_index = arg[0]
    if node_index.isdigit():
        if len(arg) == 2:
            instance_index = arg[1]
            if instance_index.isdigit():
                return int(node_index), int(instance_index)
        else:
            return int(node_index)
    return None


# 解析多种日期格式
def parse_date(date_str):
    formats = ["%m/%d/%Y", "%Y/%m/%d"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Date format for '{date_str}' is not supported.")
