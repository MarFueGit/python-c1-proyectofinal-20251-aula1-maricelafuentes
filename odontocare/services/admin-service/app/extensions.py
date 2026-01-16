"""
Módulo de extensiones de la aplicación OdontoCare.

Define y expone las extensiones utilizadas por la aplicación Flask,
permitiendo su inicialización centralizada y su reutilización en
los distintos módulos del sistema.
"""   

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()