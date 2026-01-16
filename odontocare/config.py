"""
Módulo de configuración de la aplicación OdontoCare.

Este archivo define las clases de configuración utilizadas por la aplicación Flask,
permitiendo separar parámetros comunes y específicos según el entorno de ejecución
(desarrollo o producción).

La configuración incluye:
- Clave secreta para la aplicación
- Conexión a la base de datos SQLite
- Opciones de SQLAlchemy
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Clase base de configuración.

    Contiene los parámetros comunes a todos los entornos de ejecución
    de la aplicación Flask.
    """
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        BASE_DIR, "..", "instance", "app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Configuraciones específicas por entorno
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False   


class TestConfig(Config):
    """
    Configuración específica para pruebas unitarias.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"     