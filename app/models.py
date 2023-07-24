from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from pydantic import BaseModel
from sqlalchemy.orm import relationship

# Table model
class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    capacity = Column(Integer, nullable=False)

    guests = relationship("Guest", back_populates="table")

# Guest model
class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    name = Column(String(100), index=True, nullable=False)
    accompanying_guests = Column(Integer, nullable=False)
    table_id = Column(Integer, ForeignKey('tables.id'), nullable=False)
    time_arrived = Column(DateTime, nullable=True, default=None)

    table = relationship("Table", back_populates="guests")


