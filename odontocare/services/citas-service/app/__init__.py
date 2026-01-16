from flask import Flask, request
from app.middlewares.jwt_required import jwt_required
from .extensions import db
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.before_request
    def auth():
        if request.blueprint in ("health", "auth"):
            return
        jwt_required()

    db.init_app(app)

    from .modules.citas.routes import citas_bp
    from .modules.health.routes import health_bp

    app.register_blueprint(health_bp) 
    app.register_blueprint(citas_bp, url_prefix="/citas")

    return app
