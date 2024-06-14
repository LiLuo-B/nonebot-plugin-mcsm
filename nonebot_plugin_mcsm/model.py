from typing import Optional
from datetime import timedelta
import time


class Node_Info:
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
    panel_version: str
    panel_cpu_usage: str
    panel_memory_usage: str
    system_cpu_usage: str
    system_memory_usage: str
    system_memory_total:str
    system_type: str
    system_daemon_version: str
    system_version: str
    system_node_version: str
    system_host_name: str
    system_user_name: str
    system_time: str
    system_run_time: str
    node_total_count:int
    node_online_count:int
    instance_total_count:int
    instance_online_count:int


    def __init__(self, data: dict):
        self.panel_version = data["version"]
        self.panel_cpu_usage = "{:.1f}%".format(data["process"]["cpu"] * 100)
        self.panel_memory_usage = (
            f"{round(data['process']['memory'] / 1024 / 1024 * 10, 1) / 10}MB"
        )
        self.system_cpu_usage="{:.1f}%".format(data["system"]["cpu"] * 100)
        self.system_memory_usage="{:.1f}G".format((data["system"]["totalmem"]-data["system"]["freemem"])/1024/1024/1024)
        self.system_memory_total="{:.1f}G".format(data["system"]["totalmem"]/1024/1024/1024)
        self.system_type=f"{data['system']['type']} {data['system']['platform']}"
        self.system_daemon_version=data["specifiedDaemonVersion"]
        self.system_version=f"{data['system']['version']} {data['system']['release']}"
        self.system_node_version=data["system"]["node"]
        self.system_host_name=data["system"]["hostname"]
        self.system_user_name=data["system"]["user"]["username"]
        self.system_time=time.strftime(
            "%Y/%m/%d  %H:%M:%S",
            time.localtime(data["system"]["time"] / 1000),
        )
        self.system_run_time=timedelta(seconds=int(data["system"]["uptime"] ))
        self.node_online_count=data["remoteCount"]["available"]
        self.node_total_count=data["remoteCount"]["total"]
        online_count=0
        total_count=0
        for instance in data["remote"]:
            online_count+=instance["instance"]["running"]
            total_count+=instance["instance"]["total"]
        self.instance_online_count = sum(instance["instance"]["running"] for instance in data["remote"])
        self.instance_total_count = sum(instance["instance"]["total"] for instance in data["remote"])


class Instance_Info:
    index: Optional[int]
    instance_name: str
    instance_id: str
    instance_status: int
    start_command: str
    stop_command: str
    update_command: str
    instance_path: str
    last_run_time: str
    run_time: Optional[str] = None
    cpu_usage: Optional[str] = None
    memory_usage: Optional[float] = None
    pid: Optional[int] = None

    def __init__(self, detail: bool, data: dict, index: int = -1):
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
        if detail == True:
            self.run_time = timedelta(
                seconds=int(data["processInfo"]["elapsed"] / 1000)
            )
            self.cpu_usage = "{:.1f}%".format(data["processInfo"]["cpu"] * 100)
            self.memory_usage = (
                round(data["processInfo"]["memory"] / 1024 / 1024 / 1024 * 10, 1) / 10
            )
            self.pid = data["processInfo"]["pid"]
