"""
Script de inicialización de la base de datos.

Este módulo crea la aplicación Flask y genera todas las tablas
definidas en los modelos utilizando SQLAlchemy.
Debe ejecutarse una sola vez o cuando se necesite reinicializar
la base de datos.
"""

from app import create_app
from app.extensions import db

print("Inicializando base de datos...")

app = create_app()

with app.app_context():
    db.create_all()
    print("Base de datos creada correctamente")