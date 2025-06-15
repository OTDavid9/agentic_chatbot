import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret_goggle_sheet.json', scope)
client = gspread.authorize(creds)
sheet = client.open("UserDatabase").sheet1

def add_user(full_name: str, email: str, hashed_password: str):
    sheet.append_row([full_name, email, hashed_password])

def user_exists(email: str) -> bool:
    users = sheet.get_all_records()
    return any(user['email'] == email for user in users)

def get_user_by_email(email: str):
    users = sheet.get_all_records()
    for user in users:
        if user['email'] == email:
            return user
    return None
