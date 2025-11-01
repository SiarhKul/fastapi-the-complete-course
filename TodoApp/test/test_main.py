from fastapi.testclient import TestClient
from TodoApp.main import app
from fastapi import status

client = TestClient(app)


def test_return_health_check():
    reponse = client.get('/heathy')
    assert reponse.status_code == status.HTTP_200_OK
    assert reponse.json() == {'status': 'Heathy'}