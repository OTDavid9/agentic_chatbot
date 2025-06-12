import requests

BASE_API_URL = "http://127.0.0.1:8000"


def make_purchase(item_name:str):
    return {"message": f"{item_name} was purchased!"}

def order_items(item_name:str, quantity:int):
    return {"message": f"{quantity} {item_name} were ordered!"}


def create_profile(username: str, name: str, email: str, age: int):
    response = requests.post(f"{BASE_API_URL}/profiles/", json={
        "username": username,
        "name": name,
        "email": email,
        "age": age
    })
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json().get("detail", "Unknown error")}

def get_profile(username: str):
    response = requests.get(f"{BASE_API_URL}/profiles/{username}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json().get("detail", "Profile not found")}

def update_profile(username: str, name: str, email: str, age: int):
    response = requests.put(f"{BASE_API_URL}/profiles/{username}", json={
        "username": username,
        "name": name,
        "email": email,
        "age": age
    })
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json().get("detail", "Unknown error")}
