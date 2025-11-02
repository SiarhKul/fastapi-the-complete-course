from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi import status
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app
from ..routers.auth import get_current_user
from ..routers.todos import get_db
from fastapi.testclient import TestClient
import pytest
from ..models import  Todos

SQLALCHEMY_DATABASE_URL = 'sqlite:///testapp.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={'check_same_thread': False},
                       poolclass=StaticPool
                       )

TestingSessionLocal = SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db  = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username":'test_user', 'id':1, 'role':'admin'}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code",
        description="Need to learn",
        priority=5,
        compted=False,
        owner_id=1
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()
    db.close()




def test_read_all_autthnticated(test_todo):
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() ==[ {'priority': 5, 'id': 1, 'owner_id': 1, 'title': 'Learn to code', 'description': 'Need to learn', 'compted': False}]
