from models import db, Memory, Cpu, Disk, ActiveProcesses
import shared
import paramiko
from flask import  request, session, flash, redirect, url_for
import paramiko


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
        cpu_data = Cpu(times_user=times_user,
                           times_system=times_system,
                           times_idle=times_idle,
                            usage_percent=usage_percent,
                            host_ip=shared.current_hostname)
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
        memory_data = Memory(used=round(shared.bytes_to_gb(mem_used),2), 
                                 active=shared.kb_to_gb(active_mem),
                                 inactive=shared.kb_to_gb(Inactive_mem),
                                usage_percent=round(usage_percent,2),
                                host_ip=shared.current_hostname)
        stdin, stdout, stderr = ssh_client.exec_command('df -h /')
        output = stdout.read().decode("utf-8")
        data_line = output.split('\n')[1]
        parts=data_line.split()
        disk_size=parts[1]
        disk_used=parts[2]
        disk_avil=parts[3]
        disk_percent=parts[4]
        shared.total_space=disk_size
        disk_data = Disk(used=round(float(disk_used[:-1]),2),
                             free=round(float(disk_avil[:-1]) ,2) ,
                            usage_percent=disk_percent[:1],
                            host_ip=shared.current_hostname)
        
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