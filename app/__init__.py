from flask import Flask
from .config import Config
from .routes.index import projects_router
from app.db import db


def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(projects_router)
    db.init_app(app)
        
    return app