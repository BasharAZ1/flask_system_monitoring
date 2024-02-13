from flask import Flask
from flask_migrate import Migrate
from urls import configure_routes
from models import db, Memory, Cpu, Disk, ActiveProcesses
import os
import psutil 
from datetime import datetime
import threading
import time
import shared
import paramiko


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_fallback_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"

db.init_app(app)
migrate = Migrate(app, db)

configure_routes(app)

DEFAULT_HOSTNAME = 'localhost'
hostname_changed_event = threading.Event()
shared.current_hostname = DEFAULT_HOSTNAME


def collect_remote_system_info(ssh_client):
    try:
        stdin, stdout, stderr = ssh_client.exec_command("ls")
        
        # Read the output
        output = stdout.read().decode("utf-8")
        
        # Print the output
        print("ls command output:")
        print(output)

        # # Execute commands to collect system info remotely
        # stdin, stdout, stderr = ssh_client.exec_command("free -m")  # Example command to get memory info
        # mem_info = stdout.read().decode("utf-8")
        # stdin, stdout, stderr = ssh_client.exec_command("df -h")  # Example command to get disk usage info
        # disk_info = stdout.read().decode("utf-8")
        # stdin, stdout, stderr = ssh_client.exec_command("top -bn1")  # Example command to get CPU usage info
        # cpu_info = stdout.read().decode("utf-8")

        # # Close SSH connection
        # # ssh_client.close()
        # testin, testout, testerr = ssh_client.exec_command("ls")
        # print(testin.read().decode("utf-8") + testout.read().decode("utf-8") + testerr.read().decode("utf-8"))
        # # Return the collected information
        # return mem_info, disk_info, cpu_info

    except Exception as e:
        print("Error:", e)
        return None


def collect_system_info(hostname=DEFAULT_HOSTNAME):
    with app.app_context():
        hostname = shared.current_hostname
        username = shared.current_username
        password = shared.current_password
        if hostname == DEFAULT_HOSTNAME:
            virtual_memory = psutil.virtual_memory()
            disk_usage = psutil.disk_usage("/")
            cpu_times = psutil.cpu_times()

            memory_data = Memory(used=virtual_memory.used, active=virtual_memory.active, inactive=virtual_memory.inactive,
                                usage_percent=virtual_memory.percent, host_ip=hostname)
            disk_data = Disk(used=disk_usage.used / (1024**3), free=disk_usage.free / (1024**3),
                            usage_percent=disk_usage.percent, host_ip=hostname)
            cpu_data = Cpu(times_user=cpu_times.user, times_system=cpu_times.system, times_idle=cpu_times.idle,
                            usage_percent=psutil.cpu_percent(interval=1), host_ip=hostname)

            db.session.query(ActiveProcesses).delete()
            for proc in psutil.process_iter(attrs=['pid', 'name', 'status', 'create_time']):
                try:
                    pid = proc.info['pid']
                    name = proc.info['name']
                    status = proc.info['status']
                    start_date = datetime.fromtimestamp(proc.info['create_time']).strftime('%Y-%m-%d %H:%M:%S.%f')
                    process = ActiveProcesses(pid=pid, name=name, status=status, start_date=start_date, host_ip=hostname)
                    db.session.add(process)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

        else:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(hostname, username=username, password=password)
                #memory_data, disk_data, cpu_data = collect_remote_system_info(ssh)
            
            except Exception as e:
                print("Error:", e)

            db.session.query(ActiveProcesses).delete()
            process = ActiveProcesses(id=0, measurement_time='s', pid=1234, name='process1', status='running', start_date='2024-02-13 12:00:00.000', host_ip=hostname)
            db.session.add(process)

        db.session.add(memory_data)
        db.session.add(disk_data)
        db.session.add(cpu_data)
        db.session.commit()


def background_thread():
    while True:
        collect_system_info()
        time.sleep(10)


def start_background_thread():
    thread = threading.Thread(target=background_thread)
    thread.daemon = True
    thread.start()
start_background_thread()


@app.route('/change_hostname/<new_hostname>', methods=['POST'])
def change_hostname(new_hostname):
    shared.current_hostname = new_hostname
    hostname_changed_event.set()  # Set the Event to notify the thread
    return f"Hostname changed to {new_hostname}"


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
