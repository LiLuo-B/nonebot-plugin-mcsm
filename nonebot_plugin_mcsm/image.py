from nonebot import require
from pathlib import Path
from typing import List
import jinja2
from .model import Instance_Info, Panel_Info, Node_Info

require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import html_to_pic

resources_path = Path(__file__).resolve().parent / "static"
templates_path = resources_path / "templates"
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(templates_path),
    enable_async=True,
)


async def panel_info_img(panel_info: Panel_Info) -> bytes:
    template = env.get_template("panel_info.html")
    html = await template.render_async(
        resources_path=f"file://{resources_path}", panel_info=panel_info
    )
    return await html_to_pic(
        html,
        wait=0,
        viewport={"width": 1360, "height": 700},
        type="jpeg",
    )


async def node_list_img(node_list: List[Node_Info]) -> bytes:
    template = env.get_template("node_list.html")
    html = await template.render_async(
        resources_path=f"file://{resources_path}", node_list=node_list
    )
    return await html_to_pic(
        html,
        wait=0,
        viewport={
            "width": 1360,
            "height": 70 + 70 + 20 + 20 + 54 + 57 * len(node_list),
        },
        type="jpeg",
    )


async def instance_list_img(instance_list: List[Instance_Info]) -> bytes:
    template = env.get_template("instance_list.html")
    html = await template.render_async(
        resources_path=f"file://{resources_path}", instance_list=instance_list
    )
    return await html_to_pic(
        html,
        wait=0,
        viewport={
            "width": 1360,
            "height": 70 + 70 + 20 + 20 + 54 + 57 * len(instance_list),
        },
        type="jpeg",
    )
