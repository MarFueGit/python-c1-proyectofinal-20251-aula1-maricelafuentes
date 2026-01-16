"""
Decoradores de seguridad para la autenticación y autorización.

Define decoradores reutilizables para proteger rutas mediante JWT
y control de roles de usuario.
"""

from functools import wraps
from typing import Callable

from flask import request, g, jsonify

from ...utils import decode_token
from ...models.usuario import Usuario


def jwt_required(fn: Callable) -> Callable:
    """
    Decorador que protege una ruta validando un token JWT.

    - Verifica el header Authorization
    - Decodifica el token
    - Valida que el usuario exista
    - Guarda el usuario autenticado en g.current_user
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "error": "Autenticación requerida",
                "detalle": "Header Authorization no encontrado"
            }), 401

        if not auth_header.startswith("Bearer "):
            return jsonify({
                "error": "Formato de token inválido",
                "detalle": "Debe usar Bearer <token>"
            }), 401

        # Extrae el token del header
        token = auth_header.split(" ")[1]
        payload = decode_token(token)

        if payload is None:
            return jsonify({
                "error": "Token inválido",
                "detalle": "Token expirado o corrupto"
            }), 401

        user_id = payload.get("user_id")
        if not user_id:
            return jsonify({
                "error": "Token inválido",
                "detalle": "user_id no presente en el token"
            }), 401

        user = Usuario.query.get(user_id)
        if not user:
            return jsonify({
                "error": "Usuario no encontrado",
                "detalle": "El usuario asociado al token no existe"
            }), 401

        # Usuario autenticado disponible globalmente
        g.current_user = user
        g.current_payload = payload

        return fn(*args, **kwargs)

    return wrapper


def admin_required(fn: Callable) -> Callable:
    """
    Decorador que restringe el acceso solo a usuarios con rol ADMIN.
    """
    @wraps(fn)
    @jwt_required
    def wrapper(*args, **kwargs):
        if g.current_user.rol != "admin":
            return jsonify({
                "error": "Acceso denegado",
                "rol_actual": g.current_user.rol,
                "rol_requerido": "admin"
            }), 403

        return fn(*args, **kwargs)

    return wrapper


def roles_required(*roles: str) -> Callable:
    """
    Decorador flexible que permite restringir el acceso
    a múltiples roles permitidos.

    Ejemplo:
    @roles_required("admin", "secretaria")
    """
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        @jwt_required
        def wrapper(*args, **kwargs):
            user_role = g.current_user.rol

            if user_role not in roles:
                return jsonify({
                    "error": "Acceso no autorizado",
                    "rol_actual": user_role,
                    "roles_permitidos": list(roles)
                }), 403

            return fn(*args, **kwargs)

        return wrapper
    return decorator