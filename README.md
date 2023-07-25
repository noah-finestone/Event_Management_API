# GetGround_Backend_Assignment

This API serves as the backend for managing the arrangements and interactions for the End-of-Year Party.

#### This API  has 2 routes

## 1) Table route

#### This route is responsible for managing the party tables. It allows adding tables and checking the availability of seats at the party.

## 2) Guest route

#### The guests route deals with managing guests for the party. It allows adding guests to the guest list, checking them in, checking them out, and tracking their arrival time.

# How to run locally
First clone this repo by using following command
````

git clone https://github.com/noah-finestone/GetGround_Backend_Assignment

````
then 
````

cd GetGround_Backend_Assignment

````

Then install fastapp using all flag like (or pip install -r requirements.txt)
```

pip install fastapi[all]

````

Then go this repo folder in your local computer run the following command
````
uvicorn app.main:app --reload

````

Then you can use following link to use the  API

````

http://127.0.0.1:8000/docs 

````

# How to Run Tests

To run the tests for the table and guest routes, follow these steps:
## 1) Change to the project directory

## 2) Execute the following command to run the test_table.py or test_guest.py file:
```

pytest -v -s app/tests/test_table.py

pytest -v -s app/tests/test_guest.py


```



