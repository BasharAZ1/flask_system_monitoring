from flask import Flask
from flask_migrate import Migrate
from urls import configure_routes
from models import db
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_fallback_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"

db.init_app(app)
migrate = Migrate(app, db)

configure_routes(app)

if __name__ == "__main__":
    app.run(debug=True)






from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import threading
import time
import psutil

app = Flask(__name__)


@app.route('/')
def homepage():
    # global stop_cpu_monitoring
    # global stop_memory_monitoring
    # global stop_hd_monitoring
    # stop_cpu_monitoring = True
    # stop_memory_monitoring = True
    # stop_hd_monitoring = True

    cpu_cores_num = psutil.cpu_count()
    ram_total = psutil.virtual_memory().total
    hd_total = psutil.disk_usage('/').total

    return render_template('homepage.html', cpu_cores_num=cpu_cores_num, ram_total=ram_total, hd_total=hd_total)


@app.route('/cpu')
def cpu_monitoring():
    # global stop_cpu_monitoring
    # stop_cpu_monitoring = False
    # while not stop_cpu_monitoring:
        cpu_percent = psutil.cpu_percent()
        cpu_usage = psutil.cpu_usage()
        cpu_times_usage = psutil.cpu_times_usage()
        cpu_data = monitor_db(col_a=cpu_percent, col_b=cpu_usage[0], col_c=cpu_usage[1], col_d=col_c = cpu_usage[
            2], col_e = col_c = cpu_usage[3], col_f = cpu_times_usage)
        database.session.add(cpu_data)
        database.session.commit()

        cpu_db = cpu_table.query.all()

        time.sleep(600)
    return render_template('cpu.html', cpu_db=cpu_db)


if __name__ == '__main__':
    init_db()
    # cpu_thread = threading.Thread(target=cpu_monitoring)
    # memory_thread = threading.Thread(target=memory_monitoring)
    # hd_thread = threading.Thread(target=hd_monitoring)
    #
    # cpu_thread.start()
    # memory_thread.start()
    # hd_thread.start()

    app.run()
