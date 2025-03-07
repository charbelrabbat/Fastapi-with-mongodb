from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient
from datetime import datetime
import os

# Use MongoDB Atlas connection from environment variable
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://rabbat:ChelseaPass@2022@1111558811@cluster0.3q4r6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

client = MongoClient(MONGO_URI)
db = client['userDB']
collection = db['users']

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    users = collection.find()
    return templates.TemplateResponse("index.html", {"request": request, "users": users})

@app.post("/add_user/")
async def add_user(name: str = Form(...), age: str = Form(...), city: str = Form(...)):
    if not name or not age or not city:
        raise HTTPException(status_code=400, detail="All fields are required")

    user_data = {
        "name": name,
        "age": age,
        "city": city,
        "date_added": datetime.now()
    }

    collection.insert_one(user_data)
    return RedirectResponse("/", status_code=303)

@app.post("/delete_user/")
async def delete_user(name: str = Form(...)):
    result = collection.delete_one({"name": name})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return RedirectResponse("/", status_code=303)
