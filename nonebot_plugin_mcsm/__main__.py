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
from .mcsm_api import get_node_list, get_instance_list

show_node_list = on_command("节点列表", permission=SUPERUSER)
show_instance_list = on_command("实例列表", permission=SUPERUSER)


@show_node_list.handle()
async def _():
    nodes = await get_node_list()
    print(nodes)
    print(nodes.online_node)
    print(nodes.total_node)
    for node in nodes.remote_nodes:
        print(node.daemon_id)
        print(node.cpu_usage)

@show_instance_list.handle()
async def _():
    await get_instance_list()
