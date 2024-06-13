from nonebot import on_command, on_message, on_notice
from nonebot.params import CommandArg, CommandStart, RawCommand, ArgStr
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
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

node_show_list = on_command("节点列表", permission=SUPERUSER)
instance_show_list = on_command("实例列表", permission=SUPERUSER)
instance_start = on_command("实例启动", permission=SUPERUSER)
instance_stop = on_command("实例关闭", permission=SUPERUSER)
instance_restart = on_command("实例重启", permission=SUPERUSER)
instance_kill = on_command("实例终止", permission=SUPERUSER)


# 获取节点列表
@node_show_list.handle()
async def _():
    nodes = await get_node_list()
    # 正常返回对象，异常返回int
    if isinstance(nodes, int):
        await node_show_list.finish(f"节点查询失败,错误码{nodes}")
    for node in nodes:
        await node_show_list.send(
            f"序号：{node.index}，名称：{node.remark}，是否在线：{node.status}"
        )
    await node_show_list.finish()


# 获取实例列表
@instance_show_list.handle()
async def _(args: Message = CommandArg()):
    # 提取响应参数
    args = args.extract_plain_text()
    if args == "":
        await instance_show_list.pause("请输入节点ID")
    # 提取index
    index = get_index(args)
    if index == None:
        await instance_show_list.finish("参数错误")
    nodes = await get_node_list()
    # 正常返回对象，异常返回int
    if isinstance(nodes, int):
        await instance_show_list.finish(f"节点查询失败，错误码{nodes}")
        # 遍历节点列表查询index对应的节点daemon_id
    for node in nodes:
        if index != node.index:
            continue
        # 查询成功调用函数获取实例信息
        instances = await get_instance_list(node.daemon_id)
        # 正常返回对象，异常返回int
        if isinstance(instances, int):
            await instance_show_list.finish(f"实例查询失败，错误码{instances}")
        for instance in instances:
            await instance_show_list.send(
                f"序号：{instance.index} 备注：{instance.instance_name} 状态：{instance.instance_status} 启动命令：{instance.start_command} 停止命令：{instance.stop_command} 更新命令：{instance.update_command}"
            )
        await instance_show_list.finish()
    await instance_show_list.finish("未查到该ID对应的节点")


@instance_show_list.handle()
async def _(event: MessageEvent):
    # 提取响应参数
    index = get_index(str(event.message))
    if index == None:
        await instance_show_list.finish("参数错误，已退出流程")
    # 正常返回对象，异常返回int
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_show_list.finish(f"节点查询失败，错误码{nodes}")
    # 遍历节点列表查询index对应的节点daemon_id
    for node in nodes:
        if index != node.index:
            continue
        # 正常返回对象，异常返回int
        instances = await get_instance_list(node.daemon_id)
        if isinstance(instances, int):
            await instance_show_list.finish(f"查询失败，返回码{instances}")
            # 遍历节点列表查询index对应的实例instance_id
        for instance in instances:
            await instance_show_list.send(
                f"序号：{instance.index} 备注：{instance.instance_name} 状态：{instance.instance_status} 启动命令：{instance.start_command} 停止命令：{instance.stop_command} 更新命令：{instance.update_command}"
            )
        await instance_show_list.finish()
    await instance_show_list.finish("未查到该ID对应的节点")


@instance_start.handle()
async def _(args: Message = CommandArg()):
    # 提取响应参数
    args = args.extract_plain_text()
    if args == "":
        await instance_start.pause("请输入节点ID")
    index = get_indexs(args)
    if index == None:
        await instance_start.finish("参数错误")
    # 正常返回对象，异常返回int
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_start.finish(f"节点查询失败，错误码{nodes}")
    # 提取index，如果用户只提供了一个参数则返回node_index，instance_index为-1
    if isinstance(index, tuple):
        node_index, instance_index = index
    else:
        node_index = index
        instance_index = -1
    # 遍历节点列表查询index对应的节点daemon_id
    for node in nodes:
        if node_index != node.index:
            continue
        # 获取对应节点的实例列表
        instances = await get_instance_list(node.daemon_id)
        if isinstance(instances, int):
            await instance_start.finish(f"实例查询失败，错误码{instances}")
        # 若用户提供了两个参数则查询对应实例列表并判断
        if instance_index == -1:
            await instance_start.finish("参数错误")
        for instance in instances:
            # 若成功匹配实例index则调用启动函数
            if instance_index != instance.index:
                continue
            await instance_start.send("指令已发送")
            return_code, return_text = await start_instance(
                node.daemon_id, instance.instance_id
            )
            if return_code == 200:
                await instance_start.finish("启动成功")
            await instance_start.finish(return_text)
        await instance_start.finish("未查到该ID对应的实例")
    await instance_start.finish("未查到该ID对应的节点")


@instance_start.handle()
async def _(state: T_State, event: MessageEvent):
    node_index = get_index(str(event.message))
    # 用户参数为节点ID
    if not isinstance(node_index, int):
        await instance_start.finish("参数错误")
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_start.finish(f"节点查询失败，错误码{nodes}")
    for node in nodes:
        if node_index != node.index:
            continue
        state.update({"node_id": node.daemon_id})
        await instance_start.pause("请输入实例ID")
    await instance_start.finish("未查到该ID对应的节点")


@instance_start.got("node_id")
async def _(state: T_State, event: MessageEvent):
    instance_index = get_index(str(event.message))
    # 用户参数为实例ID
    if not isinstance(instance_index, int):
        await instance_start.finish("参数错误")
    daemon_id = state["node_id"]
    instances = await get_instance_list(daemon_id)
    if isinstance(instances, int):
        await instance_start.finish(f"实例查询失败，错误码{instances}")
    for instance in instances:
        if instance_index != instance.index:
            continue
        await instance_start.send("指令已发送")
        return_code, return_text = await start_instance(daemon_id, instance.instance_id)
        if return_code == 200:
            await instance_start.finish("启动成功")
        await instance_start.finish(return_text)
    await instance_start.finish("未查到该ID对应的实例")


@instance_stop.handle()
async def _(args: Message = CommandArg()):
    # 提取响应参数
    args = args.extract_plain_text()
    if args == "":
        await instance_stop.pause("请输入节点ID")
    index = get_indexs(args)
    if index == None:
        await instance_stop.finish("参数错误")
    # 正常返回对象，异常返回int
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_stop.finish(f"节点查询失败，错误码{nodes}")
    # 提取index，如果用户只提供了一个参数则返回node_index，instance_index为-1
    if isinstance(index, tuple):
        node_index, instance_index = index
    else:
        node_index = index
        instance_index = -1
    # 遍历节点列表查询index对应的节点daemon_id
    for node in nodes:
        if node_index != node.index:
            continue
        # 获取对应节点的实例列表
        instances = await get_instance_list(node.daemon_id)
        if isinstance(instances, int):
            await instance_stop.finish(f"实例查询失败，错误码{instances}")
        # 若用户提供了两个参数则查询对应实例列表并判断
        if instance_index == -1:
            await instance_stop.finish("参数错误")
        for instance in instances:
            # 若成功匹配实例index则调用关闭函数
            if instance_index != instance.index:
                continue
            await instance_stop.send("指令已发送")
            return_code, return_text = await stop_instance(
                node.daemon_id, instance.instance_id
            )
            if return_code == 200:
                await instance_stop.finish("关闭成功")
            await instance_stop.finish(return_text)
        await instance_stop.finish("未查到该ID对应的实例")
    await instance_stop.finish("未查到该ID对应的节点")


@instance_stop.handle()
async def _(state: T_State, event: MessageEvent):
    node_index = get_index(str(event.message))
    # 用户参数为节点ID
    if not isinstance(node_index, int):
        await instance_stop.finish("参数错误")
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_stop.finish(f"节点查询失败，错误码{nodes}")
    for node in nodes:
        if node_index != node.index:
            continue
        state.update({"node_id": node.daemon_id})
        await instance_stop.pause("请输入实例ID")
    await instance_stop.finish("未查到该ID对应的节点")


@instance_stop.got("node_id")
async def _(state: T_State, event: MessageEvent):
    instance_index = get_index(str(event.message))
    # 用户参数为实例ID
    if not isinstance(instance_index, int):
        await instance_stop.finish("参数错误")
    daemon_id = state["node_id"]
    instances = await get_instance_list(daemon_id)
    if isinstance(instances, int):
        await instance_stop.finish(f"实例查询失败，错误码{instances}")
    for instance in instances:
        if instance_index != instance.index:
            continue
        return_code, return_text = await stop_instance(daemon_id, instance.instance_id)
        if return_code == 200:
            await instance_stop.finish("关闭成功")
        await instance_stop.finish(return_text)
    await instance_stop.finish("为查到该ID对应的实例")
