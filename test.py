# test.py
# Create this file in your root folder

import requests

BASE_URL = "http://127.0.0.1:5000"

# Step 1 — Register
register = requests.post(
    f"{BASE_URL}/register",
    json={
        "name": "Ryan",
        "password": "mypassword123"
    }
)
print("REGISTER:", register.json())

# Step 2 — Login
login = requests.post(
    f"{BASE_URL}/login",
    json={
        "name": "Ryan",
        "password": "mypassword123"
    }
)
print("LOGIN:", login.json())

# Step 3 — Get token
token = login.json().get("token")

# Step 4 — Check balance
balance = requests.get(
    f"{BASE_URL}/balance",
    headers={
        "Authorization": f"Bearer {token}"
    }
)
print("BALANCE:", balance.json())

# Step 5 — Deposit
deposit = requests.post(
    f"{BASE_URL}/deposit",
    json={"amount": 500},
    headers={
        "Authorization": f"Bearer {token}"
    }
)
print("DEPOSIT:", deposit.json())

# Step 6 — Withdraw
withdraw = requests.post(
    f"{BASE_URL}/withdraw",
    json={"amount": 200},
    headers={
        "Authorization": f"Bearer {token}"
    }
)
print("WITHDRAW:", withdraw.json())