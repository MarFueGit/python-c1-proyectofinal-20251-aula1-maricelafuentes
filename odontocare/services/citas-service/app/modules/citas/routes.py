from flask import request, g, Blueprint, jsonify
from datetime import datetime
from marshmallow import ValidationError
from app.extensions import db

from . import citas_bp
from .schemas import (
    CitaCreateSchema,
    CitaUpdateSchema,
    CitaSchema,
    CitaFiltrosSchema
)
from .services import (
    agendar_cita,
    listar_citas,
    actualizar_cita,
    cancelar_cita,
    eliminar_cita
)


# =========================
# Schemas
# =========================
cita_create_schema = CitaCreateSchema()
cita_update_schema = CitaUpdateSchema()
cita_schema = CitaSchema()
citas_schema = CitaSchema(many=True)
cita_filtros_schema = CitaFiltrosSchema()

# =========================
# CREAR CITA
# =========================
@citas_bp.route("", methods=["POST"])
def crear_cita():
    try:
        data = cita_create_schema.load(request.get_json())

        cita = agendar_cita(
            data=data,
            usuario=g.current_user,
            token=g.jwt_token
        )

        return cita_schema.dump(cita), 201

    except ValidationError as err:
        return err.messages, 400
    except ValueError as err:
        return {"error": str(err)}, 400


# =========================
# LISTAR CITAS
# =========================
@citas_bp.route("", methods=["GET"])
def obtener_citas():
    try:
        filtros = cita_filtros_schema.load(request.args)

        citas = listar_citas(
            usuario=g.current_user,
            filtros=filtros
        )

        return citas_schema.dump(citas), 200

    except ValidationError as err:
        return err.messages, 400


# =========================
# ACTUALIZAR CITA
# =========================
@citas_bp.route("/<int:cita_id>", methods=["PUT"])
def editar_cita(cita_id):
    try:
        data = cita_update_schema.load(request.get_json())

        cita = actualizar_cita(cita_id, data)

        return cita_schema.dump(cita), 200

    except ValidationError as err:
        return err.messages, 400
    except ValueError as err:
        return {"error": str(err)}, 400


# =========================
# CANCELAR CITA
# =========================
@citas_bp.route("/<int:cita_id>/cancelar", methods=["PATCH"])
def cancelar(cita_id):
    try:
        cita = cancelar_cita(cita_id)

        return {
            "message": "Cita cancelada correctamente",
            "id_cita": cita.id_cita
        }, 200

    except ValueError as err:
        return {"error": str(err)}, 400


# =========================
# ELIMINAR CITA
# =========================
@citas_bp.route("/<int:cita_id>", methods=["DELETE"])
def eliminar(cita_id):
    try:
        eliminar_cita(cita_id)
        return {"message": "Cita eliminada correctamente"}, 200

    except ValueError as err:
        return {"error": str(err)}, 400