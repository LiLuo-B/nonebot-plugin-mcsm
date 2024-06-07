from pydantic import BaseModel
from pathlib import Path
from nonebot import get_plugin_config


class Config(BaseModel):
    mcsm_path: str = Path.cwd() / "data/mcsm"
    mcsm_api_key: str
    mcsm_url:str


plugin_config = get_plugin_config(Config)
