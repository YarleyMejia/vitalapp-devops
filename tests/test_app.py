import sys
import os
import pytest
from datetime import date, timedelta

# ✅ Permitir importar app.py desde la carpeta raíz
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from services.cita_service import CitaService


# ---------------------------
# FIXTURES
# ---------------------------
@pytest.fixture
def client():
    """Crea un cliente de prueba para Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="module")
def service():
    """Instancia del servicio de citas con limpieza antes y después."""
    s = CitaService()
    s.citas.delete_many({})  # limpiar citas antes de las pruebas
    yield s
    s.citas.delete_many({})  # limpiar después de las pruebas


# ---------------------------
# TESTS
# ---------------------------

def test_home_page(client):
    """✅ Prueba la ruta principal '/'"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Salud Vital" in response.data


def test_agendar_cita(client, service):
    """ Prueba que se pueda agendar una cita nueva"""
    fecha = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")

    response = client.post(
        "/cita/agendar",
        data={
            "nombre": "Juan Pérez",
            "cedula": "12345678",
            "correo": "juan@example.com",
            "fecha": fecha,
            "hora": "09:00",
            "profesional": "Alejandro Gomez Bedoya",
            "especialidad": "Medicina General"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    citas = service.obtener_citas()
    assert any(c["cedula"] == "12345678" for c in citas)


def test_listar_citas(client):
    """ Prueba la lista de citas"""
    response = client.get("/cita/listar")
    assert response.status_code == 200
    assert b"Citas" in response.data or b"Nombre" in response.data


def test_reprogramar_cita(service):
    """ Prueba la reprogramación de una cita"""
    # Crear cita original
    service.agendar_cita(
        nombre="Carlos Ruiz",
        cedula="11223344",
        correo="carlos@example.com",
        fecha="2025-10-15",
        hora="08:00",
        profesional="Alejandro Gomez Bedoya",
        especialidad="Medicina General"
    )

    # Reprogramar
    nueva_fecha = "2025-10-20"
    nueva_hora = "10:00"
    nuevo_profesional = "Laura Martinez"
    nueva_especialidad = "Medicina Interna"

    service.reprogramar_cita(
        "11223344",
        nueva_fecha,
        nueva_hora,
        nuevo_profesional,
        nueva_especialidad
    )

    cita_actualizada = service.obtener_cita_por_cedula("11223344")
    assert cita_actualizada["fecha"] == nueva_fecha
    assert cita_actualizada["hora"] == nueva_hora
    assert cita_actualizada["profesional"] == nuevo_profesional
    assert cita_actualizada["especialidad"] == nueva_especialidad


def test_cancelar_cita(client, service):
    """ Prueba cancelar una cita existente"""
    # Crear cita de ejemplo
    service.agendar_cita(
        nombre="Maria Gomez",
        cedula="87654321",
        correo="maria@example.com",
        fecha=date.today().strftime("%Y-%m-%d"),
        hora="10:00",
        profesional="Laura Martinez",
        especialidad="Pediatría"
    )

    response = client.post(
        "/cita/cancelar",
        data={"cedula": "87654321"},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert not any(c["cedula"] == "87654321" for c in service.obtener_citas())
