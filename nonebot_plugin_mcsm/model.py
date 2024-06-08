from typing import Optional, List
from datetime import timedelta
import time


class Remote_Node:
    index: int
    connection_address: str
    status: bool
    cpu_usage: Optional[str] = None
    free_memory: Optional[float] = None
    total_memory: Optional[float] = None
    online_instance: Optional[int] = None
    total_instance: Optional[int] = None
    daemon_id: str
    remark: str
    platform: Optional[str] = None
    version: Optional[str] = None

    def __init__(self, index: int, data: dict):
        self.index = index
        self.connection_address = f"{data['ip']}:{data['port']}"
        self.status = data["available"]
        self.daemon_id = data["uuid"]
        self.remark = data["remarks"] if data["remarks"] else "localhost"
        if self.status == True:
            self.cpu_usage = "{:.1f}%".format(data["system"]["cpuUsage"] * 100)
            self.free_memory = (
                round(data["system"]["freemem"] / 1024 / 1024 / 1024 * 10, 1) / 10
            )
            self.total_memory = (
                round(data["system"]["totalmem"] / 1024 / 1024 / 1024 * 10, 1) / 10
            )
            self.online_instance = data["instance"]["running"]
            self.total_instance = data["instance"]["total"]
            self.platform = data["system"]["platform"]
            self.version = data["version"]


class Panel_Info:
    total_node: int
    online_node: int
    remote_nodes: List[Optional[Remote_Node]]

    def __init__(self, data: dict):
        self.total_node = data["remoteCount"]["total"]
        self.online_node = data["remoteCount"]["available"]
        self.remote_nodes = [
            Remote_Node(index + 1, node_data)
            for index, node_data in enumerate(data["remote"])
        ]


class Instance_Info:
    index: int
    instance_name: str
    instance_id: str
    instance_status: int
    start_command: str
    stop_command: str
    update_command: str
    instance_path: str
    last_run_time: str
    run_time: str
    cpu_usage: str
    memory_usage: float
    pid: int

    def __init__(self, index: int, data: dict):
        self.index = index
        self.instance_name = data["config"]["nickname"]
        self.instance_id = data["instanceUuid"]
        self.instance_status = data["status"]
        self.start_command = data["config"]["startCommand"]
        self.stop_command = data["config"]["stopCommand"]
        self.update_command = data["config"]["updateCommand"]
        self.instance_path = data["config"]["cwd"]
        self.last_run_time = time.strftime(
            "%Y-%m-%d  %H:%M:%S",
            time.localtime(data["config"]["lastDatetime"] / 1000),
        )
        self.run_time = timedelta(seconds=int(data["processInfo"]["elapsed"] / 1000))
        self.cpu_usage = "{:.1f}%".format(data["processInfo"]["cpu"] * 100)
        self.memory_usage = (
            round(data["processInfo"]["memory"] / 1024 / 1024 / 1024 * 10, 1) / 10
        )
        self.pid = data["processInfo"]["pid"]
