from datetime import timedelta
from typing import Optional, List


class Remote_Node:
    connection_address: str
    status: bool
    cpu_usage: str
    free_memory: float
    total_memory: float
    online_instance: int
    total_instance: int
    daemon_id: str
    remark: str
    platform: str
    version: str

    def __init__(self, data: dict):
        self.connection_address = f"{data['ip']}:{data['port']}"
        self.status = data["available"]
        self.cpu_usage = "{:.1f}%".format(data["system"]["cpuUsage"] * 100)
        self.free_memory = (
            round(data["system"]["freemem"] / 1024 / 1024 / 1024 * 10, 1) / 10
        )
        self.total_memory = (
            round(data["system"]["totalmem"] / 1024 / 1024 / 1024 * 10, 1) / 100
        )
        self.online_instance = data["instance"]["running"]
        self.total_instance = data["instance"]["total"]
        self.daemon_id = data["uuid"]
        self.remark = data["remarks"] if data["remarks"] else "localhost"
        self.platform = data["system"]["platform"]
        self.version = data["version"]


class Panel_Info:
    total_node: int
    online_node: int
    remote_nodes: List[Optional[Remote_Node]]

    def __init__(self, data: dict):
        self.total_node = data["remoteCount"]["total"]
        self.online_node = data["remoteCount"]["available"]
        self.remote_nodes = [Remote_Node(node_data) for node_data in data["remote"]]
