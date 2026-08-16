import requests

BASE_URL = "http://localhost"


def create_user_with_api(user):
    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json={
            "name": user["name"],
            "surname": user["surname"],
            "email": user["email"],
            "password": user["password"],
            "role": "user",
        },
    )

    if response.status_code not in (200, 201):
        raise Exception(f"Не удалось создать пользователя: {response.status_code} {response.text}")

    return response.json()


def up_balance_with_api(cookie_header: str, amount: int):
    response = requests.post(
        f"{BASE_URL}/api/users/balance/add",
        json={"amount": amount},
        headers={"Cookie": cookie_header},
    )

    if response.status_code not in (200, 201):
        raise Exception(f"Не удалось пополнить баланс: {response.status_code} {response.text}")

    return response.json()