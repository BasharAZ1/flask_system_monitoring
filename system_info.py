from models import db, Memory, Cpu, Disk, ActiveProcesses
import psutil 
from shared import bytes_to_gb,kb_to_gb,current_hostname
from datetime import datetime


def collect_local_info():
        virtual_memory = psutil.virtual_memory()
        disk_usage = psutil.disk_usage("/")
        cpu_times = psutil.cpu_times()
        memory_data = Memory(used=round(bytes_to_gb(virtual_memory.used),2), 
                                 active=round(bytes_to_gb(virtual_memory.active),2),
                                 inactive=round(bytes_to_gb(virtual_memory.inactive),2),
                                usage_percent=virtual_memory.percent,
                                host_ip=current_hostname)
        disk_data = Disk(used=round(bytes_to_gb(disk_usage.used),2),
                             free=round(bytes_to_gb(disk_usage.free ),2) ,
                            usage_percent=disk_usage.percent,
                            host_ip=current_hostname)
        cpu_data = Cpu(times_user=round(cpu_times.user,2),
                           times_system=round(cpu_times.system,2), 
                           times_idle=round(cpu_times.idle,2),
                            usage_percent=psutil.cpu_percent(interval=1),
                            host_ip=current_hostname)

        db.session.query(ActiveProcesses).delete()
        for proc in psutil.process_iter(attrs=['pid', 'name', 'status', 'create_time']):
                try:
                    pid = proc.info['pid']
                    name = proc.info['name']
                    status = proc.info['status']
                    start_date = datetime.fromtimestamp(proc.info['create_time']).strftime('%Y-%m-%d %H:%M:%S.%f')
                    process = ActiveProcesses(pid=pid, name=name, status=status, start_date=start_date, host_ip=current_hostname)
                    db.session.add(process)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        db.session.add(memory_data)
        db.session.add(disk_data)
        db.session.add(cpu_data)
        db.session.commit()