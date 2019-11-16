from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from .config import config_by_name


BASE_URL = 'https://true-chat.herokuapp.com'
db = SQLAlchemy()
cors = CORS(resources={r"/api/*": {"origins": "*"}})


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    cors.init_app(app)
    
    return app
