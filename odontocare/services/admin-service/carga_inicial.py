import csv
import os
import sys
import time
import requests

print("CARGA INICIAL INICIO")

# =========================
# CONFIGURACIÓN POR ENTORNO
# =========================
ADMIN_BASE_URL = os.getenv("ADMIN_SERVICE_URL", "http://admin-service:5000")
CITAS_BASE_URL = os.getenv("CITAS_SERVICE_URL", "http://citas-service:5000")

ADMIN_SEED = {
    "username": "admin",
    "password": "admin123"
}

CSV_PATH = os.getenv("CSV_PATH", "/app/data/datos.csv")

# =========================
# UTILIDADES
# =========================
def fail(msg):
    print(f"{msg}")
    sys.exit(1)

def safe_post(url, **kwargs):
    try:
        response = requests.post(url, timeout=10, **kwargs)
        return response
    except requests.exceptions.RequestException as e:
        fail(f"Error llamando {url}: {e}")

def wait_for_service(url, retries=20, delay=2):
    print(f"Esperando servicio: {url}")
    for i in range(retries):
        try:
            r = requests.get(url, timeout=3)
            if r.status_code == 200:
                print("Servicio disponible")
                return
        except Exception:
            pass
        time.sleep(delay)
    fail(f"Servicio no disponible: {url}")

# =========================
# ESPERAR SERVICIOS
# =========================
wait_for_service(f"{ADMIN_BASE_URL}/health")
wait_for_service(f"{CITAS_BASE_URL}/health")

# =========================
# LOGIN ADMIN SEMILLA
# =========================
print("Login admin inicial...")
login = safe_post(f"{ADMIN_BASE_URL}/auth/login", json=ADMIN_SEED)

if login.status_code != 200:
    fail(f"No se pudo autenticar admin semilla: {login.text}")

token = login.json().get("token")
headers = {"Authorization": f"Bearer {token}"}
print("Login admin semilla exitoso")

# =========================
# LECTURA CSV
# =========================
if not os.path.exists(CSV_PATH):
    fail(f"Archivo CSV no encontrado: {CSV_PATH}")

usuarios, centros, doctores, pacientes = [], [], [], []

print(f"Leyendo CSV: {CSV_PATH}")

with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        tipo = row.get("tipoCarga")

        if tipo == "usuario":
            usuarios.append({
                "username": row["username"],
                "password": row["password"],
                "rol": row["tipo"]
            })

        elif tipo == "centro":
            centros.append({
                "nombre": row["nombre"],
                "direccion": row["direccion"]
            })

        elif tipo == "doctor":
            doctores.append({
                "nombre": row["nombre"],
                "especialidad": row["especialidad"]
            })

        elif tipo == "paciente":
            pacientes.append({
                "nombre": row["nombre"],
                "telefono": row["telefono"]
            })

print(f"CSV cargado: {len(usuarios)} usuarios, {len(centros)} centros, {len(doctores)} doctores, {len(pacientes)} pacientes")

# =========================
# CREAR ADMIN DESDE CSV
# =========================
if usuarios:
    admin_csv = usuarios[0]
    print("Creando admin desde CSV...")

    r = safe_post(
        f"{ADMIN_BASE_URL}/auth/register",
        json=admin_csv,
        headers=headers
    )

    if r.status_code in (200, 201):
        print("Admin CSV creado")
    else:
        print("Admin CSV ya existe o error controlado:", r.text)

    # Login con admin del CSV
    print("Login admin CSV...")
    r = safe_post(
        f"{ADMIN_BASE_URL}/auth/login",
        json={
            "username": admin_csv["username"],
            "password": admin_csv["password"]
        }
    )

    if r.status_code != 200:
        fail("No se pudo loguear con admin CSV")

    token = r.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Login admin CSV exitoso")

# =========================
# CARGA MASIVA
# =========================
print("Carga masiva de datos...")

bulk = safe_post(
    f"{ADMIN_BASE_URL}/admin/bulk-load",
    json={
        "centros": centros,
        "doctores": doctores,
        "pacientes": pacientes
    },
    headers=headers
)

if bulk.status_code not in (200, 201):
    print("Error en carga masiva")
    print("Status:", bulk.status_code)
    print("Body:", bulk.text)
else:
    print("Carga masiva completada")

# =========================
# CREACIÓN DE CITA
# =========================
print("Creando cita inicial...")

cita_payload = {
    "fecha": "2026-01-15 13:00",
    "motivo": "Consulta inicial",
    "id_paciente": 1,
    "id_doctor": 1,
    "id_centro": 1
}

cita = safe_post(
    f"{CITAS_BASE_URL}/citas",
    json=cita_payload,
    headers=headers
)

if cita.status_code not in (200, 201):
    print("Error creando cita")
    print("Status:", cita.status_code)
    print("Body:", cita.text)
else:
    print("Cita creada:", cita.json())

print("CARGA INICIAL COMPLETA")