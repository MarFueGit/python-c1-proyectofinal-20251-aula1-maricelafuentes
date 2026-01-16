from ...extensions import db
from ...models import CentroMedico, Doctor, Paciente

# =========================
# CENTROS MÉDICOS
# =========================

def create_center(data):
    centro = CentroMedico(
        nombre=data["nombre"],
        direccion=data["direccion"]
    )
    db.session.add(centro)
    db.session.commit()
    return centro


def list_centers():
    return CentroMedico.query.all()


def get_center_by_id(center_id):
    return CentroMedico.query.get(center_id)


def update_center(centro, data):
    for key, value in data.items():
        setattr(centro, key, value)
    db.session.commit()
    return centro


def delete_center(centro):
    db.session.delete(centro)
    db.session.commit()


def center_exists(nombre):
    return CentroMedico.query.filter_by(nombre=nombre).first()

# =========================
# DOCTORES
# =========================

def create_doctor(data):
    doctor = Doctor(
        nombre=data["nombre"],
        especialidad=data["especialidad"]
    )
    db.session.add(doctor)
    db.session.commit()
    return doctor


def list_doctores():
    return Doctor.query.all()


def get_doctor_by_id(doctor_id):
    return Doctor.query.get(doctor_id)


def update_doctor(doctor, data):
    for key, value in data.items():
        setattr(doctor, key, value)
    db.session.commit()
    return doctor


def delete_doctor(doctor):
    db.session.delete(doctor)
    db.session.commit()

# =========================
# PACIENTES
# =========================

def create_patient(data):
    paciente = Paciente(
        nombre=data["nombre"],
        telefono=data["telefono"]
    )
    db.session.add(paciente)
    db.session.commit()
    return paciente


def list_patients():
    # Solo pacientes activos
    return Paciente.query.filter_by(estado="ACTIVO").all()


def get_patient_by_id(paciente_id):
    return Paciente.query.get(paciente_id)


def update_patient(paciente, data):
    for key, value in data.items():
        setattr(paciente, key, value)
    db.session.commit()
    return paciente


def delete_patient(paciente):
    """
    Eliminación lógica del paciente.
    """
    paciente.estado = "INACTIVO"
    db.session.commit()

# =========================
# CARGA MASIVA
# =========================

def bulk_load(data):
    created = {
        "centros": 0,
        "doctores": 0,
        "pacientes": 0
    }

    for c in data.get("centros", []):
        db.session.add(CentroMedico(**c))
        created["centros"] += 1

    for d in data.get("doctores", []):
        db.session.add(Doctor(**d))
        created["doctores"] += 1

    for p in data.get("pacientes", []):
        db.session.add(Paciente(**p))
        created["pacientes"] += 1

    db.session.commit()

    return {
        "message": "Carga masiva exitosa",
        "created": created
    }