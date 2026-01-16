from app import create_app
from app.extensions import db

print("Inicializando base de datos...")

app = create_app()

with app.app_context():
    db.create_all()
    print("Base de datos creada correctamente")
