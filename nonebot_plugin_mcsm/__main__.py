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
    for node in nodes.remote_nodes:
        await show_node_list.send(
            f"序号：{node.index}，名称：{node.remark}，是否在线：{node.status}"
        )
    await show_node_list.finish()


@show_instance_list.handle()
async def _(args: Message = CommandArg()):
    await get_instance_list()
