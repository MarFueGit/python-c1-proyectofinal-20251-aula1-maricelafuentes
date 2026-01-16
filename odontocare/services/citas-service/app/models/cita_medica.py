from app.extensions import db

class CitaMedica(db.Model):
    __tablename__ = "citas_medicas"

    id_cita = db.Column(db.Integer, primary_key=True)

    fecha = db.Column(db.DateTime, nullable=False)
    motivo = db.Column(db.String(255), nullable=False)

    estado = db.Column(
        db.Enum("PROGRAMADA", "CANCELADA", "ATENDIDA", name="estado_cita"),
        nullable=False,
        default="PROGRAMADA"
    )
    id_paciente = db.Column(db.Integer, nullable=False)
    id_doctor = db.Column(db.Integer, nullable=False)
    id_centro = db.Column(db.Integer, nullable=False)
    id_usuario_registra = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Cita {self.id_cita} - {self.fecha}>"
