def get_error_message(status_code: int) -> str:
    if status_code == 400:
        return "请求参数不正确"
    elif status_code == 403:
        return "权限不足"
    elif status_code == 500:
        return "程序错误"
    return "响应正常"
