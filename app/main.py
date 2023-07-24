from fastapi import FastAPI, HTTPException, status, Response
import pymysql.cursors
import time 
from . import models
from .database import engine
from .routers import guest, table


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Connect to the database
while True: 
    try:
        connection = pymysql.connect(host='localhost',
                            user='user',
                            password='password',
                            database='end_of_year_party_db',
                            cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

app.include_router(guest.router)
app.include_router(table.router)

        
