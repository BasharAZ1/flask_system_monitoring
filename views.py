from models import Memory, Cpu, Disk, ActiveProcesses
from flask import jsonify, render_template
import psutil 
import shared


DEFAULT_HOSTNAME = 'localhost'

def homepage():
    hostname = shared.current_hostname
    return render_template("homepage.html", hostname=hostname)


def cpu_usage():
    return render_template("cpu_usage.html")


def cpu_usage_data():
    host = shared.current_hostname
    cpu_data = Cpu.query.filter(Cpu.host_ip==host).all()
    cpu_data_list = [{
            'id': curr_cpu.id,
            'measurement_time': curr_cpu.measurement_time[:-7],
            'times_user': f'{curr_cpu.times_user} seconds',
            'times_system': f'{curr_cpu.times_system} seconds',
            'times_idle': f'{curr_cpu.times_idle} seconds',
            'usage_percent': f'{curr_cpu.usage_percent}%',
        } for curr_cpu in cpu_data]
    if host == DEFAULT_HOSTNAME:
        cpu_cores = psutil.cpu_count()
    else:
        cpu_cores=0

    return jsonify({'cpu_counts': cpu_cores, 'cpu_list': cpu_data_list})


def memory_utilization():
    host = shared.current_hostname
    if host == DEFAULT_HOSTNAME:
        mem_info_gb = psutil.virtual_memory().total/(1024 ** 3)
        shared.mem_info_gb_formatted = "{:.2f} GB".format(mem_info_gb)
    else:
        shared.mem_info_gb_formatted="{:.2f} GB".format(0)

    return render_template("memory_utilization.html")


def memory_utilization_data():
    host = shared.current_hostname
    mem_data = Memory.query.filter(Memory.host_ip==host).all()
    data = [{
        'id': mem.id,
        'measurement_time': mem.measurement_time[:-7],
        'used': f'{mem.used} GB',
        'active': f'{mem.active} GB',
        'inactive': f'{mem.inactive} GB',
        'usage_percent': mem.usage_percent,
    } for mem in mem_data]
    
    return jsonify({'mem_list':data, 'total_memory':shared.mem_info_gb_formatted})


def disk_space():
    host = shared.current_hostname
    if host == DEFAULT_HOSTNAME:
        shared.total_space = f'{(psutil.disk_usage("/").total) / (1024.0 ** 3):.2f} GB'
    else:
        shared.total_space=0
        
    return render_template("disk_space.html")


def disk_space_data():
    host = shared.current_hostname
    disk_data=Disk.query.filter(Disk.host_ip==host).all()
    data = [{
        'id': disk.id,
        'measurement_time': disk.measurement_time[:-7],
        'used': f'{disk.used} GB',
        'free': f'{disk.free} GB',
        'usage_percent': disk.usage_percent,
    } for disk in disk_data]
    
    return jsonify({'disk_list':data,'total_space':shared.total_space})


def active_processes():
    return render_template("active_processes.html")


def active_processes_data():
    host = shared.current_hostname
    active_processes_data = ActiveProcesses.query.filter(ActiveProcesses.host_ip==host).all()
    active_list = [{
        'pid': procces.pid,
        'measurement_time': procces.measurement_time[:-7],
        'name': procces.name,
        'status': procces.status,
        'start_date': procces.start_date,
    } for procces in active_processes_data]
    
    return jsonify({'active_processes_list': active_list})







