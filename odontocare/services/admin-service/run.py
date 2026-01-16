"""
Punto de entrada del microservicio de Usuarios.

Responsabilidades:
- Crear la aplicación Flask
- Levantar el servidor HTTP del servicio
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )