"""
Módulo de utilidades de OdontoCare.

Este archivo sirve como punto de entrada del paquete `utils`.
Aquí se exponen de manera limpia y controlada las funciones
disponibles públicamente, evitando importar directamente
desde los submódulos internos.

Actualmente expone:

- decode_token: función para decodificar tokens JWT de la aplicación.
"""

from .jwt_utils import decode_token, get_current_user

__all__ = ["decode_token", "get_current_user"]