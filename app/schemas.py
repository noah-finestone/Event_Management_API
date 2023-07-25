from pydantic import BaseModel

# Defines the shape of the request body when you create a new table
class TableCreate(BaseModel):
    capacity: int

# Defines the shape of the response when a new table is created
class TableResponse(BaseModel):
    id: int
    capacity: int

# Defines the shape of the request body when a adding a guest to the guest list
class AddGuest(BaseModel):
    table: int
    accompanying_guests: int

# Defines the shape of the response when a adding a guest to the guest list
class AddGuestResponse(BaseModel):
    name: str

# Defines the shape of the response containing guest data
class GuestDataResponse(BaseModel):
    name: str
    table: int
    accompanying_guests: int

# Request body schema for guest arrival
class GuestArrival(BaseModel):
    accompanying_guests: int

# Response body schema for guest arrival
class GuestArrivalResponse(BaseModel):
    name: str

# Defines the shape of the response for guests who have arrived
class ArrivedGuest(BaseModel):
    name: str
    accompanying_guests: int
    time_arrived: str
    
  # Response body schema for empty seats  
class EmptySeatsResponse(BaseModel):
    seats_empty: int
