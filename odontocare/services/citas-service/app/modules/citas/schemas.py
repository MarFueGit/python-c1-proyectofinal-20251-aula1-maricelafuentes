from marshmallow import Schema, fields, validate

class CitaCreateSchema(Schema):
    fecha = fields.DateTime(
        required=True,
        format="%Y-%m-%d %H:%M",
        error_messages={
            "invalid": "Formato correcto: YYYY-MM-DD HH:MM"
        }
    )

    motivo = fields.String(
        required=True,
        validate=validate.Length(min=3)
    )

    id_paciente = fields.Integer(required=True)
    id_doctor = fields.Integer(required=True)
    id_centro = fields.Integer(required=True)

class CitaUpdateSchema(Schema):
    fecha = fields.DateTime(
        format="%Y-%m-%d %H:%M",
        error_messages={
            "invalid": "Formato correcto: YYYY-MM-DD HH:MM"
        }
    )

    motivo = fields.String(
        validate=validate.Length(min=3)
    )

    id_doctor = fields.Integer()
    id_centro = fields.Integer()

    estado = fields.String(
        validate=validate.OneOf(["PROGRAMADA", "ATENDIDA", "CANCELADA"])
    )

class CitaSchema(Schema):
    id_cita = fields.Integer(dump_only=True)

    fecha = fields.DateTime()
    motivo = fields.String()
    estado = fields.String()

    id_paciente = fields.Integer()
    id_doctor = fields.Integer()
    id_centro = fields.Integer()

    id_usuario_registra = fields.Integer()

class CitaFiltrosSchema(Schema):
    id_doctor = fields.Integer()
    id_paciente = fields.Integer()
    id_centro = fields.Integer()

    estado = fields.String(
        validate=validate.OneOf(["PROGRAMADA", "ATENDIDA", "CANCELADA"])
    )

    fecha = fields.String()  # YYYY-MM-DD