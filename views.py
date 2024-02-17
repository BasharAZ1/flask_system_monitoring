from models import Memory, Cpu, Disk, ActiveProcesses,db
from flask import jsonify, render_template,request, session, flash, redirect, url_for
import psutil 
import shared
from shared import bytes_to_gb, mb_to_gb, current_hostname
from datetime import datetime
from models import db, Memory, Cpu, Disk, ActiveProcesses
import shared
import paramiko


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
            'cpu_counts':curr_cpu.total_cores,
        } for curr_cpu in cpu_data]
    last_cpu_data = cpu_data_list[-1]
    return jsonify({'cpu_counts': last_cpu_data['cpu_counts'], 'cpu_list': cpu_data_list})


def memory_utilization():
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
        'Total_memory':f'{mem.total_mem} GB',
    } for mem in mem_data]
    last_data = data[-1]
    return jsonify({'mem_list':data, 'total_memory':last_data['Total_memory']})


def disk_space():        
    return render_template("disk_space.html")


def disk_space_data():
    host = shared.current_hostname
    disk_data=Disk.query.filter(Disk.host_ip==host).all()
    data = [{
        'id': disk.id,
        'measurement_time': disk.measurement_time[:-7],
        'used': f'{disk.used}',
        'free': f'{disk.free}',
        'usage_percent': disk.usage_percent,
        'total_space': f'{disk.total_space} GB',
    } for disk in disk_data]
    last_data = data[-1]
    
    return jsonify({'disk_list':data,'total_space':last_data['total_space']})


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


def collect_local_info():
        virtual_memory = psutil.virtual_memory()
        disk_usage = psutil.disk_usage("/")
        cpu_times = psutil.cpu_times()
        mem_info_gb = psutil.virtual_memory().total/(1024 ** 3)
        total_space = round((psutil.disk_usage("/").total) / (1024.0 ** 3),2)
        mem_info_gb_formatted = "{:.2f}".format(mem_info_gb)
        memory_data = Memory(used=round(bytes_to_gb(virtual_memory.used),2), 
                                 active=round(bytes_to_gb(virtual_memory.active),2),
                                 inactive=round(bytes_to_gb(virtual_memory.inactive),2),
                                usage_percent=virtual_memory.percent,
                                total_mem=mem_info_gb_formatted,
                                host_ip=current_hostname)
        disk_data = Disk(used=round(bytes_to_gb(disk_usage.used),2),
                             free=round(bytes_to_gb(disk_usage.free ),2) ,
                            usage_percent=disk_usage.percent,
                            total_space=total_space,
                            host_ip=current_hostname)
        cpu_data = Cpu(times_user=round(cpu_times.user,2),
                           times_system=round(cpu_times.system,2), 
                           times_idle=round(cpu_times.idle,2),
                            usage_percent=psutil.cpu_percent(interval=1),
                            host_ip=current_hostname,
                            total_cores=psutil.cpu_count())

        db.session.query(ActiveProcesses).delete()
        for proc in psutil.process_iter(attrs=['pid', 'name', 'status', 'create_time']):
                try:
                    pid = proc.info['pid']
                    name = proc.info['name']
                    status = proc.info['status']
                    start_date = datetime.fromtimestamp(proc.info['create_time']).strftime('%Y-%m-%d %H:%M:%S')
                    process = ActiveProcesses(pid=pid, name=name, status=status, start_date=start_date, host_ip=current_hostname)
                    db.session.add(process)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        db.session.add(memory_data)
        db.session.add(disk_data)
        db.session.add(cpu_data)
        db.session.commit()


def ssh_connect():
    hostname = request.form['hostname']
    username = request.form['username']
    password = request.form['password']

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)
        session['hostname'] = hostname
        session['username'] = username
        session['password'] = password
        shared.current_hostname = hostname
        shared.current_username = username
        shared.current_password = password
        flash('SSH connection successful.', 'success')
        return redirect(url_for('homepage'))
    except Exception as e:
        flash('SSH connection failed.', 'fail')
    return redirect(url_for('homepage'))


def set_localhost():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.close()
    shared.current_hostname = 'localhost'
    shared.current_username = ''
    shared.current_password = ''
    flash('Localhost connection successful.', 'success')
    return redirect(url_for('homepage'))


def collect_remote_system_info(ssh_client):
    try:
        stdin, stdout, stderr = ssh_client.exec_command("top -bn 1 | grep Cpu")
        output = stdout.read().decode("utf-8")
        parts = output.split(',')
        times_user = round(float(parts[0].split()[1]),2)
        times_system = round(float(parts[1].split()[0]),2)
        times_idle = round(float(parts[3].split()[0]),2)
        usage_percent = round(100.0 - times_idle,2)
        stdin, stdout, stderr = ssh_client.exec_command("nproc")
        output = stdout.read().decode("utf-8")
        cpu_cores=output.split('\n')[0]
        cpu_data = Cpu(times_user=times_user,
                           times_system=times_system,
                           times_idle=times_idle,
                            usage_percent=usage_percent,
                            host_ip=shared.current_hostname,
                            total_cores=cpu_cores)
        stdin, stdout, stderr = ssh_client.exec_command("top -bn 1 | grep Mem")
        output = stdout.read().decode("utf-8")
        data_line = output.split('\n')[0]
        parts = output.split(',')
        mem_used=round(float(parts[2].split()[0]),2)
        free_mem=round(float(parts[1].split()[0]),2)
        total_mem=round(float(parts[0].split()[3]),2)
        usage_percent = (mem_used / total_mem) * 100
        stdin, stdout, stderr = ssh_client.exec_command('cat /proc/meminfo | grep -E "Active:|Inactive:"')
        output = stdout.read().decode("utf-8")
        active_mem_kb = output.split('\n')[0].split(':')[1]
        active_mem = active_mem_kb.split()[0]
        Inactive_mem_kb = output.split('\n')[1].split(':')[1]
        Inactive_mem = Inactive_mem_kb.split()[0]
        memory_data = Memory(used=round(mb_to_gb(mem_used),2), 
                                 active=shared.kb_to_gb(active_mem),
                                 inactive=shared.kb_to_gb(Inactive_mem),
                                usage_percent=round(usage_percent,2),
                                host_ip=shared.current_hostname,
                                total_mem=mb_to_gb(total_mem))
        stdin, stdout, stderr = ssh_client.exec_command('df -h /')
        output = stdout.read().decode("utf-8")
        data_line = output.split('\n')[1]
        parts=data_line.split()
        disk_size=parts[1]
        disk_used=parts[2]
        disk_avil=parts[3]
        disk_percent=parts[4]
        disk_data = Disk(used=round(float(disk_used[:-1]),2),
                             free=round(float(disk_avil[:-1]) ,2) ,
                            usage_percent=disk_percent[:1],
                            host_ip=shared.current_hostname,
                            total_space=disk_size)
        
        stdin, stdout, stderr = ssh_client.exec_command('ps -eo pid,comm,stat,lstart')
        output = stdout.read().decode("utf-8")
        lines = output.split('\n')

        db.session.query(ActiveProcesses).delete()
        for line in lines[1:]: 
                parts = line.split()
                if len(parts) < 5: 
                    continue
                pid = parts[0]
                stat = parts[2]
                startdate = ' '.join(parts[-5:])
                command = parts[1]
                process = ActiveProcesses(pid=pid, name=command, status=stat, start_date=startdate, host_ip=shared.current_hostname)
                db.session.add(process)

        db.session.add(cpu_data)
        db.session.add(disk_data)
        db.session.add(memory_data)
        db.session.commit()


    except Exception as e:
        print("Error:", e)
        return None

