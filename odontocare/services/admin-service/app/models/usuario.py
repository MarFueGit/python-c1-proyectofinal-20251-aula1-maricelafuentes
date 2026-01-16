""""
Modelo Usuario.
Representa un usuario del sistema con credenciales de acceso y rol asignado.
"""

from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    """
    Entidad que representa un usuario del sistema.
    """
    __tablename__ = "usuarios"

    id_usuario = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(
        db.Enum("admin", "medico", "secretaria", "paciente", name="rol_usuario"),
        nullable=False
    )

    def set_password(self, password):
        """
        Genera y almacena el hash de la contraseña del usuario.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Verifica si la contraseña proporcionada coincide con el hash almacenado.
        """
        return check_password_hash(self.password, password)