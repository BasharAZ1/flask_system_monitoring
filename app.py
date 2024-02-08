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











# if __name__ == '__main__':
#     # cpu_thread = threading.Thread(target=cpu_monitoring)
#     # memory_thread = threading.Thread(target=memory_monitoring)
#     # hd_thread = threading.Thread(target=hd_monitoring)
#     #
#     # cpu_thread.start()
#     # memory_thread.start()
#     # hd_thread.start()

#     app.run()
