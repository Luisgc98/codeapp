from flask import Flask
from .config import Config
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

def create_app(config=Config):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config)
    bootstrap.init_app(app)
    
    from .auth import auth
    app.register_blueprint(auth)
    
    return app