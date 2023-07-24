from sqlalchemy import func
from .. import schemas, models
from fastapi import FastAPI, Depends, status, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(tags=['Tables'])

@router.post("/tables", status_code=status.HTTP_201_CREATED, response_model=schemas.TableResponse)
def add_table(post: schemas.TableCreate, db: Session = Depends(get_db)):
    table = models.Table(capacity=post.capacity)
    db.add(table)
    db.commit()
    db.refresh(table)
    return schemas.TableResponse(id=table.id, capacity=table.capacity)

@router.get("/seats_empty", response_model=schemas.EmptySeatsResponse)
def count_empty_seats(db: Session = Depends(get_db)):
    # Get the total capacity of all guest tables
    empty_seats = db.query(func.sum(models.Table.capacity)).scalar() or 0

    return schemas.EmptySeatsResponse(seats_empty=empty_seats)