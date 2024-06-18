from nonebot import require
from nonebot.permission import SUPERUSER

require("nonebot_plugin_alconna")
from arclet.alconna import Alconna, Args
from nonebot_plugin_alconna import Match, on_alconna, UniMessage, Image
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
from .image import panel_info_img, node_list_img, instance_list_img, instance_info_img

panel_info = on_alconna("面板信息", permission=SUPERUSER)
node_show_list = on_alconna("节点列表", permission=SUPERUSER)
instance_show_list = on_alconna(
    Alconna("实例列表", Args["node_index?", int]),
    permission=SUPERUSER,
)
instance_info = on_alconna(
    Alconna("实例详情", Args["node_index?", int]["instance_index?", int]),
    permission=SUPERUSER,
)
instance_start = on_alconna(
    Alconna("实例启动", Args["node_index?", int]["instance_index?", int]),
    permission=SUPERUSER,
)
instance_stop = on_alconna(
    Alconna("实例关闭", Args["node_index?", int]["instance_index?", int]),
    permission=SUPERUSER,
)
instance_restart = on_alconna(
    Alconna("实例重启", Args["node_index?", int]["instance_index?", int]),
    permission=SUPERUSER,
)
instance_kill = on_alconna(
    Alconna("实例终止", Args["node_index?", int]["instance_index?", int]),
    permission=SUPERUSER,
)
instance_update = on_alconna(
    Alconna("实例更新", Args["node_index?", int]["instance_index?", int]),
    permission=SUPERUSER,
)
instance_logs = on_alconna(
    Alconna("实例日志", Args["node_index?", int]["instance_index?", int]),
    permission=SUPERUSER,
)


# 获取面板信息
@panel_info.handle()
async def _():
    panel = await get_panel_info()
    # 正常返回对象，异常返回int
    if isinstance(panel, int):
        await panel_info.finish(f"面板查询失败,错误码{panel}")
    img = await panel_info_img(panel)
    await panel_info.finish(await UniMessage(Image(raw=img)).export())


# 获取节点列表
@node_show_list.handle()
async def _():
    nodes = await get_node_list()
    # 正常返回对象，异常返回int
    if isinstance(nodes, int):
        await node_show_list.finish(f"节点查询失败,错误码{nodes}")
    img = await node_list_img(nodes)
    await node_show_list.finish(await UniMessage(Image(raw=img)).export())


# 获取实例列表
@instance_show_list.handle()
async def _(node_index: Match[int]):
    if node_index.available:
        instance_show_list.set_path_arg("node_index", node_index.result)


@instance_show_list.got_path("node_index", prompt="请输入节点id")
async def _(node_index: int):
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_show_list.finish(f"节点查询失败，错误码{nodes}")
    # 遍历节点列表查询index对应的节点daemon_id
    for node in nodes:
        if node_index != node.index:
            continue
        # 正常返回对象，异常返回int
        instances = await get_instance_list(node.daemon_id)
        if isinstance(instances, int):
            await instance_show_list.finish(f"查询失败，错误码{instances}")
            # 遍历节点列表查询index对应的实例instance_id
        img = await instance_list_img(instances)
        await instance_show_list.finish(await UniMessage(Image(raw=img)).export())
    await instance_show_list.finish("未查到该ID对应的节点")


# 获取实例详情
@instance_info.handle()
async def _(node_index: Match[int], instance_index: Match[int]):
    if node_index.available and instance_index.available:
        instance_info.set_path_arg("node_index", node_index.result)
        instance_info.set_path_arg("instance_index", instance_index.result)


@instance_info.got_path("node_index", prompt="请输入节点id")
@instance_info.got_path("instance_index", prompt="请输入实例id")
async def _(node_index: int, instance_index: int):
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_info.finish(f"节点查询失败，错误码{nodes}")
    for node in nodes:
        if node_index != node.index:
            continue
        instances = await get_instance_list(node.daemon_id)
        if isinstance(instances, int):
            await instance_info.finish(f"查询失败，错误码{instances}")
        for instance in instances:
            if instance_index != instance.index:
                continue
            instance = await get_instance_info(node.daemon_id, instance.instance_id)
            if isinstance(instance, int):
                await instance_info.finish(f"查询失败，错误码{instance}")
            img = await instance_info_img(instance)
            await instance_show_list.finish(await UniMessage(Image(raw=img)).export())
    await instance_info.finish("未查到该ID对应的节点或实例")


# 启动实例
@instance_start.handle()
async def _(node_index: Match[int], instance_index: Match[int]):
    if node_index.available and instance_index.available:
        instance_start.set_path_arg("node_index", node_index.result)
        instance_start.set_path_arg("instance_index", instance_index.result)


@instance_start.got_path("node_index", prompt="请输入节点id")
@instance_start.got_path("instance_index", prompt="请输入实例id")
async def _(node_index: int, instance_index: int):
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_start.finish(f"节点查询失败，错误码{nodes}")
    for node in nodes:
        if node_index != node.index:
            continue
        instances = await get_instance_list(node.daemon_id)
        if isinstance(instances, int):
            await instance_start.finish(f"查询失败，错误码{instances}")
        for instance in instances:
            if instance_index != instance.index:
                continue
            await instance_stop.send("指令已发送")
            return_code, return_text = await start_instance(
                node.daemon_id, instance.instance_id
            )
            if return_code == 200:
                await instance_start.finish("启动成功")
            await instance_start.finish(return_text)
    await instance_start.finish("未查到该ID对应的节点或实例")


# 停止实例
@instance_stop.handle()
async def _(node_index: Match[int], instance_index: Match[int]):
    if node_index.available and instance_index.available:
        instance_stop.set_path_arg("node_index", node_index.result)
        instance_stop.set_path_arg("instance_index", instance_index.result)


@instance_stop.got_path("node_index", prompt="请输入节点id")
@instance_stop.got_path("instance_index", prompt="请输入实例id")
async def _(node_index: int, instance_index: int):
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_stop.finish(f"节点查询失败，错误码{nodes}")
    for node in nodes:
        if node_index != node.index:
            continue
        instances = await get_instance_list(node.daemon_id)
        if isinstance(instances, int):
            await instance_stop.finish(f"查询失败，错误码{instances}")
        for instance in instances:
            if instance_index != instance.index:
                continue
            await instance_stop.send("指令已发送")
            return_code, return_text = await stop_instance(
                node.daemon_id, instance.instance_id
            )
            if return_code == 200:
                await instance_stop.finish("关闭成功")
            await instance_stop.finish(return_text)
    await instance_stop.finish("未查到该ID对应的节点或实例")


# 重启实例
@instance_restart.handle()
async def _(node_index: Match[int], instance_index: Match[int]):
    if node_index.available and instance_index.available:
        instance_restart.set_path_arg("node_index", node_index.result)
        instance_restart.set_path_arg("instance_index", instance_index.result)


@instance_restart.got_path("node_index", prompt="请输入节点id")
@instance_restart.got_path("instance_index", prompt="请输入实例id")
async def _(node_index: int, instance_index: int):
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_restart.finish(f"节点查询失败，错误码{nodes}")
    for node in nodes:
        if node_index != node.index:
            continue
        instances = await get_instance_list(node.daemon_id)
        if isinstance(instances, int):
            await instance_restart.finish(f"查询失败，错误码{instances}")
        for instance in instances:
            if instance_index != instance.index:
                continue
            await instance_restart.send("指令已发送")
            return_code, return_text = await restart_instance(
                node.daemon_id, instance.instance_id
            )
            if return_code == 200:
                await instance_restart.finish("重启成功")
            await instance_restart.finish(return_text)
    await instance_restart.finish("未查到该ID对应的节点或实例")


# 终止实例
@instance_kill.handle()
async def _(node_index: Match[int], instance_index: Match[int]):
    if node_index.available and instance_index.available:
        instance_kill.set_path_arg("node_index", node_index.result)
        instance_kill.set_path_arg("instance_index", instance_index.result)


@instance_kill.got_path("node_index", prompt="请输入节点id")
@instance_kill.got_path("instance_index", prompt="请输入实例id")
async def _(node_index: int, instance_index: int):
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_kill.finish(f"节点查询失败，错误码{nodes}")
    for node in nodes:
        if node_index != node.index:
            continue
        instances = await get_instance_list(node.daemon_id)
        if isinstance(instances, int):
            await instance_kill.finish(f"查询失败，错误码{instances}")
        for instance in instances:
            if instance_index != instance.index:
                continue
            await instance_kill.send("指令已发送")
            return_code, return_text = await kill_instance(
                node.daemon_id, instance.instance_id
            )
            if return_code == 200:
                await instance_kill.finish("终止成功")
            await instance_kill.finish(return_text)
    await instance_kill.finish("未查到该ID对应的节点或实例")


# 更新实例
@instance_update.handle()
async def _(node_index: Match[int], instance_index: Match[int]):
    if node_index.available and instance_index.available:
        instance_update.set_path_arg("node_index", node_index.result)
        instance_update.set_path_arg("instance_index", instance_index.result)


@instance_update.got_path("node_index", prompt="请输入节点id")
@instance_update.got_path("instance_index", prompt="请输入实例id")
async def _(node_index: int, instance_index: int):
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_update.finish(f"节点查询失败，错误码{nodes}")
    for node in nodes:
        if node_index != node.index:
            continue
        instances = await get_instance_list(node.daemon_id)
        if isinstance(instances, int):
            await instance_update.finish(f"查询失败，错误码{instances}")
        for instance in instances:
            if instance_index != instance.index:
                continue
            return_code, return_text = await update_instance(
                node.daemon_id, instance.instance_id
            )
            if return_code == 200:
                await instance_update.finish("更新指令已发送，可通过日志查询更新情况")
            await instance_update.finish(f"更新失败，{return_text}")
    await instance_update.finish("未查到该ID对应的节点或实例")


# 实例日志获取
@instance_logs.handle()
async def _(node_index: Match[int], instance_index: Match[int]):
    if node_index.available and instance_index.available:
        instance_logs.set_path_arg("node_index", node_index.result)
        instance_logs.set_path_arg("instance_index", instance_index.result)


@instance_logs.got_path("node_index", prompt="请输入节点id")
@instance_logs.got_path("instance_index", prompt="请输入实例id")
async def _(node_index: int, instance_index: int):
    nodes = await get_node_list()
    if isinstance(nodes, int):
        await instance_logs.finish(f"节点查询失败，错误码{nodes}")
    for node in nodes:
        if node_index != node.index:
            continue
        instances = await get_instance_list(node.daemon_id)
        if isinstance(instances, int):
            await instance_logs.finish(f"查询失败，错误码{instances}")
        for instance in instances:
            if instance_index != instance.index:
                continue
            return_code, return_text = await get_instance_logs(
                node.daemon_id, instance.instance_id
            )
            if return_code == 200:
                await instance_logs.finish(f"日志获取成功\r\n{return_text}")
            await instance_logs.finish(f"日志获取失败，{return_text}")
    await instance_logs.finish("未查到该ID对应的节点或实例")
