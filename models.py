from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()
from datetime import datetime


class Cpu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_time = db.Column(db.String(50), unique=True, nullable=False, default=lambda: datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    times_user = db.Column(db.Float, unique=False, nullable=False)
    times_system = db.Column(db.Float, unique=False, nullable=False)
    times_idle = db.Column(db.Float, unique=False, nullable=False)
    usage_percent = db.Column(db.Float, unique=False, nullable=False)

class Memory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_time = db.Column(db.String(50), unique=True, nullable=False, default=lambda: datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    used = db.Column(db.Integer, unique=False, nullable=False)
    active = db.Column(db.Integer, unique=False, nullable=False)
    inactive = db.Column(db.Integer, unique=False, nullable=False)
    usage_percent = db.Column(db.Float, unique=False, nullable=False)

class Disk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_time = db.Column(db.String(50), unique=True, nullable=False, default=lambda: datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    used = db.Column(db.Integer, unique=False, nullable=False)
    free = db.Column(db.Integer, unique=False, nullable=False)
    usage_percent = db.Column(db.Float, unique=False, nullable=False)
    
    
class Active_processes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_time = db.Column(db.String(50), unique=True, nullable=False, default=lambda: datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    pid = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(50), unique=False, nullable=False)
    start_date = db.Column(db.String(50), unique=False, nullable=False)