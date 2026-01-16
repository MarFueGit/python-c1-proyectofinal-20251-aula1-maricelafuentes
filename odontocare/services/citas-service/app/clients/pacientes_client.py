import requests
from flask import current_app

def paciente_valido(id_paciente, token):
    r = requests.get(
        f"{current_app.config['PACIENTES_SERVICE_URL']}/admin/pacientes/{id_paciente}",
        headers={"Authorization": f"Bearer {token}"}
    )
    print("R: ", r)
    if r.status_code != 200:
        return False

    return r.json()["estado"] == "ACTIVO"
