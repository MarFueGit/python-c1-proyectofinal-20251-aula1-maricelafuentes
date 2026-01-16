"""
Paquete de modelos de datos de la aplicación OdontoCare.

Este módulo centraliza la importación de todas las entidades ORM
definidas en la aplicación, facilitando su registro automático
en SQLAlchemy al iniciar la aplicación.
"""
from .cita_medica import CitaMedica

__all__ = ["CitaMedica"]