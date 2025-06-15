from fastapi import FastAPI, Form, BackgroundTasks, UploadFile, File, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import  OAuth2PasswordBearer
from auth import hash_password, verify_password, create_access_token, get_current_user
from google_sheet import sheet, add_user, user_exists, get_user_by_email
from email_service import send_email
from dotenv import load_dotenv
from models import UserSignupRequest, UserLoginRequest
import os

load_dotenv()

app = FastAPI()

# CORS setup for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


@app.post("/api/signup")
async def signup(background_tasks: BackgroundTasks, signup_request: UserSignupRequest):
    full_name = signup_request.full_name
    email = signup_request.email
    password = signup_request.password

    if user_exists(email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(password)
    add_user(full_name, email, hashed_password)

    background_tasks.add_task(
        send_email,
        recipient_email=email,
        subject="Welcome!",
        body=f"Hello {full_name}, thank you for signing up!"
    )

    return {"message": "Signup successful. Please log in."}


@app.post("/api/login")
async def login(background_tasks: BackgroundTasks, login_request: UserLoginRequest):
    email = login_request.email
    password = login_request.password

    user = get_user_by_email(email)
    if not user or not verify_password(password, user['password']):
        return JSONResponse(status_code=401, content={"message": "Invalid email or password"})

    token = create_access_token(data={"sub": email})

    background_tasks.add_task(
        send_email,
        recipient_email=email,
        subject="Login Notification",
        body=f"Hello {user['Full Name']}, you have successfully logged in."
    )

    return {"access_token": token, "token_type": "bearer", "name": user['Full Name'].split()[0]}


@app.get("/api/chat")
async def chat(current_user: dict = Depends(get_current_user)):
    name = current_user['Full Name'].split()[0]
    return {"message": f"Welcome to the chat, {name}"}


@app.post("/api/upload")
async def upload(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    content = await file.read()
    print(f"User {current_user['email']} uploaded file of size {len(content)} bytes.")
    return {"filename": file.filename, "status": "uploaded successfully"}


@app.get("/api/logout")
async def logout():
    # Logout is frontend-driven with JWT
    return {"message": "You are logged out. Please clear your stored token on the frontend."}
