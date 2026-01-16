
import jwt
from flask import request, g, abort
from app.config import Config

def jwt_required():
    auth = request.headers.get("Authorization")

    if not auth or not auth.startswith("Bearer "):
        abort(401, "Token requerido")

    token = auth.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            Config.JWT_SECRET,
            algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        abort(401, "Token expirado")
    except jwt.InvalidTokenError:
        abort(401, "Token inválido")

    g.current_user = payload
    g.jwt_token = token
