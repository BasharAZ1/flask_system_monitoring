from models import db, Memory, Cpu, Disk
from flask import jsonify, render_template, current_app
import psutil 
import time



def homepage():
    return render_template("homepage.html")

def CPU_Usage():
    cpu_cores=psutil.cpu_count()
    cpu_data = Cpu.query.all()
    return render_template("cpu_usage.html", cpu_counts=cpu_cores,cpu_list=cpu_data)

def cpu_usage_data():
    cpu_cores = psutil.cpu_count()
    cpu_data = Cpu.query.all()
    cpu_data_list = [{
        'id': cur_cpu.id,
        'measurement_time': cur_cpu.measurement_time,
        'times_system': cur_cpu.times_system,
        'times_idle': cur_cpu.times_idle,
        'usage_percent': cur_cpu.usage_percent,
    } for cur_cpu in cpu_data]
    return jsonify({'cpu_counts': cpu_cores, 'cpu_list': cpu_data_list})

def Memory_Utilization():
    mem_info_gb = psutil.virtual_memory().total/(1024 ** 3)
    mem_info_gb_formatted = "{:.2f} GB".format(mem_info_gb)
    mem_data = Memory.query.all()
    return render_template("memory_utilization.html", total_memory=mem_info_gb_formatted,mem_list=mem_data)

def memory_utilization_data():
    mem_data = Memory.query.order_by(Memory.id.desc()).all()  
    data = [{
        'id': mem.id,
        'measurement_time': mem.measurement_time,
        'used': mem.used,
        'active': mem.active,
        'inactive': mem.inactive,
        'usage_percent': mem.usage_percent,
    } for mem in mem_data]
    return jsonify(data)
    
def Disk_Space():
    Disk_data=Disk.query.all()
    return render_template("disk_space.html", total_space=psutil.disk_usage('/').total,disk_list=Disk_data)

def disk_space_data():
    disk_data = Disk.query.order_by(Disk.id.desc()).all() 
    data = [{
        'id': disk.id,
        'measurement_time': disk.measurement_time,
        'used': disk.used,
        'free': disk.free,
        'usage_percent': disk.usage_percent,
    } for disk in disk_data]
    return jsonify(data)




def Active_Processes():
    return render_template("active_processes.html")

def active_processes_data():
    pass






def collect_system_info():
    memory_inf = psutil.virtual_memory()
    disk_usage = psutil.disk_usage("/")
    cpu_times = psutil.cpu_times()
    m = Memory(used=memory_inf.used,active=memory_inf.active,inactive= memory_inf.inactive,usage_percent=memory_inf.percent)
    d = Disk(used=disk_usage.total / (1024**3),free=disk_usage.used / (1024**3),usage_percent=disk_usage.free / (1024**3))
    cpu_data = Cpu(times_user=cpu_times.user, times_system=cpu_times.system, times_idle=cpu_times.idle, usage_percent=psutil.cpu_percent(interval=1))
    db.session.add(m)
    db.session.add(d)
    db.session.add(cpu_data)
    db.session.commit()
    return jsonify(result="System info collected successfully")