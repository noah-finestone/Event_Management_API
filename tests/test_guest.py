import datetime
import pytest
from app import models
from .database import client, session
from app import schemas

@pytest.fixture
def add_table(session):
    def _add_table(capacity: int):
        table = models.Table(capacity=capacity)
        session.add(table)
        session.commit()
        return table

    return _add_table

@pytest.fixture
def check_in_guest(client, add_table, session):
    # Add a table with a capacity of 10
    table = add_table(10)

    # Make a request to the guest_arrives endpoint to add the guest to the guest list
    data = {
        "table": table.id,  
        "accompanying_guests": 2
    }
    res = client.post("/guest_list/john", json=data)
    checked_in_guest = schemas.AddGuestResponse(**res.json())
    session.commit()

    return checked_in_guest
    

def test_add_to_guest_list(client, add_table):
    # Add a table with a capacity of 10
    table = add_table(10)

    # Make a request to the guest_arrives endpoint
    data = {
        "table": table.id, 
        "accompanying_guests": 2
    }
    res = client.post("/guest_list/john", json=data)
    checked_in_guest = schemas.AddGuestResponse(**res.json())

    # Assert the response
    assert res.status_code == 201
    assert checked_in_guest.name == "john"

def test_check_in(client, add_table, check_in_guest, session):
    # Use the check_in_guest fixture to get the previously added guest's information
    guest = check_in_guest

    # Make a request to the guests/{name} endpoint to check in the guest
    data_check_in = {
        "accompanying_guests": 2
    }
    res_check_in = client.put(f"/guests/{guest.name}", json=data_check_in)

    # Assert the response
    assert res_check_in.status_code == 200
    assert res_check_in.json()["name"] == "john"

    # Retrieve the guest from the database after the check-in
    guest = session.query(models.Guest).filter(models.Guest.name == "john").first()

    # Verify that the guest has a non-empty arrival time
    assert guest.time_arrived != None

def test_guest_leaves(client, check_in_guest, session, add_table):
    check_in_guest_response = check_in_guest

    # Make a request to the guest_leaves endpoint to delete the guest
    response = client.delete(f"/guests/{check_in_guest_response.name}")

    # Assert the response
    assert response.status_code == 204

def test_get_guest_list(client, session, add_table):
    # Add a guest to the database
    table = add_table(10)
    guest = models.Guest(name="john", table_id=table.id, accompanying_guests=2)
    session.add(guest)
    session.commit()

    # Make a request to the get_guest_list endpoint
    response = client.get("/guest_list")

    # Assert the response
    assert response.status_code == 200
    assert "guests" in response.json()
    assert len(response.json()["guests"]) == 1
    assert response.json()["guests"][0]["name"] == "john"

def test_get_arrived_guests(client, session, check_in_guest):
     # Use the check_in_guest fixture to get the previously added guest's information
    guest = check_in_guest

    # Retrieve the guest from the database after the check-in and set arrival time
    guest = session.query(models.Guest).filter(models.Guest.name == guest.name).first()
    guest.time_arrived = datetime.datetime.now()
    session.commit()

    guest = session.merge(guest)
    print(guest.name)

    # Make a request to the /guests endpoint to get the arrived guests
    response = client.get("/guests") 
    
    # Assert the response
    assert response.status_code == 200
    assert "guests" in response.json()
    assert guest.name == "john"

    # Extract the time_arrived from the response
    if response.json()["guests"]:
        time_arrived_str = response.json()["guests"][0]["time_arrived"]
        assert time_arrived_str is not None, "Guest arrival time should not be None"
    else:
        print("No guests found in the response.")
