from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# Initialize FastAPI app
app = FastAPI()

# In-memory database simulation
database = []

# Pydantic model for POST data
class Item(BaseModel):
    id: int
    name: str
    description: str

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/items", response_model=List[Item])
def get_items():
    return database

@app.post("/items", response_model=Item)
def create_item(item: Item):
    database.append(item)
    return item
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

VERIFY_TOKEN = "ssadadsadas"  # Replace with your verify token

@app.get("/webhook")
async def verify_webhook(hub_mode: str, hub_challenge: str, hub_verify_token: str):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Invalid token")

@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()
    print("Received webhook payload:", payload)
    return {"status": "received"}
