from flask import Blueprint, request
from marshmallow import ValidationError
from ...extensions import db

from .schemas import (
    CentroMedicoSchema,
    DoctorSchema,
    PacienteSchema,
    BulkLoadSchema
)

from .services import (
    create_center,
    list_centers,
    get_center_by_id,
    update_center,
    delete_center,
    create_doctor,
    list_doctores,
    get_doctor_by_id,
    update_doctor,
    delete_doctor,
    create_patient,
    list_patients,
    get_patient_by_id,
    update_patient,
    delete_patient,
    bulk_load
)

from ..auth.decorators import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# Schemas
centro_schema = CentroMedicoSchema()
centros_schema = CentroMedicoSchema(many=True)

doctor_schema = DoctorSchema()
doctores_schema = DoctorSchema(many=True)

paciente_schema = PacienteSchema()
pacientes_schema = PacienteSchema(many=True)

bulk_schema = BulkLoadSchema()

# =========================
# CENTROS MÉDICOS
# =========================

@admin_bp.route("/centros", methods=["POST"])
@admin_required
def crear_centro_medico():
    try:
        data = centro_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    centro = create_center(data)
    return centro_schema.dump(centro), 201


@admin_bp.route("/centros", methods=["GET"])
@admin_required
def obtener_centros():
    centros = list_centers()
    return centros_schema.dump(centros), 200


@admin_bp.route("/centros/<int:centro_id>", methods=["GET"])
@admin_required
def obtener_centro(centro_id):
    centro = get_center_by_id(centro_id)
    if not centro:
        return {"error": "Centro médico no encontrado"}, 404
    return centro_schema.dump(centro), 200


@admin_bp.route("/centros/<int:centro_id>", methods=["PATCH"])
@admin_required
def actualizar_centro(centro_id):
    centro = get_center_by_id(centro_id)
    if not centro:
        return {"error": "Centro médico no encontrado"}, 404

    try:
        data = centro_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return err.messages, 400

    centro = update_center(centro, data)
    return centro_schema.dump(centro), 200


@admin_bp.route("/centros/<int:centro_id>", methods=["DELETE"])
@admin_required
def eliminar_centro(centro_id):
    centro = get_center_by_id(centro_id)
    if not centro:
        return {"error": "Centro médico no encontrado"}, 404

    delete_center(centro)
    return {"message": "Centro médico eliminado correctamente"}, 200

# =========================
# DOCTORES
# =========================

@admin_bp.route("/doctores", methods=["POST"])
@admin_required
def crear_doctor():
    try:
        data = doctor_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    doctor = create_doctor(data)
    return doctor_schema.dump(doctor), 201


@admin_bp.route("/doctores", methods=["GET"])
@admin_required
def obtener_doctores():
    doctores = list_doctores()
    return doctores_schema.dump(doctores), 200


@admin_bp.route("/doctores/<int:doctor_id>", methods=["GET"])
@admin_required
def obtener_doctor(doctor_id):
    doctor = get_doctor_by_id(doctor_id)
    if not doctor:
        return {"error": "Doctor no encontrado"}, 404
    return doctor_schema.dump(doctor), 200


@admin_bp.route("/doctores/<int:doctor_id>", methods=["PATCH"])
@admin_required
def actualizar_doctor(doctor_id):
    doctor = get_doctor_by_id(doctor_id)
    if not doctor:
        return {"error": "Doctor no encontrado"}, 404

    try:
        data = doctor_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return err.messages, 400

    doctor = update_doctor(doctor, data)
    return doctor_schema.dump(doctor), 200


@admin_bp.route("/doctores/<int:doctor_id>", methods=["DELETE"])
@admin_required
def eliminar_doctor(doctor_id):
    doctor = get_doctor_by_id(doctor_id)
    if not doctor:
        return {"error": "Doctor no encontrado"}, 404

    delete_doctor(doctor)
    return {"message": "Doctor eliminado correctamente"}, 200

# =========================
# PACIENTES
# =========================

@admin_bp.route("/pacientes", methods=["POST"])
@admin_required
def crear_paciente():
    try:
        data = paciente_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    paciente = create_patient(data)
    return paciente_schema.dump(paciente), 201


@admin_bp.route("/pacientes", methods=["GET"])
@admin_required
def obtener_pacientes():
    pacientes = list_patients()
    return pacientes_schema.dump(pacientes), 200


@admin_bp.route("/pacientes/<int:paciente_id>", methods=["GET"])
@admin_required
def obtener_paciente(paciente_id):
    paciente = get_patient_by_id(paciente_id)
    if not paciente:
        return {"error": "Paciente no encontrado"}, 404
    return paciente_schema.dump(paciente), 200


@admin_bp.route("/pacientes/<int:paciente_id>", methods=["PATCH"])
@admin_required
def actualizar_paciente(paciente_id):
    paciente = get_patient_by_id(paciente_id)
    if not paciente:
        return {"error": "Paciente no encontrado"}, 404

    try:
        data = paciente_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return err.messages, 400

    paciente = update_patient(paciente, data)
    return paciente_schema.dump(paciente), 200


@admin_bp.route("/pacientes/<int:paciente_id>", methods=["DELETE"])
@admin_required
def eliminar_paciente(paciente_id):
    paciente = get_patient_by_id(paciente_id)
    if not paciente:
        return {"error": "Paciente no encontrado"}, 404

    delete_patient(paciente)
    return {"message": "Paciente desactivado correctamente"}, 200


@admin_bp.route("/pacientes/<int:paciente_id>/activar", methods=["PATCH"])
@admin_required
def activar_paciente(paciente_id):
    """
    Activa a un paciente previamente desactivado.
    """
    paciente = get_patient_by_id(paciente_id)
    if not paciente:
        return {"error": "Paciente no encontrado"}, 404

    paciente.estado = "ACTIVO"
    db.session.commit()
    return {"message": f"Paciente {paciente_id} activado correctamente"}, 200

# =========================
# CARGA MASIVA
# =========================

@admin_bp.route("/bulk-load", methods=["POST"])
@admin_required
def carga_masiva():
    try:
        data = bulk_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    result = bulk_load(data)
    return result, 201