from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

def get_local_time():
    local_timezone = datetime.now().astimezone().tzinfo
    local_now = datetime.now().astimezone(local_timezone)
    return local_now.strftime('%Y-%m-%d %H:%M:%S.%f')

class Cpu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_time = db.Column(db.String(50), unique=False, nullable=False, default=get_local_time)
    times_user = db.Column(db.Float, unique=False, nullable=False)
    times_system = db.Column(db.Float, unique=False, nullable=False)
    times_idle = db.Column(db.Float, unique=False, nullable=False)
    usage_percent = db.Column(db.Float, unique=False, nullable=False)
    host_ip = db.Column(db.String, unique=False, nullable=False)
    total_cores=db.Column(db.String(255), unique=False, default="")


class Memory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_time = db.Column(db.String(50), unique=False, nullable=False, default=get_local_time)
    used = db.Column(db.Integer, unique=False, nullable=False)
    active = db.Column(db.Integer, unique=False, nullable=False)
    inactive = db.Column(db.Integer, unique=False, nullable=False)
    usage_percent = db.Column(db.Float, unique=False, nullable=False)
    host_ip = db.Column(db.String, unique=False, nullable=False)
    total_mem=db.Column(db.String(255), unique=False, default="")


class Disk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_time = db.Column(db.String(50), unique=False, nullable=False, default=get_local_time)
    used = db.Column(db.Integer, unique=False, nullable=False)
    free = db.Column(db.Integer, unique=False, nullable=False)
    usage_percent = db.Column(db.Float, unique=False, nullable=False)
    host_ip = db.Column(db.String, unique=False, nullable=False)
    total_space=db.Column(db.String(255), unique=False, default="")
    
    
class ActiveProcesses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_time = db.Column(db.String(50), unique=False, nullable=False, default=get_local_time)
    pid = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100),unique=False,nullable=False)
    status = db.Column(db.String(50), unique=False, nullable=False)
    start_date = db.Column(db.String(50), unique=False, nullable=False)
    host_ip = db.Column(db.String, unique=False, nullable=False)
