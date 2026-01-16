from flask import Flask
from .extensions import db
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from .modules.health.routes import health_bp
    from .modules.auth.routes import auth_bp
    from .modules.admin.routes import admin_bp

    app.register_blueprint(health_bp) 
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app