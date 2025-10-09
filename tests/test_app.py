import sys
import os
import pytest

# Asegura que se pueda importar app.py desde tests/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Prueba la ruta principal '/'"""
    res = client.get('/')
    assert res.status_code == 200
    assert b'html' in res.data  # Ajusta según tu plantilla

def test_listar_citas(client):
    """Prueba la ruta '/cita/listar'"""
    res = client.get('/cita/listar')
    assert res.status_code == 200
    assert b'Citas' in res.data or b'html' in res.data  # Ajusta según tu plantilla