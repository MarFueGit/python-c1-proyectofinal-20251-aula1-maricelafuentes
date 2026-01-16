# odontocare/app/modules/auth/routes.py

from flask import request
from marshmallow import ValidationError

from . import auth_bp
from .schemas import RegisterSchema, LoginSchema
from .services import register_user, authenticate_user
from .decorators import admin_required  # 👈 importante

register_schema = RegisterSchema()
login_schema = LoginSchema()


@auth_bp.route("/register", methods=["POST"])
@admin_required
def register():
    """
    Registra un nuevo usuario.
    Solo accesible para administradores.
    """
    try:
        data = register_schema.load(request.get_json())
        user = register_user(
            data["username"],
            data["password"],
            data["rol"]
        )

        return {
            "message": "Usuario creado correctamente",
            "id": user.id_usuario,
            "username": user.username,
            "rol": user.rol
        }, 201

    except ValidationError as err:
        return {"errors": err.messages}, 400

    except ValueError as err:
        return {"error": str(err)}, 409


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Inicia sesión y devuelve un JWT.
    """
    try:
        data = login_schema.load(request.get_json())
        token = authenticate_user(
            data["username"],
            data["password"]
        )

        return {"token": token}, 200

    except ValidationError as err:
        return {"errors": err.messages}, 400

    except ValueError as err:
        return {"error": str(err)}, 401