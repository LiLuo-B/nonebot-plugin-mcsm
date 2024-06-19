from nonebot.plugin import PluginMetadata, inherit_supported_adapters
from . import __main__ as __main__
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="MCSM小助手",
    description="对接MCSM，可查看面板、节点、实例信息以及管理实例",
    usage="私聊或群里发送消息",
    type="application",
    homepage="https://github.com/LiLuo-B/nonebot-plugin-mcsm",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
)
