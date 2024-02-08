from models import db, Memory, Cpu, Disk
from flask import render_template, current_app
import psutil 
import time


def homepage():
    return render_template("index.html")

def CPU_Usage():
    return render_template("cpu_usage.html", cpu_counts=psutil.cpu_count)

def Memory_Utilization():
    return render_template("memory_utilization.html", total_memory=psutil.virtual_memory.total)

def Disk_Space():
    return render_template("disk_space.html", total_space=psutil.disk_usage.total)

def Active_Processes():
    return render_template("active_processes.html")

def collect_system_info():
    while True:
        memory_inf = psutil.virtual_memory()
        disk_usage = psutil.disk_usage("/")
        cpu_times = psutil.cpu_times()
        m = Memory(used=memory_inf.used,active=memory_inf.active,inactive= memory_inf.inactive,usage_percent=memory_inf.percent)
        d = Disk(used=disk_usage.total / (1024**3),free=disk_usage.used / (1024**3),usage_percent=disk_usage.free / (1024**3))
        cpu_data = Cpu(times_user=cpu_times.user, times_system=cpu_times.system, times_idle=cpu_times.idle, usage_percent=psutil.cpu_percent(interval=1))
        #processes table HERE
        db.session.add(m)
        db.session.add(d)
        db.session.add(cpu_data)
        db.session.commit()
        time.sleep(60)