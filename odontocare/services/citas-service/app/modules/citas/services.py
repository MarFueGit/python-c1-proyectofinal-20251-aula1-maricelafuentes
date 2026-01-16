from ...extensions import db
from ...models import CitaMedica
from ...clients.catalog_client import doctor_existe, centro_existe
from ...clients.pacientes_client import paciente_valido


def agendar_cita(data, usuario, token):

    # Si el usuario es paciente, forzamos su id
    if usuario["rol"] == "paciente":
        data["id_paciente"] = usuario["id_paciente"]

    if not doctor_existe(data["id_doctor"], token):
        raise ValueError("Doctor no existe")

    if not paciente_valido(data["id_paciente"], token):
        raise ValueError("Paciente inválido o inactivo")

    if not centro_existe(data["id_centro"], token):
        raise ValueError("Centro médico no existe")

    # Evitar doble cita
    existe = CitaMedica.query.filter_by(
        id_doctor=data["id_doctor"],
        fecha=data["fecha"]
    ).first()
    
    if existe:
        raise ValueError("El doctor ya tiene una cita en ese horario")

    cita = CitaMedica(
        fecha=data["fecha"],
        motivo=data["motivo"],
        id_paciente=data["id_paciente"],
        id_doctor=data["id_doctor"],
        id_centro=data["id_centro"],
        id_usuario_registra=usuario["user_id"]
    )

    db.session.add(cita)
    db.session.commit()

    return cita


def listar_citas(usuario, filtros):
    query = CitaMedica.query

    # ----------------------
    # DOCTOR → solo sus citas
    # ----------------------
    if usuario["rol"] == "doctor":
        query = query.filter(
            CitaMedica.id_doctor == usuario["id_doctor"]
        )

    # ----------------------
    # SECRETARIA → filtrar por fecha
    # ----------------------
    if usuario["rol"] == "secretaria":
        if "fecha" in filtros:
            query = query.filter(
                CitaMedica.fecha.like(filtros["fecha"] + "%")
            )

    # ----------------------
    # ADMIN → filtros libres
    # ----------------------
    if usuario["rol"] == "admin":
        if "doctor" in filtros:
            query = query.filter(
                CitaMedica.id_doctor == filtros["doctor"]
            )

        if "centro" in filtros:
            query = query.filter(
                CitaMedica.id_centro == filtros["centro"]
            )

        if "paciente" in filtros:
            query = query.filter(
                CitaMedica.id_paciente == filtros["paciente"]
            )

        if "estado" in filtros:
            query = query.filter(
                CitaMedica.estado == filtros["estado"]
            )

        if "fecha" in filtros:
            query = query.filter(
                CitaMedica.fecha.like(filtros["fecha"] + "%")
            )

    return query.all()

def cancelar_cita(cita_id):
    cita = CitaMedica.query.get(cita_id)

    if not cita:
        raise ValueError("La cita no existe")

    if cita.estado == "CANCELADA":
        raise ValueError("La cita ya está cancelada")

    cita.estado = "CANCELADA"
    db.session.commit()

    return cita

# =========================
# ACTUALIZAR CITA
# =========================
def actualizar_cita(cita_id, data):
    cita = CitaMedica.query.get(cita_id)

    if not cita:
        raise ValueError("Cita no encontrada")

    if cita.estado == "CANCELADA":
        raise ValueError("No se puede editar una cita cancelada")

    for campo, valor in data.items():
        setattr(cita, campo, valor)

    db.session.commit()
    return cita

# =========================
# ELIMINAR CITA
# =========================
def eliminar_cita(cita_id):
    cita = CitaMedica.query.get(cita_id)

    if not cita:
        raise ValueError("La cita no existe")

    db.session.delete(cita)
    db.session.commit()