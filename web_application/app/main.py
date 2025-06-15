import bcrypt
from fastapi import BackgroundTasks, FastAPI, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from typing import Optional
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from fastapi import FastAPI, Request, Form, Cookie
from fastapi import status
from passlib.context import CryptContext
import re
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket

load_dotenv()

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
SMTP_EMAIL = os.getenv('SMTP_EMAIL')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')


# Google Sheets Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret_goggle_sheet.json', scope)
client = gspread.authorize(creds)
sheet = client.open("UserDatabase").sheet1  # Name of your Google Sheet

# Test if the service account can list the sheets
try:
    sheet = client.open("UserDatabase").sheet1
    print("✅ Successfully connected to Google Sheet!")
except Exception as e:
    print("❌ Failed to connect to Google Sheet:", e)


# FastAPI Setup
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key='your-secret-key')


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Helper Functions
# Add this to your setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_current_user(request: Request) -> Optional[str]:
    return request.session.get("user")

def add_user(full_name: str, email: str, password: str):
    sheet.append_row([full_name, email, password])

def validate_user(email: str, password: str) -> bool:
    records = sheet.get_all_records()
    for record in records:
        if record['email'] == email and record['password'] == password:
            return True
    return False

def username_exists(email: str) -> bool:
    records = sheet.get_all_records()
    for record in records:
        if record['email'] == email:
            return True
    return False


def send_email(recipient_email, subject, body):
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = os.getenv('SMTP_EMAIL')
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Try both ports with timeout
        try:
            # Attempt TLS on port 587 first
            with smtplib.SMTP(os.getenv('SMTP_SERVER'), 587, timeout=10) as server:
                server.ehlo()
                server.starttls()
                server.login(os.getenv('SMTP_EMAIL'), os.getenv('SMTP_PASSWORD'))
                server.send_message(msg)
                print(f"Yes, on Port 587")
        except:
            # Fallback to SSL on port 465
            with smtplib.SMTP_SSL(os.getenv('SMTP_SERVER'), 465, timeout=10) as server:
                server.login(os.getenv('SMTP_EMAIL'), os.getenv('SMTP_PASSWORD'))
                server.send_message(msg)
                print(f"Yes, on Port 465")

        
        print(f"✅ Email sent to {recipient_email}")
        return True
        
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error sending to {recipient_email}: {str(e)}")
    except socket.timeout:
        print(f"❌ Connection timeout when sending to {recipient_email}")
    except Exception as e:
        print(f"❌ General error sending to {recipient_email}: {str(e)}")
    
    return False

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/signup", response_class=HTMLResponse)
async def post_signup(background_tasks: BackgroundTasks, request: Request, full_name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    users = sheet.get_all_records()
    for user in users:
        if user['email'] == email:
            raise HTTPException(status_code=400, detail="Email already registered")
            return templates.TemplateResponse("signup.html", {"request": request, "error": "Email already registered"})
            
                

    hashed_password = hash_password(password)
    add_user(full_name, email, hashed_password)

    # Send signup email
    background_tasks.add_task(
        send_email,
        recipient_email=email,
        subject="Welcome!",
        body=f"Hello {full_name}, thank for signing up!"
    )


    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)



@app.post("/login", response_class=HTMLResponse)
async def post_login(background_tasks: BackgroundTasks, request: Request, email: str = Form(...), password: str = Form(...)):
    users = sheet.get_all_records()
    for user in users:
        if user['email'] == email and verify_password(password, user['password']):
            full_name = user['Full Name']
            first_name = full_name.split()[0]
            response = RedirectResponse(url=f"/chat?name={first_name}", status_code=status.HTTP_303_SEE_OTHER)
            response.set_cookie(key="user", value=email)

            # Send login email
            
            background_tasks.add_task(
                send_email,
                recipient_email=email,
                subject="Login Notification",
                body=f"Hello {full_name},\n\nYou have successfully logged in to your account."
            )                                  


            return response

    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid email or password"})






@app.get("/chat", response_class=HTMLResponse)
def chat(request: Request, user: str = Cookie(None)):
    if not user:
        return RedirectResponse(url="/login")

    # Retrieve all users from the sheet
    users = sheet.get_all_records()

    # Find the user by matching the email (which is stored in the cookie)
    user_record = next((u for u in users if u['email'] == user), None)

    # Extract the first name if user exists
    name = user_record['Full Name'].split()[0] if user_record else ""

    return templates.TemplateResponse("chat.html", {"request": request, "name": name})


@app.post("/login", response_class=HTMLResponse)
async def post_login(request: Request, email: str = Form(...), password: str = Form(...)):
    users = sheet.get_all_records()
    for user in users:
        if user['email'] == email:
            if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                full_name = user['Full Name']
                first_name = full_name.split()[0]
                response = RedirectResponse(url=f"/chat?name={first_name}", status_code=status.HTTP_303_SEE_OTHER)
                response.set_cookie(key="user", value=email)
                return response

            # Incorrect password
            return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid email or password."})

    # Email not found
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid email or password."})




@app.get("/chat", response_class=HTMLResponse)
def chat(request: Request, name: str = "", user: str = Cookie(None)):
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("chat.html", {"request": request, "name": name})

@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    
    content = await file.read()
    print(f"User {user} uploaded file of size {len(content)} bytes.")
    return {"filename": file.filename, "status": "uploaded successfully"}

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login")
