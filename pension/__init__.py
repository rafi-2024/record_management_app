from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging
from pension.config import Config
from flask_minify import minify

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view= 'users.login'
login_manager.login_message_category = "info"
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logger.log', encoding='utf-8', level=logging.ERROR)

def create_app(config_class=Config):
    app = Flask(__name__)
    minify(app=app, html=True, js=True, cssless=True)
    app.config.from_object(Config)
    db.init_app(app)
    
    from pension.users.routes import users
    from pension.diary.routes import diaries
    from pension.main.routes import main
    from pension.issue.routes import issues
    from pension.dashboard.routes import dash
    app.register_blueprint(users)
    app.register_blueprint(diaries)
    app.register_blueprint(main)
    app.register_blueprint(issues)
    app.register_blueprint(dash)
    with app.app_context():
        db.create_all()
    login_manager.init_app(app)
    return app
