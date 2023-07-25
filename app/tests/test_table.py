from app import schemas
from .database import client, session

def test_add_table(client):
    res = client.post("/tables", json={"capacity": 10})
    print(res.json)
    assert res.status_code == 201

def test_count_empty_seats(client):
    # Add a table with capacity 10 to the database
    client.post("/tables", json={"capacity": 10})
    
    # Make a request to the /seats_empty endpoint
    res = client.get("/seats_empty")
    assert res.status_code == 200
    data = res.json()
    # Check that the response contains the expected keys
    assert "seats_empty" in data
    # Check that the value of "seats_empty" is an integer
    assert isinstance(data["seats_empty"], int)
    # Since the database has one table with capacity 10 and no guests, "seats_empty" should be 10
    assert data["seats_empty"] == 10

