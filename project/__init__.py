#################
#### imports ####
#################

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext.bcrypt import Bcrypt
# from flask.ext.login import LoginManager
import os

################
#### config ####
################

app = Flask(__name__)
# bcrypt = Bcrypt(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)

from project.home.views import home_blueprint
from project.api.views import api_blueprint
# register our blueprints
app.register_blueprint(home_blueprint)
app.register_blueprint(api_blueprint, url_prefix='/json/api')