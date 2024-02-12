from flask import Flask
from flask_migrate import Migrate
from urls import configure_routes
from models import db, Memory, Cpu, Disk,Active_processes
import os
import psutil 
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler



app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_fallback_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"

db.init_app(app)
migrate = Migrate(app, db)

configure_routes(app)

def collect_virtual_info():
    pass


def collect_system_info():
 with app.app_context():
    db.session.query(Active_processes).delete()
    memory_inf = psutil.virtual_memory()
    disk_usage = psutil.disk_usage("/")
    cpu_times = psutil.cpu_times()
    m = Memory(used=memory_inf.used,active=memory_inf.active,inactive= memory_inf.inactive,usage_percent=memory_inf.percent,host_ip='localhost')
    d = Disk(used=disk_usage.used / (1024**3),free=disk_usage.free / (1024**3),usage_percent=disk_usage.percent,host_ip='localhost')
    cpu_data = Cpu(times_user=cpu_times.user, times_system=cpu_times.system, times_idle=cpu_times.idle, usage_percent=psutil.cpu_percent(interval=1),host_ip='localhost')
    db.session.add(m)
    db.session.add(d)
    db.session.add(cpu_data)
        
    for proc in psutil.process_iter(attrs=['pid', 'name', 'status', 'create_time']):
        try:
            pid = proc.info['pid']
            name = proc.info['name']
            status = proc.info['status']
            start_date = datetime.fromtimestamp(proc.info['create_time']).strftime('%Y-%m-%d %H:%M:%S.%f')
            process = Active_processes(pid=pid, name=name, status=status, start_date=start_date, host_ip='localhost')
            db.session.add(process)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    db.session.commit()
    
    
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=collect_system_info, trigger="interval", seconds=1000)
scheduler.start()
if __name__ == "__main__":
    app.run(debug=True,use_reloader=False)