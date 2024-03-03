from flask import Flask
from flask_migrate import Migrate
from urls import configure_routes
from models import db
import os
import threading
import time
import shared 
import paramiko
from views import collect_local_info,collect_remote_system_info


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_fallback_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"

db.init_app(app)
migrate = Migrate(app, db)

configure_routes(app)

DEFAULT_HOSTNAME = 'localhost'
hostname_changed_event = threading.Event()
shared.current_hostname = DEFAULT_HOSTNAME


def collect_system_info(hostname=DEFAULT_HOSTNAME):
    with app.app_context():
        hostname = shared.current_hostname
        username = shared.current_username
        password = shared.current_password
        if hostname == DEFAULT_HOSTNAME:
            collect_local_info()
        else:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(hostname, username=username, password=password)
                collect_remote_system_info(ssh)
            except Exception as e:
                print("Error:", e)


def background_thread():
    while True:
        collect_system_info()
        time.sleep(60)


def start_background_thread():
    thread = threading.Thread(target=background_thread)
    thread.daemon = True
    thread.start()
start_background_thread()


@app.route('/change_hostname/<new_hostname>', methods=['POST'])
def change_hostname(new_hostname):
    shared.current_hostname = new_hostname
    hostname_changed_event.set()  
    return f"Hostname changed to {new_hostname}"


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
