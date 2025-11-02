from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import status
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app
from ..routers.auth import get_current_user
from ..routers.todos import get_db
from fastapi.testclient import TestClient

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

def test_read_all_autthnticated():
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() ==[]
