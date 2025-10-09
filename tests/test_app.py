import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

def test_home_page():
    client = app.test_client()
    res = client.get('/')
    assert res.status_code == 200

def test_api_citas():
    client = app.test_client()
    res = client.get('/api/citas')
    assert res.status_code == 200
    assert 'citas' in res.json
