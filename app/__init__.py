from flask import Flask
from .config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config=Config):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()
    
    from .auth import auth
    app.register_blueprint(auth)

    from .main import main
    app.register_blueprint(main)
    
    return app