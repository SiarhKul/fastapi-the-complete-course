from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi import status
from sqlalchemy.pool import StaticPool

from .utils import client, TestingSessionLocal
from ..database import Base
from ..main import app
from ..routers.auth import get_current_user
from ..routers.todos import get_db
from fastapi.testclient import TestClient
import pytest
from ..models import  Todos




def test_read_all_authenticated(test_todo):
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() ==[ {'priority': 5, 'id': 1, 'owner_id': 1, 'title': 'Learn to code', 'description': 'Need to learn', 'compted': False}]

def test_read_one_authenticated(test_todo):
    response = client.get('/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() =={'priority': 5, 'id': 1, 'owner_id': 1, 'title': 'Learn to code', 'description': 'Need to learn', 'compted': False}

def test_read_one_authenticated_not_found(test_todo):
    response = client.get('/todo/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}


def test_create_todo(test_todo):
    request_data = {
        "title": "New Todo",
        "description": "New todo description",
        "priority": 5,
        "compted": False
    }

    response = client.post("/todo", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.compted == request_data.get('compted')
    assert model.owner_id == 1

def test_create_todo_invalid_data():
    request_data = {
        "title": "a",
        "description": "b",
        "priority": 0,
        "compted": False
    }
    response = client.post("/todo", json=request_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_update_todo(test_todo):
    request_data = {
        "title": "Updated title",
        "description": "Updated description",
        "priority": 1,
        "compted": True
    }
    response = client.put("/todo/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id ==1).first()
    assert model.title == 'Updated title'
    assert model.description == 'Updated description'
    assert model.priority == 1
    assert model.compted is True

def test_delete_todo(test_todo):
    response = client.delete("/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id ==1).first()
    assert model is None