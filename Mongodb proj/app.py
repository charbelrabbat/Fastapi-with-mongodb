from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient
from datetime import datetime

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['userDB']
collection = db['users']

# FastAPI app and templates setup
app = FastAPI()

# Mount the static directory for CSS, images, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Fetch users from MongoDB
    users = collection.find()
    return templates.TemplateResponse("index.html", {"request": request, "users": users})

@app.post("/add_user/")
async def add_user(name: str = Form(...), age: str = Form(...), city: str = Form(...)):
    if not name or not age or not city:
        raise HTTPException(status_code=400, detail="All fields are required")

    # Add user data to MongoDB with current date
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
    # Delete the user from MongoDB
    result = collection.delete_one({"name": name})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return RedirectResponse("/", status_code=303)
