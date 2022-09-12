from flask import Flask,jsonify
import os
from src.auth import auth
from src.Tasks import tasks
from src.database import db
from flask_jwt_extended import JWTManager
def create_app(test_config=None):

    app=Flask(__name__,instance_relative_config=True)
    if test_config is None:
        app.config.from_mapping(
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI= os.environ.get("SQLALCHEMY_DB_URI"),
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY")
        )
    else:
        app.config.from_mapping(test_config)
        
    db.app=app
    db.init_app(app)
    JWTManager(app)
    app.register_blueprint(auth)
    app.register_blueprint(tasks)
        
    return app