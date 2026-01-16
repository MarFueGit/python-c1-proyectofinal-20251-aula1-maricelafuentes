# odontocare/app/modules/auth/services.py

from werkzeug.security import generate_password_hash, check_password_hash
from ...extensions import db
from ...models.usuario import Usuario
import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app

def register_user(username, password, rol):
    existing = Usuario.query.filter_by(username=username).first()
    if existing:
        raise ValueError("El usuario ya existe")

    # Crear el usuario y encriptar la contraseña
    hashed = generate_password_hash(password)
    user = Usuario(username=username, rol=rol, password=hashed)

    db.session.add(user)
    db.session.commit()
    return user

def authenticate_user(username, password):
    user = Usuario.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        raise ValueError("Credenciales inválidas")

    payload = {
        "user_id": user.id_usuario,
        "rol": user.rol,
        "exp": datetime.now(timezone.utc) + timedelta(hours=8)
    }

    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    return token
