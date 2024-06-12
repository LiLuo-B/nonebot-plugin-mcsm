from nonebot import on_command, on_message, on_notice
from nonebot.params import CommandArg, CommandStart, RawCommand
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import (
    MessageSegment,
    MessageEvent,
    Event,
    NoticeEvent,
    PrivateMessageEvent,
    Bot,
)
from nonebot.adapters.onebot.v11.message import Message
from .mcsm_api import (
    get_node_list,
    get_instance_list,
    start_instance,
    stop_instance,
    kill_instance,
    restart_instance,
)
from .utils import get_index, get_indexs

show_node_list = on_command("节点列表", permission=SUPERUSER)
show_instance_list = on_command("实例列表", permission=SUPERUSER)
start_instance = on_command("实例启动", permission=SUPERUSER)
stop_instance = on_command("实例关闭", permission=SUPERUSER)
restart_instance = on_command("实例重启", permission=SUPERUSER)
kill_instance = on_command("实例终止", permission=SUPERUSER)


@show_node_list.handle()
async def _():
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await show_node_list.finish(f"节点查询失败,错误码{nodes}")
    for node in nodes:
        await show_node_list.send(
            f"序号：{node.index}，名称：{node.remark}，是否在线：{node.status}"
        )
    await show_node_list.finish()


@show_instance_list.handle()
async def _(args: Message = CommandArg()):
    if args := args.extract_plain_text():
        index = get_index(args)
        if index != None:
            nodes = await get_node_list()
            if isinstance(nodes, int):
                await show_instance_list.finish(f"节点查询失败，错误码{nodes}")
            for node in nodes:
                if index == node.index:
                    instances = await get_instance_list(node.daemon_id)
                    if isinstance(instances, int):
                        await show_instance_list.finish(
                            f"实例查询失败，错误码{instances}"
                        )
                    for instance in instances:
                        await show_instance_list.send(
                            f"序号：{instance.index} 备注：{instance.instance_name} 状态：{instance.instance_status} 启动命令：{instance.start_command} 停止命令：{instance.stop_command} 更新命令：{instance.update_command}"
                        )
                    await show_instance_list.finish()
            await show_instance_list.finish("没查到该ID对应的节点")
    await show_instance_list.pause("请输入节点ID")


@show_instance_list.handle()
async def _(event: MessageEvent):
    index = get_index(str(event.message))
    if index != None:
        nodes = await get_node_list()
        if isinstance(nodes, int):
            await show_instance_list.finish(f"节点查询失败，错误码{nodes}")
        for node in nodes:
            if index == node.index:
                instances = await get_instance_list(node.daemon_id)
                if isinstance(instances, int):
                    await show_instance_list.finish(f"查询失败，返回码{instances}")
                for instance in instances:
                    await show_instance_list.send(
                        f"序号：{instance.index} 备注：{instance.instance_name} 状态：{instance.instance_status} 启动命令：{instance.start_command} 停止命令：{instance.stop_command} 更新命令：{instance.update_command}"
                    )
                await show_instance_list.finish()
        await show_instance_list.finish("没查到该ID对应的节点")
    await show_instance_list.finish("参数错误，已退出流程")


@start_instance.handle()
async def _(args: Message = CommandArg()):
    if args := args.extract_plain_text():
        index = get_index(args)
        if index != None:
            nodes = await get_node_list()
            if isinstance(nodes, int):
                await show_instance_list.finish(f"节点查询失败，错误码{nodes}")
            for node in nodes:
                if index == node.index:
                    instances = await get_instance_list(node.daemon_id)
                    if isinstance(instances, int):
                        await show_instance_list.finish(
                            f"实例查询失败，错误码{instances}"
                        )
                    for instance in instances:
                        await show_instance_list.send(
                            f"序号：{instance.index} 备注：{instance.instance_name} 状态：{instance.instance_status} 启动命令：{instance.start_command} 停止命令：{instance.stop_command} 更新命令：{instance.update_command}"
                        )
                    await show_instance_list.finish()
            await show_instance_list.finish("没查到该ID对应的节点")
    await show_instance_list.pause("请输入节点ID")
