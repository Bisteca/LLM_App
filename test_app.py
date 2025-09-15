import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Tutor Interactivo de Programaci" in response.data  

def test_tutor_valid_question(client):
    response = client.post('/tutor', json={"pregunta": "Qué es Data Engineering?"})
    assert response.status_code == 200
    data = response.get_json()
    assert "pregunta" in data
    assert "respuesta" in data
    assert data["pregunta"] == "Qué es Data Engineering?"

def test_tutor_empty_question(client):
    response = client.post('/tutor', json={"pregunta": ""})
    assert response.status_code == 200
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Por favor escribe una pregunta primero."

def test_tutor_missing_question(client):
    response = client.post('/tutor', json={})
    assert response.status_code == 200
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Por favor escribe una pregunta primero."
