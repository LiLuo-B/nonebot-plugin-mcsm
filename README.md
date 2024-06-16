<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>


<h1 align="center">MCSM小助手</h1>

_✨ 对接MCSM的管理插件，可用于查询面板、节点、实例信息以及管理实例✨_

<p align="center">
  <a href="https://raw.githubusercontent.com/cscs181/QQ-Github-Bot/master/LICENSE">
    <img src="https://img.shields.io/github/license/cscs181/QQ-Github-Bot.svg" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot-plugin-analysis-bilibili">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-analysis-bilibili.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</p>


## 安装

### nb-cli

```shell
nb plugin install nonebot_plugin_mcsm
```

### pip

```shell
pip install nonebot_plugin_mcsm
```

### git
```shell
git clone https://github.com/LiLuo-B/nonebot-plugin-mcsm.git
```

## 配置

### .env|.env.prod|.env.dev

| 配置项        | 说明                             |
| ------------- | -------------------------------- |
| mcsm_api_key  | MCSM API Key                     |
| mcsm_url      | MCSM面板地址                     |
| mcsm_img_path | 背景图片地址                     |
| mcsm_log_size | 日志输出大小（单位KB，默认1024） |

## 使用

| 指令     | 权限 | 相关参数                                              |
| -------- | ---- | ----------------------------------------------------- |
| 面板信息 | 超管 | 无                                                    |
| 节点列表 | 超管 | 无                                                    |
| 实例列表 | 超管 | 节点序号，可通过“节点列表”查看                        |
| 实例详情 | 超管 | 节点序号 实例序号，分别通过“节点列表”、“实例列表”查看 |
| 实例启动 | 超管 | 节点序号 实例序号，分别通过“节点列表”、“实例列表”查看 |
| 实例关闭 | 超管 | 节点序号 实例序号，分别通过“节点列表”、“实例列表”查看 |
| 实例重启 | 超管 | 节点序号 实例序号，分别通过“节点列表”、“实例列表”查看 |
| 实例终止 | 超管 | 节点序号 实例序号，分别通过“节点列表”、“实例列表”查看 |
| 实例更新 | 超管 | 节点序号 实例序号，分别通过“节点列表”、“实例列表”查看 |
| 实例日志 | 超管 | 节点序号 实例序号，分别通过“节点列表”、“实例列表”查看 |

## 示例

### 面板信息

<img src="https://github.com/LiLuo-B/nonebot-plugin-mcsm/blob/main/image/panel_info.png" width="800"></img>

### 节点列表

<img src="https://github.com/LiLuo-B/nonebot-plugin-mcsm/blob/main/image/node_list.png" width="800"></img>

### 实例列表

<img src="https://github.com/LiLuo-B/nonebot-plugin-mcsm/blob/main/image/instance_list.png" width="800"></img>

### 实例详情

<img src="https://github.com/LiLuo-B/nonebot-plugin-mcsm/blob/main/image/instance_info.png" width="800"></img>

### 实例重启

<img src="https://github.com/LiLuo-B/nonebot-plugin-mcsm/blob/main/image/instance_restart.png" width="800"></img>