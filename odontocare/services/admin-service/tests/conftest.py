import pytest
from app import create_app
from app.extensions import db

# Fixture que crea y configura la aplicación para las pruebas
@pytest.fixture
def app():
    # Crear la aplicación con configuración de prueba
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

# Fixture que crea un cliente de pruebas para hacer requests HTTP
@pytest.fixture
def client(app):
    return app.test_client()