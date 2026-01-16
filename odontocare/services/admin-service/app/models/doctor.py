#Modelo Doctor

from app.extensions import db

class Doctor(db.Model):
    """
    Entidad que representa un doctor.
    """
    __tablename__ = "doctores"

    id_doctor = db.Column(db.Integer, primary_key=True)

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id_usuario"),
        nullable=True
    )

    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)

    usuario = db.relationship("Usuario", backref="doctor", uselist=False)

    def __repr__(self):
        return f"<Doctor {self.nombre} - {self.especialidad}>"