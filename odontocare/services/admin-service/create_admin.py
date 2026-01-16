from app import create_app, db
from app.models import Usuario

# Crea la aplicación Flask y el contexto de la base de datos
app = create_app()

with app.app_context():
    """
    Se utiliza el contexto de la aplicación para poder acceder
    a la base de datos y a los modelos de Flask correctamente.
    """
    admin_username = "admin"

    admin = Usuario.query.filter_by(username=admin_username).first()

    if admin:
        print("El usuario admin ya existe")
    else:
        admin = Usuario(
            username=admin_username,
            rol="admin"
        )
        admin.set_password("admin123")

        db.session.add(admin)
        db.session.commit()

        print("Usuario admin creado correctamente")