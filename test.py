# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.models import Guest, Table

# # Assuming you have created the engine and Base as you did before
# engine = create_engine('sqlite:///mydatabase.db')
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Create some tables and guests
# def create_sample_data():
#     db = SessionLocal()
    
#     # Create tables
#     table1 = Table(name="Table 1", capacity=4)
#     table2 = Table(name="Table 2", capacity=6)

#     db.add_all([table1, table2])
#     db.commit()

#     # Create guests and associate them with tables
#     guest1 = Guest(name="Alice", accompanying_guests=2, table_id=table1.id)
#     guest2 = Guest(name="Bob", accompanying_guests=1, table_id=table1.id)
#     guest3 = Guest(name="Charlie", accompanying_guests=3, table_id=table2.id)

#     db.add_all([guest1, guest2, guest3])
#     db.commit()

#     db.close()

# # Query tables and their associated guests
# def query_tables_and_guests():
#     db = SessionLocal()

#     # Query all tables
#     tables = db.query(Table).all()

#     # Print table information and their guests
#     for table in tables:
#         print(f"Table: {table.name}, Capacity: {table.capacity}")
#         for guest in table.guests:
#             print(f"Guest: {guest.name}, Accompanying Guests: {guest.accompanying_guests}")

#     db.close()

# # Create the sample data and query tables with their associated guests
# create_sample_data()
# query_tables_and_guests()
