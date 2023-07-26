from app import schemas
from .database import client, session

def test_add_table(client):
    res = client.post("/tables", json={"capacity": 10})
    
    # Assert response
    assert res.status_code == 201

def test_count_empty_seats(client):
    # Add a table with capacity 10 to the database
    client.post("/tables", json={"capacity": 10})
    
    # Make a request to the /seats_empty endpoint
    res = client.get("/seats_empty")
    assert res.status_code == 200
    data = res.json()
    # Assert response
    assert "seats_empty" in data
    assert isinstance(data["seats_empty"], int)
    # Since the database has one table with capacity 10 and no guests, "seats_empty" should be 10
    assert data["seats_empty"] == 10

