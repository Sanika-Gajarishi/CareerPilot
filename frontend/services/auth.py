import requests

from utils.session import login

BASE_URL = "http://127.0.0.1:8000/api/v1"


def login_user(email: str, password: str):
    """
    Login user using backend API.
    """

    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": email,
            "password": password,
        },
        timeout=30,
    )

    response.raise_for_status()

    token = response.json()["access_token"]

    user_response = requests.get(
        f"{BASE_URL}/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
        timeout=30,
    )

    user_response.raise_for_status()

    user = user_response.json()

    login(token, user)

    return user


def register_user(full_name, email, password):

    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "full_name": full_name,
            "email": email,
            "password": password,
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()