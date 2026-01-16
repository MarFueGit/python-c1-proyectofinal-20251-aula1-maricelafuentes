#Modelo Paciente

from app.extensions import db

class Paciente(db.Model):
    """
    Entidad que representa un paciente.
    """
    __tablename__ = "pacientes"

    id_paciente = db.Column(db.Integer, primary_key=True)

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id_usuario"),
        nullable=True
    )

    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)

    estado = db.Column(
        db.Enum("ACTIVO", "INACTIVO", name="estado_paciente"),
        nullable=False,
        default="ACTIVO"
    )

    # Relación ORM
    usuario = db.relationship("Usuario", backref="paciente", uselist=False)

    def __repr__(self):
        return f"<Paciente {self.nombre} ({self.estado})>"