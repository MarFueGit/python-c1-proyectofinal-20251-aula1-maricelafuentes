"""
Módulo Citas Médicas de OdontoCare.

Define el blueprint `citas_bp` y expone los endpoints relacionados
con la gestión de citas médicas:

- Agendar citas
- Listar citas
- Cancelar citas
"""

from flask import Blueprint

citas_bp = Blueprint(
    "citas",
    __name__,
    url_prefix="/citas"
)

from .import routes