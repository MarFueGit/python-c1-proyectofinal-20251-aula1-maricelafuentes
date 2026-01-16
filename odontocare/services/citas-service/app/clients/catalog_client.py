import requests
from flask import current_app

def doctor_existe(id_doctor, token):
    r = requests.get(
        f"{current_app.config['CATALOG_SERVICE_URL']}/admin/doctores/{id_doctor}",
        headers={"Authorization": f"Bearer {token}"}
    )
    return r.status_code == 200


def centro_existe(id_centro, token):
    r = requests.get(
        f"{current_app.config['CATALOG_SERVICE_URL']}/admin/centros/{id_centro}",
        headers={"Authorization": f"Bearer {token}"}
    )
    return r.status_code == 200
