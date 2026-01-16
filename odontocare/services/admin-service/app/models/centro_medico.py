#Modelo CentroMedico

from app.extensions import db

class CentroMedico(db.Model):
    """
    Entidad que representa un centro médico.
    """
    __tablename__ = "centros_medicos"

    id_centro = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<CentroMedico {self.nombre}>"