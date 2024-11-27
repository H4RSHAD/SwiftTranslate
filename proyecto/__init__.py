from flask import Flask
from config import BaseConfig
from flask_migrate import Migrate
import os





app = Flask(__name__,static_folder = BaseConfig.STATIC_FOLDER, template_folder = BaseConfig.TEMPLATE_FOLDER)

app.config.from_object('config.DevConfig')  # traigo las configuraciones de DevConfig

from .models.User import db       # importo el db para poder migrar a la base de datos

migrate = Migrate(app, db)                  # realiza las migraciones

from .routers import home
from .routers.router_login import home_login
from .routers.router_registro import home_registro
from .routers.router_dashboard import home_dashboard



app.register_blueprint(home, url_prefix="/")
app.register_blueprint(home_login, url_prefix="/")
app.register_blueprint(home_registro, url_prefix="/")
app.register_blueprint(home_dashboard, url_prefix="/")