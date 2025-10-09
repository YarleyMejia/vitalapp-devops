import sys
import os
import pytest
from flask import Flask

# Asegura que se pueda importar app.py desde tests/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # Importa la instancia de Flask

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Prueba la ruta principal '/'"""
    res = client.get('/')
    assert res.status_code == 200
    assert b'html' in res.data  # Ajusta según el contenido de tu plantilla

def test_listar_citas(client):
    """Prueba la ruta '/cita/listar'"""
    res = client.get('/cita/listar')
    assert res.status_code == 200
    assert b'Citas' in res.data or b'html' in res.data  # Ajusta según tu plantilla

# Puedes agregar más pruebas como estas:

# def test_agendar_cita(client):
#     res = client.post('/cita/agendar', data={
#         'nombre': 'Felipe',
#         'cedula': '123456789',
#         'correo': 'felipe@example.com',
#         'fecha': '2025-10-10',
#         'hora': '10:00'
#     }, follow_redirects=True)
#     assert res.status_code == 200
#     assert b'Cita agendada' in res.data

# def test_cancelar_cita(client):
#     res = client.post('/cita/cancelar', data={
#         'cedula': '123456789'
#     }, follow_redirects=True)
#     assert res.status_code == 200
#     assert b'Cita cancelada' in res.data