from models import db, Memory, Cpu, Disk, Active_processes
from flask import jsonify, render_template,request,session,flash,redirect,url_for
import psutil 
import paramiko



def homepage():
    hostname = session.get('hostname', 'Local')  
    return render_template("homepage.html", hostname=hostname)

def CPU_Usage(host='localhost'):
    cpu_cores=psutil.cpu_count()
    cpu_data = Cpu.query.filter(Cpu.host_ip==host).all()

    return render_template("cpu_usage.html", cpu_counts=cpu_cores,cpu_list=cpu_data)

def cpu_usage_data(host='localhost'):
    cpu_cores = psutil.cpu_count()
    cpu_data = Cpu.query.filter(Cpu.host_ip==host).all()
    cpu_data_list = [{
        'id': cur_cpu.id,
        'measurement_time': cur_cpu.measurement_time,
        'times_system': cur_cpu.times_system,
        'times_idle': cur_cpu.times_idle,
        'usage_percent': cur_cpu.usage_percent,
    } for cur_cpu in cpu_data]
    return jsonify({'cpu_counts': cpu_cores, 'cpu_list': cpu_data_list})

def Memory_Utilization(host='localhost'):
    mem_info_gb = psutil.virtual_memory().total/(1024 ** 3)
    mem_info_gb_formatted = "{:.2f} GB".format(mem_info_gb)
    mem_data = Memory.query.filter(Memory.host_ip==host).all()
    return render_template("memory_utilization.html", total_memory=mem_info_gb_formatted,mem_list=mem_data)

def memory_utilization_data(host='localhost'):
    mem_data = Memory.query.filter(Memory.host_ip==host).all()
    data = [{
        'id': mem.id,
        'measurement_time': mem.measurement_time,
        'used': mem.used,
        'active': mem.active,
        'inactive': mem.inactive,
        'usage_percent': mem.usage_percent,
    } for mem in mem_data]
    return jsonify({'mem_list':data,'total_memory':0})
    
def Disk_Space(host='localhost'):
    Disk_data=Disk.query.filter(Disk.host_ip==host).all()
    return render_template("disk_space.html", total_space=psutil.disk_usage('/').total,disk_list=Disk_data)

def disk_space_data(host='localhost'):
    Disk_data=Disk.query.filter(Disk.host_ip==host).all()
    data = [{
        'id': disk.id,
        'measurement_time': disk.measurement_time,
        'used': disk.used,
        'free': disk.free,
        'usage_percent': disk.usage_percent,
    } for disk in Disk_data]
    return jsonify({'disk_list':data})




def Active_Processes(host='localhost'):
    active_processes_data = Active_processes.query.filter(Active_processes.host_ip==host).all()
    return render_template("active_processes.html", active_processes_list=active_processes_data)

def active_processes_data(host='localhost'):
    active_processes_data = Active_processes.query.filter(Active_processes.host_ip==host).all()
    active__list = [{
        'pid': procces.pid,
        'measurement_time': procces.measurement_time,
        'name': procces.name,
        'status': procces.status,
        'start_date': procces.start_date,
    } for procces in active_processes_data]
    return jsonify({'active_processes_list': active__list})





def ssh_connect():
    hostname = request.form['hostname']
    username = request.form['username']
    password = request.form['password']  # Hardcoded for demonstration, replace with your actual password

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)
        ssh.close() 
        session['hostname'] = hostname
        flash('SSH connection successful.', 'success')
        return redirect(url_for('homepage'))
    except Exception as e:
        flash('SSH connection successful.', 'fail')
    return redirect(url_for('homepage'))
