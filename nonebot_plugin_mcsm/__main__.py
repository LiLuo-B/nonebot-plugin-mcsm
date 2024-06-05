from nonebot import on_command, on_message, on_notice
from nonebot.params import CommandArg, CommandStart, RawCommand
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import (
    MessageSegment,
    Event,
    NoticeEvent,
    PrivateMessageEvent,
    Bot,
)
from nonebot.adapters.onebot.v11.message import Message
from .config import plugin_config
import httpx

show_node_list = on_command("节点列表", permission=SUPERUSER)


@show_node_list.handle()
async def get_node_list():
    url = f"http://{plugin_config.mcsm_ip}:{plugin_config.mcsm_port}/api/service/remote_services_system"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    params = {"apikey": plugin_config.mcsm_api_key}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            print(data)
            await show_node_list.finish()
        else:
            await show_node_list.finish("异常")
