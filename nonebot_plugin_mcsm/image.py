from nonebot import require
from typing import List
from pathlib import Path
import jinja2
from .model import Instance_Info

require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import html_to_pic

resources_path = Path(__file__).resolve().parent / "static"
templates_path = resources_path / "templates"
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(templates_path),
    enable_async=True,
)


async def node_list_img(instances: List[Instance_Info]):
    template = env.get_template("node_list.html")
