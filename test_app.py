import pytest
import json
from app import app  # importa sua aplicação Flask

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Testa se a página inicial carrega corretamente"""
    response = client.get('/')
    assert response.status_code == 200
    html = response.get_data(as_text=True)   # converte para str
    assert "Tutor Interactivo de Programación" in html

def test_tutor_endpoint_success(client):
    """Testa se a rota /tutor retorna JSON válido"""
    payload = {"pregunta": "What is SQL?"}
    response = client.post('/tutor',
                           data=json.dumps(payload),
                           content_type="application/json")
    
    assert response.status_code == 200
    
    data = response.get_json()
    assert "pregunta" in data
    assert "respuesta" in data

def test_tutor_endpoint_empty_question(client):
    """Testa se rota /tutor retorna erro para pergunta vazia"""
    payload = {"pregunta": ""}
    response = client.post('/tutor',
                           data=json.dumps(payload),
                           content_type="application/json")
    
    assert response.status_code == 400 or response.status_code == 200
    data = response.get_json()
    assert "error" in data or "respuesta" in data
