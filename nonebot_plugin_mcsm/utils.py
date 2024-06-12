from typing import Optional, Tuple, Union


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
    daemon_index = arg[0]
    if daemon_index.isdigit():
        if len(arg) == 2:
            instance_index = arg[1]
            if instance_index.isdigit():
                return daemon_index, instance_index
        else:
            return daemon_index
    return None
