"""
Esquemas de validación para el módulo de administración.

Define los esquemas Marshmallow utilizados para validar y serializar
los datos de centros médicos, doctores, pacientes y cargas masivas.
"""

from marshmallow import Schema, fields, validate, EXCLUDE

class CentroMedicoSchema(Schema):
    """Esquema para validar y serializar centros médicos.
    """
    id_centro = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, validate=validate.Length(min=3))
    direccion = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE

class DoctorSchema(Schema):
    """Esquema para validar y serializar doctores.
    """
    id_doctor = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, validate=validate.Length(min=3))
    especialidad = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE

class PacienteSchema(Schema):
    id_paciente = fields.Int(dump_only=True)
    id_usuario = fields.Int(allow_none=True)

    nombre = fields.Str(required=True, validate=validate.Length(min=3))
    telefono = fields.Str(required=True)

    estado = fields.Str(dump_only=True)

    class Meta:
        unknown = EXCLUDE

class BulkLoadSchema(Schema):
    """Esquema para validar la carga masiva de datos.
    """
    centros = fields.List(fields.Nested(CentroMedicoSchema))
    doctores = fields.List(fields.Nested(DoctorSchema))
    pacientes = fields.List(fields.Nested(PacienteSchema))

    class Meta:
        unknown = EXCLUDE