from models import db,Memory,Cpu,Disk
from flask import render_template, request, redirect,flash,session,url_for
import psutil 



def homepage(is_logged_in=False,is_admin=False):

    return render_template("index.html")






def collect_system_info():
    memory_inf = psutil.virtual_memory()
    disk_usage = psutil.disk_usage("/")
    m=Memory(total=memory_inf.total,used=memory_inf.used,active=memory_inf.active,inactive= memory_inf.inactive,usage_percent=memory_inf.percent)
    d=Disk(total=disk_usage.total,used=disk_usage.total / (1024**3),free=disk_usage.used / (1024**3),usage_percent=disk_usage.free / (1024**3))
    
    db.session.add(m)
    db.session.add(d)
    db.session.commit()
    

    
    
    