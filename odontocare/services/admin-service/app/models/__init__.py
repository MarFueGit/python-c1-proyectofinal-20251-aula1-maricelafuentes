"""
Paquete de modelos de datos de la aplicación OdontoCare.

Este módulo centraliza la importación de todas las entidades ORM
definidas en la aplicación, facilitando su registro automático
en SQLAlchemy al iniciar la aplicación.
"""

from .usuario import Usuario  
from .paciente import Paciente 
from .doctor import Doctor
from .centro_medico import CentroMedico


__all__ = ["Usuario", "Paciente", "Doctor", "CentroMedico"]