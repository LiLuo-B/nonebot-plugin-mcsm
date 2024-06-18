from pydantic import BaseModel
from nonebot import get_plugin_config


class Config(BaseModel):
    mcsm_api_key: str
    mcsm_url: str
    mcsm_log_size: int = 1024
    mcsm_img_path: str


plugin_config = get_plugin_config(Config)