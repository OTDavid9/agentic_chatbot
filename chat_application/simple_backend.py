from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# In-memory database
profiles: Dict[str, dict] = {}

# Profile schema
class Profile(BaseModel):
    username: str
    name: str
    email: str
    age: int

# --- Create Profile ---
@app.post("/profiles/", response_model=Profile)
def create_profile(profile: Profile):
    if profile.username in profiles:
        raise HTTPException(status_code=400, detail="Username already exists")
    profiles[profile.username] = profile.dict()
    return profile

# --- Get Profile ---
@app.get("/profiles/{username}", response_model=Profile)
def get_profile(username: str):
    if username not in profiles:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profiles[username]

# --- Update Profile ---
@app.put("/profiles/{username}", response_model=Profile)
def update_profile(username: str, updated_profile: Profile):
    if username not in profiles:
        raise HTTPException(status_code=404, detail="Profile not found")
    profiles[username] = updated_profile.dict()
    return updated_profile
