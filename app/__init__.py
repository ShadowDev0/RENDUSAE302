#!/bin/env python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    
    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.users import users_bp
    app.register_blueprint(users_bp) 

    from app.login import login_bp
    app.register_blueprint(login_bp)

    from app.machines import machines_bp
    app.register_blueprint(machines_bp)

    from app.logs import logs_bp
    app.register_blueprint(logs_bp)

    return app