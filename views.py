from models import Memory, Cpu, Disk, ActiveProcesses
from flask import jsonify, render_template, request, session, flash, redirect, url_for
import psutil 
import paramiko
import shared


DEFAULT_HOSTNAME = 'localhost'

def homepage():
    hostname = shared.current_hostname
    return render_template("homepage.html", hostname=hostname)


def cpu_usage():
    host = shared.current_hostname
    cpu_data = Cpu.query.filter(Cpu.host_ip==host).all()
    if host == DEFAULT_HOSTNAME:
        cpu_cores=psutil.cpu_count()
    else:
        cpu_cores=0

    return render_template("cpu_usage.html", cpu_counts=cpu_cores, cpu_list=cpu_data)


def cpu_usage_data():
    host = shared.current_hostname
    cpu_data = Cpu.query.filter(Cpu.host_ip==host).all()
    cpu_data_list = [{
            'id': curr_cpu.id,
            'measurement_time': curr_cpu.measurement_time,
            'times_system': curr_cpu.times_system,
            'times_idle': curr_cpu.times_idle,
            'usage_percent': curr_cpu.usage_percent,
        } for curr_cpu in cpu_data]
    if host == DEFAULT_HOSTNAME:
        cpu_cores = psutil.cpu_count()
    else:
        cpu_cores=0

    return jsonify({'cpu_counts': cpu_cores, 'cpu_list': cpu_data_list})


def memory_utilization():
    host = shared.current_hostname
    mem_data = Memory.query.filter(Memory.host_ip==host).all()
    if host == DEFAULT_HOSTNAME:
        mem_info_gb = psutil.virtual_memory().total/(1024 ** 3)
        mem_info_gb_formatted = "{:.2f} GB".format(mem_info_gb)
    else:
        mem_info_gb_formatted="{:.2f} GB".format(0)

    return render_template("memory_utilization.html", total_memory=mem_info_gb_formatted, mem_list=mem_data)


def memory_utilization_data():
    host = shared.current_hostname
    mem_data = Memory.query.filter(Memory.host_ip==host).all()
    data = [{
        'id': mem.id,
        'measurement_time': mem.measurement_time,
        'used': mem.used,
        'active': mem.active,
        'inactive': mem.inactive,
        'usage_percent': mem.usage_percent,
    } for mem in mem_data]
    
    return jsonify({'mem_list':data, 'total_memory':0})


def disk_space():
    host = shared.current_hostname
    disk_data=Disk.query.filter(Disk.host_ip==host).all()
    if host == DEFAULT_HOSTNAME:
        total_space=psutil.disk_usage('/').total
    else:
        total_space=0
        
    return render_template("disk_space.html", total_space=total_space, disk_list=disk_data)


def disk_space_data():
    host = shared.current_hostname
    disk_data=Disk.query.filter(Disk.host_ip==host).all()
    data = [{
        'id': disk.id,
        'measurement_time': disk.measurement_time,
        'used': disk.used,
        'free': disk.free,
        'usage_percent': disk.usage_percent,
    } for disk in disk_data]
    
    return jsonify({'disk_list':data})


def active_processes():
    host = shared.current_hostname
    active_processes_data = ActiveProcesses.query.filter(ActiveProcesses.host_ip==host).all()
    
    return render_template("active_processes.html", active_processes_list=active_processes_data)


def active_processes_data():
    host = shared.current_hostname
    active_processes_data = ActiveProcesses.query.filter(ActiveProcesses.host_ip==host).all()
    active_list = [{
        'pid': procces.pid,
        'measurement_time': procces.measurement_time,
        'name': procces.name,
        'status': procces.status,
        'start_date': procces.start_date,
    } for procces in active_processes_data]
    
    return jsonify({'active_processes_list': active_list})


def ssh_connect():
    hostname = request.form['hostname']
    username = request.form['username']
    password = request.form['password']

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)
        session['hostname'] = hostname
        shared.current_hostname = hostname
        flash('SSH connection successful.', 'success')
        return redirect(url_for('homepage'))
    except Exception as e:
        flash('SSH connection successful.', 'fail')
    return redirect(url_for('homepage'))
