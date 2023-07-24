from .. import schemas, models
from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from typing import List, Dict

router = APIRouter(tags=['Guests'])

@router.post("/guest_list/{name}", status_code=status.HTTP_201_CREATED, response_model=schemas.AddGuestResponse)
def guest_arrives(name: str, guest: schemas.AddGuest, db: Session = Depends(get_db)):
    # Check if the table exists
    table = db.query(models.Table).filter(models.Table.id == guest.table).first()

    if not table:
        raise HTTPException(status_code=404, detail=f"Table with id {guest.table} not found")

    # Check if a guest with the same table_id already exists
    existing_guest_with_table = db.query(models.Guest).filter(models.Guest.table_id == guest.table).first()
    if existing_guest_with_table:
        raise HTTPException(status_code=409, detail=f"A guest is already assigned to table with id {guest.table}")

    # Add the new guest to the guest list
    new_guest = models.Guest(name=name, table_id=guest.table, accompanying_guests=guest.accompanying_guests)
    db.add(new_guest)
    db.commit()
    db.refresh(new_guest)

    return {"name": new_guest.name}

@router.get("/guest_list", response_model=Dict[str, List[schemas.GuestDataResponse]])
def get_guest_list(db: Session = Depends(get_db)):
    guests = db.query(models.Guest).all()
    formatted_guests = [
        schemas.GuestDataResponse(
            name=guest.name,
            table=guest.table_id,
            accompanying_guests=guest.accompanying_guests
        )
        for guest in guests
    ]
    return {"guests": formatted_guests}

from datetime import datetime

@router.put("/guests/{name}", status_code=status.HTTP_200_OK, response_model=schemas.GuestArrivalResponse)
def guest_arrives(name: str, guest: schemas.GuestArrival, db: Session = Depends(get_db)):
    # Assuming guest names are unique in this API
    guest_model = db.query(models.Guest).filter(models.Guest.name == name).first()

    if not guest_model:
        raise HTTPException(status_code=404, detail=f"Guest: {name} not found")
    
    # Check if the guest is already checked in (has a time_arrived)
    if guest_model.time_arrived:
        raise HTTPException(status_code=400, detail=f"Guest: {name} is already checked in")

    table = db.query(models.Table).filter(models.Table.id == guest_model.table_id).first()
    if table:
        total_guests = guest.accompanying_guests + 1  # Adding 1 for the guest being added
        if total_guests <= table.capacity + guest_model.accompanying_guests:
            # Update the table capacity
            table.capacity -= total_guests
            db.commit()

            # Update the guest's accompanying guests count
            guest_model.accompanying_guests += guest.accompanying_guests
            
            guest_model.time_arrived = datetime.now()

            db.commit()

            # Return the response with updated time_arrived
            return {"name": guest_model.name, "time_arrived": guest_model.time_arrived}
        else:
            raise HTTPException(status_code=400, detail=f"Table does not have enough capacity for {total_guests} guests")

@router.delete("/guests/{name}", status_code=status.HTTP_204_NO_CONTENT)
def guest_leaves(name: str, db: Session = Depends(get_db)):
    # Assuming guest names are unique in this API
    guest = db.query(models.Guest).filter(models.Guest.name == name).first()

    if not guest:
        raise HTTPException(status_code=404, detail=f"Guest: {name} not found")
    
    if guest.table:
        table = db.query(models.Table).filter(models.Table.id == guest.table_id).first()
        # Safety check to ensure that the table exists before attempting to update its capacity
        if table:
            table.capacity += guest.accompanying_guests

    # Remove the guest from the database
    db.delete(guest)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/guests", response_model=Dict[str, List[schemas.ArrivedGuest]])
def get_arrived_guests(db: Session = Depends(get_db)):
    guests = db.query(models.Guest).filter(models.Guest.time_arrived <= datetime.now()).all()
    formatted_guests = [
        schemas.ArrivedGuest(
            name=guest.name,
            accompanying_guests=guest.accompanying_guests,
            time_arrived=guest.time_arrived.strftime("%Y-%m-%d %H:%M:%S")  # Convert datetime to string
        )
        for guest in guests
    ]
    return {"guests": formatted_guests}