from models import db,Memory,Cpu,Disk
from flask import render_template, request, redirect,flash,session,url_for
import psutil 



def homepage(is_logged_in=False,is_admin=False):
    memory = psutil.virtual_memory()
    memory_utilization_percentage = memory.percent

    print(f"Memory Utilization Percentage: {memory_utilization_percentage}%")
    return render_template("index.html")






def collect_system_info():
    pass
def collect_memory():
    memory_inf = psutil.virtual_memory()
    memory_inf.percent
    memory_inf.available
    memory_inf.percent
    memory_inf.used
    memory_inf.free
    memory_inf.active
    memory_inf.inactive
    memory_inf.wired
    m=memory("")

    
    
def collect_diskspace():
    path = "/"
    disk_usage = psutil.disk_usage(path)
    print(f"Total Disk Space: {disk_usage.total / (1024**3):.2f} GB")
    print(f"Used Disk Space: {disk_usage.used / (1024**3):.2f} GB")
    print(f"Free Disk Space: {disk_usage.free / (1024**3):.2f} GB")
    print(f"Disk Usage Percentage: {disk_usage.percent}%")
    
    
def set_active_processes():
    pass
    
    
    