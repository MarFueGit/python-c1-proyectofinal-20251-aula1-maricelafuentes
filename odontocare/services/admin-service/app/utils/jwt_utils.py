import jwt
from flask import current_app, request


def decode_token(token):
    """
    Decodifica un JWT usando la SECRET_KEY de la app.

    Retorna:
        dict: payload del token si es válido
        None: si el token es inválido o ha expirado
    """
    try:
        payload = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )
        return payload

    except jwt.ExpiredSignatureError:
        current_app.logger.warning("Token expirado")
        return None

    except jwt.InvalidTokenError:
        current_app.logger.warning("Token inválido")
        return None
    
def get_current_user():
    """
    Obtiene el usuario actual desde el header Authorization.

    Header esperado:
    Authorization: Bearer <token>

    Retorna:
        dict | None
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None

    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ")[1]

    return decode_token(token)