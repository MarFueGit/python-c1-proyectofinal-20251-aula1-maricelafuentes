def test_login_sin_datos(client):
    """
    Prueba que el endpoint de login retorne un error 400
    cuando no se envían datos en el cuerpo de la petición.
    """
    response = client.post("/auth/login", json={})

    assert response.status_code == 400

def test_login_password_incorrecto(client):
    """
    Prueba que el endpoint de login retorne un error 401
    cuando se envía una contraseña incorrecta para un usuario.
    """

    response = client.post("/auth/login", json={
        "username": "fail@test.com",
        "password": "mal_password"
    })

    assert response.status_code == 401