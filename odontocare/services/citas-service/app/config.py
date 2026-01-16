import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///db.sqlite3"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dates-secret")
    JWT_SECRET = os.getenv("JWT_SECRET", "admin-secret")
    CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL", "http://127.0.0.1:5001")
    PACIENTES_SERVICE_URL = os.getenv("PACIENTES_SERVICE_URL", "http://127.0.0.1:5001")