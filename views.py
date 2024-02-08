from models import db,Memory,Cpu,Disk
from flask import render_template, request, redirect,flash,session,url_for
import psutil 



def homepage():
    collect_system_info()
    return render_template("index.html")






def collect_system_info():
    memory_inf = psutil.virtual_memory()
    disk_usage = psutil.disk_usage("/")
    cpu_times = psutil.cpu_times()
    m=Memory(total=memory_inf.total,used=memory_inf.used,active=memory_inf.active,inactive= memory_inf.inactive,usage_percent=memory_inf.percent)
    d=Disk(total=disk_usage.total,used=disk_usage.total / (1024**3),free=disk_usage.used / (1024**3),usage_percent=disk_usage.free / (1024**3))
    cpu_data = Cpu(times_user=cpu_times.user, times_system=cpu_times.system, times_idle=cpu_times.idle, usage_percent=psutil.cpu_percent(interval=1))
    db.session.add(m)
    db.session.add(d)
    db.session.add(cpu_data)
    db.session.commit()
    

    
    

