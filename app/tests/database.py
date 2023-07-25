from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.database import get_db, Base

DATABASE_URL = "mysql+pymysql://user:password@localhost/end_of_year_party_db_test"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def session():
    # clears database, put here so we can see the state of our databse before running new tests 
    Base.metadata.drop_all(bind=engine)
    # run our code before we return our test 
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)



    
    
 