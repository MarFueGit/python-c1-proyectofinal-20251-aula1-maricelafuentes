from marshmallow import Schema, fields, validate, EXCLUDE

class RegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    rol = fields.Str(
        required=True,
        validate=validate.OneOf(["admin", "medico", "secretaria", "paciente"])
    )

    class Meta:
        unknown = EXCLUDE

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE

# -------------------------------
# Instancias que usarás en routes
register_schema = RegisterSchema()
login_schema = LoginSchema()
