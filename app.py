from flask import Flask
from flask_migrate import Migrate
from urls import configure_routes
from models import db, Memory, Cpu, Disk
import os
import psutil 
from apscheduler.schedulers.background import BackgroundScheduler



app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_fallback_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"

db.init_app(app)
migrate = Migrate(app, db)

configure_routes(app)



def collect_system_info():
 with app.app_context():
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
    
    
    
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=collect_system_info, trigger="interval", seconds=60)
scheduler.start()
if __name__ == "__main__":
    app.run(debug=True,use_reloader=False)