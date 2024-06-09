import asyncio
import httpx
from typing import Union, List
from .config import plugin_config
from .model import Panel_Info, Instance_Info

panel_address = plugin_config.mcsm_url.rstrip("/")
api_key = plugin_config.mcsm_api_key
headers = {"Content-Type": "application/json; charset=utf-8"}


# 获取节点列表
async def get_node_list() -> Union[Panel_Info, int]:
    url = f"{panel_address}/api/overview"
    params = {"apikey": plugin_config.mcsm_api_key}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        data = response.json()
        if response.status_code == 200:
            return Panel_Info(data["data"])
        return response.status_code


# 获取实例信息
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


# 获取实例列表
async def get_instance_list(daemonid: str) -> List[Instance_Info]:
    pass
