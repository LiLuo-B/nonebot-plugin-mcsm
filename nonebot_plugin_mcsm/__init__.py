from nonebot.plugin import PluginMetadata
from . import __main__ as __main__
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_mcsm",
    description="NoneBot插件，对接MCSM，可通过机器人来管理实例",
    usage="私聊或群里发送消息",
    type="application",
    homepage="https://github.com/LiLuo-B/nonebot-plugin-mcsm",
    config=Config,
    supported_adapters={"~onebot.v11"},
)
