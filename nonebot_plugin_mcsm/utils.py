from typing import Optional


def get_error_message(status_code: int) -> str:
    if status_code == 400:
        return "请求参数不正确"
    elif status_code == 403:
        return "权限不足"
    elif status_code == 500:
        return "程序错误"
    return "响应正常"


# 将用户传递参数的提取第一个并判断是否为id
def get_index(arg: str) -> Optional[int]:
    arg = arg.split()[0]
    if arg.isdigit():
        return int(arg)
    return None
