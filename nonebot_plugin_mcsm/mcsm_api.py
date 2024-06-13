import asyncio
import httpx
from typing import Union, List, Tuple
from .config import plugin_config
from .model import Node_Info, Instance_Info

panel_address = plugin_config.mcsm_url.rstrip("/")
api_key = plugin_config.mcsm_api_key
headers = {"Content-Type": "application/json; charset=utf-8"}


# 获取节点列表 查询成功返回实例信息，失败返回错误码
async def get_node_list() -> Union[List[Node_Info], int]:
    url = f"{panel_address}/api/overview"
    params = {"apikey": plugin_config.mcsm_api_key}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        data = response.json()
        if response.status_code == 200:
            return [
                Node_Info(index=index + 1, data=node)
                for index, node in enumerate(data["data"]["remote"])
            ]
        return response.status_code


# 获取实例信息 查询成功返回实例信息，失败返回错误码
async def get_instance_info(
    daemonid: str, instanceid: str
) -> Union[Instance_Info, int]:
    url = f"{panel_address}/api/instance"
    params = {
        "uuid": instanceid,
        "remote_uuid": daemonid,
        "apikey": plugin_config.mcsm_api_key,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        data = response.json()
        if response.status_code == 200:
            return Instance_Info(detail=True, data=data["data"])
        return response.status_code


# 获取实例列表 查询成功返回实例信息，失败返回错误码
async def get_instance_list(daemonid: str) -> Union[List[Instance_Info], int]:
    url = f"{panel_address}/api/service/remote_service_instances"
    params = {
        "daemonId": daemonid,
        "page": 1,
        "page_size": 100,
        "status": "",
        "instance_name": "",
        "apikey": plugin_config.mcsm_api_key,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        data = response.json()
        if response.status_code == 200:
            return [
                Instance_Info(detail=False, data=instance, index=index + 1)
                for index, instance in enumerate(data["data"]["data"])
            ]
        return response.status_code


# 启动实例 返回返回码与文本
async def start_instance(daemonid: str, instanceid: str) -> Tuple[int, str]:
    url = f"{panel_address}/api/protected_instance/open"
    params = {
        "uuid": instanceid,
        "daemonId": daemonid,
        "apikey": plugin_config.mcsm_api_key,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        data = response.json()
    return response.status_code, data["data"]


# 关闭实例 返回返回码与文本
async def stop_instance(daemonid: str, instanceid: str) -> Tuple[int, str]:
    url = f"{panel_address}/api/protected_instance/stop"
    params = {
        "uuid": instanceid,
        "daemonId": daemonid,
        "apikey": plugin_config.mcsm_api_key,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        data = response.json()
    return response.status_code, data["data"]


# 终止实例 返回返回码与文本
async def kill_instance(daemonid: str, instanceid: str) -> Tuple[bool, int]:
    url = f"{panel_address}/api/protected_instance/kill"
    params = {
        "uuid": instanceid,
        "daemonId": daemonid,
        "apikey": plugin_config.mcsm_api_key,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        data = response.json()
    return response.status_code, data["data"]


# 重启实例 返回返回码与文本
async def restart_instance(daemonid: str, instanceid: str) -> Tuple[bool, int]:
    url = f"{panel_address}/api/protected_instance/restart"
    params = {
        "uuid": instanceid,
        "daemonId": daemonid,
        "apikey": plugin_config.mcsm_api_key,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        data = response.json()
    return response.status_code, data["data"]


# 更新实例 返回返回码与文本
async def update_instance(daemonid: str, instanceid: str) -> Tuple[bool, int]:
    url = f"{panel_address}/api/protected_instance/asynchronous"
    params = {
        "uuid": instanceid,
        "daemonId": daemonid,
        "task_name": "update",
        "apikey": plugin_config.mcsm_api_key,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, params=params)
        data = response.json()
    return response.status_code, data["data"]


# 获取实例日志 返回返回码与文本
async def get_instance_logs(daemonid: str, instanceid: str) -> Tuple[bool, int]:
    url = f"{panel_address}/api/protected_instance/outputlog"
    params = {
        "uuid": instanceid,
        "daemonId": daemonid,
        "size": plugin_config.mcsm_log_size,
        "apikey": plugin_config.mcsm_api_key,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        data = response.json()
    return response.status_code, data["data"]
