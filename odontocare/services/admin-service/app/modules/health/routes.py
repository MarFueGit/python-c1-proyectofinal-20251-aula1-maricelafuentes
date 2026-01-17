"""
Health check blueprint.

Este módulo define un endpoint de salud para verificar
que el servicio Flask se encuentra activo y funcionando correctamente.
"""

from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint.

    Retorna el estado del servicio para comprobar que la aplicación
    está en funcionamiento.

    Returns:
        Response: Un JSON con el estado del servicio y un código HTTP 200.
    """
    return jsonify({
        "status": "ok",
        "service": "up"
    }), 200