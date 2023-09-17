# Backend API for an event management system

This API serves as the backend system for managing the arrangements and interactions of an event/party and its guestlist. 

#### This API  has 2 routes

## 1) Table route

#### This route is responsible for managing the tables of the event. It allows adding tables and checking the availability of seats at the party.

## 2) Guest route

#### The guests route deals with managing guests for the party. It allows adding guests to the guest list, checking them in, checking them out, and tracking their arrival time.

# How to run locally
First if using Github clone this repo by using following command
````

git clone https://github.com/noah-finestone/Event_Management_API

````

or if using the bundle binary file, cd into a folder where you want to clone the project, past the binary file and then run the command

```

git clone guestlist.bundle my_repo_clone

```

then cd into the root folder of the cloned repo using
```

cd Event_Management_API

``` 
or using 
```

cd my_repo_clone

```

Then install fastapi and all the project requirements using the following command
```

pip install -r requirements.txt

````

Then go to the root folder of this project and run the following command
````

uvicorn app.main:app --reload

````

Then you can use following link to use the  API

````

http://127.0.0.1:8000/docs 

````

## After running this API you need a database in postgres 
Create a database in MySQLWorkbench or using the terminal that corresponds to these fields - make sure to copy the exact answers for each field otherwise you will have to manually change the fields in the main.py and database.py file, so you can see the API work its magic

````
connection = pymysql.connect(host='localhost',
                            user='user',
                            password='password',
                            database='end_of_year_party_db',
                            cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()

````

# How to Run Tests

To run the unit tests:
## 1) Create a new schema/database in the connected sever called "end_of_year_party_db_test". 

## 2) cd to the root directory of the project

## 3) Execute the following command to run the test_table.py or test_guest.py file:
```

pytest -v -s tests/test_table.py

pytest -v -s tests/test_guest.py

```

# Future Improvements

1) Security Measures: Implement additional authentication mechanisms, such as OAuth, to protect the guests data and ensure secure access to the API endpoints.

2) CI/CD: Implements automated testing to validate the API's functionality whenever the code is pushed to github. 

3) Statistics routes: It would be useful to have routes to fetch guest and table statistics. This could include the total number of guests, the number of accompanying guests, the busiest tables, etc.

4) Waitlist Management: Instead of rejecting guets who arrive with a larger group than their table capacity, perhaps creating a waitlist where guests can join the waitlist and get notified if seats become available would be better.



