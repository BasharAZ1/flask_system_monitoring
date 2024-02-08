from flask import Flask
from flask_migrate import Migrate
from urls import configure_routes
from models import db
import os
import threading
from views import collect_system_info


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_fallback_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"

db.init_app(app)
migrate = Migrate(app, db)

configure_routes(app)

if __name__ == "__main__":
    # monitoring_thread = threading.Thread(target=collect_system_info)
    # monitoring_thread.start()

    app.run(debug=True)