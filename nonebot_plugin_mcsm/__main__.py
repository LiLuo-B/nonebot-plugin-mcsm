from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import (
    MessageSegment,
    MessageEvent,
)
from nonebot.adapters.onebot.v11.message import Message
from .mcsm_api import (
    get_panel_info,
    get_node_list,
    get_instance_list,
    get_instance_info,
    start_instance,
    stop_instance,
    kill_instance,
    restart_instance,
    update_instance,
    get_instance_logs,
)
from .image import panel_info_img,node_info_img
from .utils import get_index, get_indexs

panel_info = on_command("面板信息", permission=SUPERUSER)
node_show_list = on_command("节点列表", permission=SUPERUSER)
instance_show_list = on_command("实例列表", permission=SUPERUSER)
instance_info = on_command("实例详情", permission=SUPERUSER)
instance_start = on_command("实例启动", permission=SUPERUSER)
instance_stop = on_command("实例关闭", permission=SUPERUSER)
instance_restart = on_command("实例重启", permission=SUPERUSER)
instance_kill = on_command("实例终止", permission=SUPERUSER)
instance_update = on_command("实例更新", permission=SUPERUSER)
instance_logs = on_command("实例日志", permission=SUPERUSER)


# 获取面板信息
@panel_info.handle()
async def _():
    panel = await get_panel_info()
    # 正常返回对象，异常返回int
    if isinstance(panel, int):
        await node_show_list.finish(f"节点查询失败,错误码{panel}")
    img = await panel_info_img(panel)
    await node_show_list.finish(MessageSegment.image(img))


# 获取节点列表
@node_show_list.handle()
async def _():
    nodes = await get_node_list()
    # 正常返回对象，异常返回int
    if isinstance(nodes, int):
        await node_show_list.finish(f"节点查询失败,错误码{nodes}")
    img=await node_info_img(nodes)
    await node_show_list.finish(MessageSegment.image(img))


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


# 获取实例信息
@instance_info.handle()
async def _(args: Message = CommandArg()):
    # 提取响应参数
    args = args.extract_plain_text()
    if args == "":
        await instance_info.pause("请输入节点ID")
    index = get_indexs(args)
    if index == None:
        await instance_info.finish("参数错误")
    # 正常返回对象，异常返回int
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_info.finish(f"节点查询失败，错误码{nodes}")
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
            await instance_info.finish(f"实例查询失败，错误码{instances}")
        # 若用户提供了两个参数则查询对应实例列表并判断
        if instance_index == -1:
            await instance_info.finish("参数错误")
        for instance in instances:
            # 若成功匹配实例index则调用实例详情获取函数
            if instance_index != instance.index:
                continue
            instance = await get_instance_info(node.daemon_id, instance.instance_id)
            if isinstance(instance, int):
                await instance_info.finish(f"查询失败，返回码{instance}")
            await instance_info.finish(f"实例信息：{instance.last_run_time}")
        await instance_info.finish("未查到该ID对应的实例")
    await instance_info.finish("未查到该ID对应的节点")


@instance_info.handle()
async def _(state: T_State, event: MessageEvent):
    node_index = get_index(str(event.message))
    # 用户参数为节点ID
    if not isinstance(node_index, int):
        await instance_info.finish("参数错误")
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_info.finish(f"节点查询失败，错误码{nodes}")
    for node in nodes:
        if node_index != node.index:
            continue
        state.update({"node_id": node.daemon_id})
        await instance_info.pause("请输入实例ID")
    await instance_info.finish("未查到该ID对应的节点")


@instance_info.got("node_id")
async def _(state: T_State, event: MessageEvent):
    instance_index = get_index(str(event.message))
    # 用户参数为实例ID
    if not isinstance(instance_index, int):
        await instance_info.finish("参数错误")
    daemon_id = state["node_id"]
    instances = await get_instance_list(daemon_id)
    if isinstance(instances, int):
        await instance_info.finish(f"实例查询失败，错误码{instances}")
    for instance in instances:
        if instance_index != instance.index:
            continue
        instance = await get_instance_info(daemon_id, instance.instance_id)
        if isinstance(instance, int):
            await instance_info.finish(f"查询失败，返回码{instance}")
        await instance_info.finish(f"实例信息：{instance.last_run_time}")
    await instance_info.finish("未查到该ID对应的实例")


# 启动实例
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


# 停止实例
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
    await instance_stop.finish("未查到该ID对应的实例")


# 重启实例
@instance_restart.handle()
async def _(args: Message = CommandArg()):
    # 提取响应参数
    args = args.extract_plain_text()
    if args == "":
        await instance_restart.pause("请输入节点ID")
    index = get_indexs(args)
    if index == None:
        await instance_restart.finish("参数错误")
    # 正常返回对象，异常返回int
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_restart.finish(f"节点查询失败，错误码{nodes}")
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
            await instance_restart.finish(f"实例查询失败，错误码{instances}")
        # 若用户提供了两个参数则查询对应实例列表并判断
        if instance_index == -1:
            await instance_restart.finish("参数错误")
        for instance in instances:
            # 若成功匹配实例index则调用重启函数
            if instance_index != instance.index:
                continue
            await instance_restart.send("指令已发送")
            return_code, return_text = await restart_instance(
                node.daemon_id, instance.instance_id
            )
            if return_code == 200:
                await instance_restart.finish("重启成功")
            await instance_restart.finish(return_text)
        await instance_restart.finish("未查到该ID对应的实例")
    await instance_restart.finish("未查到该ID对应的节点")


@instance_restart.handle()
async def _(state: T_State, event: MessageEvent):
    node_index = get_index(str(event.message))
    # 用户参数为节点ID
    if not isinstance(node_index, int):
        await instance_restart.finish("参数错误")
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_restart.finish(f"节点查询失败，错误码{nodes}")
    for node in nodes:
        if node_index != node.index:
            continue
        state.update({"node_id": node.daemon_id})
        await instance_restart.pause("请输入实例ID")
    await instance_restart.finish("未查到该ID对应的节点")


@instance_restart.got("node_id")
async def _(state: T_State, event: MessageEvent):
    instance_index = get_index(str(event.message))
    # 用户参数为实例ID
    if not isinstance(instance_index, int):
        await instance_restart.finish("参数错误")
    daemon_id = state["node_id"]
    instances = await get_instance_list(daemon_id)
    if isinstance(instances, int):
        await instance_restart.finish(f"实例查询失败，错误码{instances}")
    for instance in instances:
        if instance_index != instance.index:
            continue
        return_code, return_text = await restart_instance(
            daemon_id, instance.instance_id
        )
        if return_code == 200:
            await instance_restart.finish("重启成功")
        await instance_restart.finish(return_text)
    await instance_restart.finish("未查到该ID对应的实例")


# 终止实例
@instance_kill.handle()
async def _(args: Message = CommandArg()):
    # 提取响应参数
    args = args.extract_plain_text()
    if args == "":
        await instance_kill.pause("请输入节点ID")
    index = get_indexs(args)
    if index == None:
        await instance_kill.finish("参数错误")
    # 正常返回对象，异常返回int
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_kill.finish(f"节点查询失败，错误码{nodes}")
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
            await instance_kill.finish(f"实例查询失败，错误码{instances}")
        # 若用户提供了两个参数则查询对应实例列表并判断
        if instance_index == -1:
            await instance_kill.finish("参数错误")
        for instance in instances:
            # 若成功匹配实例index则调用终止函数
            if instance_index != instance.index:
                continue
            await instance_kill.send("指令已发送")
            return_code, return_text = await kill_instance(
                node.daemon_id, instance.instance_id
            )
            if return_code == 200:
                await instance_kill.finish("终止成功")
            await instance_kill.finish(return_text)
        await instance_kill.finish("未查到该ID对应的实例")
    await instance_kill.finish("未查到该ID对应的节点")


@instance_kill.handle()
async def _(state: T_State, event: MessageEvent):
    node_index = get_index(str(event.message))
    # 用户参数为节点ID
    if not isinstance(node_index, int):
        await instance_kill.finish("参数错误")
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_kill.finish(f"节点查询失败，错误码{nodes}")
    for node in nodes:
        if node_index != node.index:
            continue
        state.update({"node_id": node.daemon_id})
        await instance_kill.pause("请输入实例ID")
    await instance_kill.finish("未查到该ID对应的节点")


@instance_kill.got("node_id")
async def _(state: T_State, event: MessageEvent):
    instance_index = get_index(str(event.message))
    # 用户参数为实例ID
    if not isinstance(instance_index, int):
        await instance_kill.finish("参数错误")
    daemon_id = state["node_id"]
    instances = await get_instance_list(daemon_id)
    if isinstance(instances, int):
        await instance_kill.finish(f"实例查询失败，错误码{instances}")
    for instance in instances:
        if instance_index != instance.index:
            continue
        return_code, return_text = await kill_instance(daemon_id, instance.instance_id)
        if return_code == 200:
            await instance_kill.finish("终止成功")
        await instance_kill.finish(return_text)
    await instance_kill.finish("未查到该ID对应的实例")


# 更新实例
@instance_update.handle()
async def _(args: Message = CommandArg()):
    # 提取响应参数
    args = args.extract_plain_text()
    if args == "":
        await instance_update.pause("请输入节点ID")
    index = get_indexs(args)
    if index == None:
        await instance_update.finish("参数错误")
    # 正常返回对象，异常返回int
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_update.finish(f"节点查询失败，错误码{nodes}")
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
            await instance_update.finish(f"实例查询失败，错误码{instances}")
        # 若用户提供了两个参数则查询对应实例列表并判断
        if instance_index == -1:
            await instance_update.finish("参数错误")
        for instance in instances:
            # 若成功匹配实例index则调用更新函数
            if instance_index != instance.index:
                continue
            return_code, return_text = await update_instance(
                node.daemon_id, instance.instance_id
            )
            if return_code == 200:
                await instance_update.finish("更新指令已发送，可通过日志查询更新情况")
            await instance_update.finish(f"更新失败，f{return_text}")
        await instance_update.finish("未查到该ID对应的实例")
    await instance_update.finish("未查到该ID对应的节点")


@instance_update.handle()
async def _(state: T_State, event: MessageEvent):
    node_index = get_index(str(event.message))
    # 用户参数为节点ID
    if not isinstance(node_index, int):
        await instance_update.finish("参数错误")
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_update.finish(f"节点查询失败，错误码{nodes}")
    for node in nodes:
        if node_index != node.index:
            continue
        state.update({"node_id": node.daemon_id})
        await instance_update.pause("请输入实例ID")
    await instance_update.finish("未查到该ID对应的节点")


@instance_update.got("node_id")
async def _(state: T_State, event: MessageEvent):
    instance_index = get_index(str(event.message))
    # 用户参数为实例ID
    if not isinstance(instance_index, int):
        await instance_update.finish("参数错误")
    daemon_id = state["node_id"]
    instances = await get_instance_list(daemon_id)
    if isinstance(instances, int):
        await instance_update.finish(f"实例查询失败，错误码{instances}")
    for instance in instances:
        if instance_index != instance.index:
            continue
        return_code, return_text = await update_instance(
            daemon_id, instance.instance_id
        )
        if return_code == 200:
            await instance_update.finish("更新指令已发送，可通过日志查询更新情况")
        await instance_update.finish(f"更新失败，f{return_text}")
    await instance_update.finish("未查到该ID对应的实例")


# 实例日志获取
@instance_logs.handle()
async def _(args: Message = CommandArg()):
    # 提取响应参数
    args = args.extract_plain_text()
    if args == "":
        await instance_logs.pause("请输入节点ID")
    index = get_indexs(args)
    if index == None:
        await instance_logs.finish("参数错误")
    # 正常返回对象，异常返回int
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_logs.finish(f"节点查询失败，错误码{nodes}")
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
            await instance_logs.finish(f"实例查询失败，错误码{instances}")
        # 若用户提供了两个参数则查询对应实例列表并判断
        if instance_index == -1:
            await instance_logs.finish("参数错误")
        for instance in instances:
            # 若成功匹配实例index则调用更新函数
            if instance_index != instance.index:
                continue
            return_code, return_text = await get_instance_logs(
                node.daemon_id, instance.instance_id
            )
            if return_code == 200:
                await instance_logs.finish(f"日志获取成功\r\n{return_text}")
            await instance_logs.finish(f"日志获取失败，{return_text}")
        await instance_logs.finish("未查到该ID对应的实例")
    await instance_logs.finish("未查到该ID对应的节点")


@instance_logs.handle()
async def _(state: T_State, event: MessageEvent):
    node_index = get_index(str(event.message))
    # 用户参数为节点ID
    if not isinstance(node_index, int):
        await instance_logs.finish("参数错误")
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_logs.finish(f"节点查询失败，错误码{nodes}")
    for node in nodes:
        if node_index != node.index:
            continue
        state.update({"node_id": node.daemon_id})
        await instance_logs.pause("请输入实例ID")
    await instance_logs.finish("未查到该ID对应的节点")


@instance_logs.got("node_id")
async def _(state: T_State, event: MessageEvent):
    instance_index = get_index(str(event.message))
    # 用户参数为实例ID
    if not isinstance(instance_index, int):
        await instance_logs.finish("参数错误")
    daemon_id = state["node_id"]
    instances = await get_instance_list(daemon_id)
    if isinstance(instances, int):
        await instance_logs.finish(f"实例查询失败，错误码{instances}")
    for instance in instances:
        if instance_index != instance.index:
            continue
        return_code, return_text = await get_instance_logs(
            daemon_id, instance.instance_id
        )
        if return_code == 200:
            await instance_logs.finish(f"日志获取成功\r\n{return_text}")
        await instance_logs.finish(f"日志获取失败，{return_text}")
    await instance_logs.finish("未查到该ID对应的实例")
