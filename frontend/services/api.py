import requests
from typing import Optional

BASE_URL = "http://127.0.0.1:8000/api/v1"


# ==========================================================
# Common Headers
# ==========================================================

def _headers(token: Optional[str] = None):
    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return headers


# ==========================================================
# Resume APIs
# ==========================================================

def upload_resume(uploaded_file, token: Optional[str] = None):
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type,
        )
    }

    response = requests.post(
        f"{BASE_URL}/resume/upload",
        files=files,
        headers=_headers(token),
        timeout=120,
    )

    response.raise_for_status()

    return response.json()


def get_resume_list(token: Optional[str] = None):

    response = requests.get(
        f"{BASE_URL}/resume/list",
        headers=_headers(token),
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_resume(
    resume_id: int,
    token: Optional[str] = None,
):

    response = requests.get(
        f"{BASE_URL}/resume/{resume_id}",
        headers=_headers(token),
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_latest_resume(token: Optional[str] = None):

    response = requests.get(
        f"{BASE_URL}/resume/latest",
        headers=_headers(token),
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def delete_resume(
    resume_id: int,
    token: Optional[str] = None,
):

    response = requests.delete(
        f"{BASE_URL}/resume/{resume_id}",
        headers=_headers(token),
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def download_resume(
    resume_id: int,
    token: Optional[str] = None,
):
    """
    Downloads original uploaded resume.
    """

    response = requests.get(
        f"{BASE_URL}/resume/{resume_id}/download",
        headers=_headers(token),
        timeout=120,
    )

    response.raise_for_status()

    return response.content


# ==========================================================
# Dashboard API
# ==========================================================

def get_dashboard(token: Optional[str] = None):

    response = requests.get(
        f"{BASE_URL}/dashboard",
        headers=_headers(token),
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Authentication APIs
# ==========================================================

def login(
    email: str,
    password: str,
):

    payload = {
        "email": email,
        "password": password,
    }

    response = requests.post(
        f"{BASE_URL}/auth/login",
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def register(
    full_name: str,
    email: str,
    password: str,
):

    payload = {
        "full_name": full_name,
        "email": email,
        "password": password,
    }

    response = requests.post(
        f"{BASE_URL}/auth/register",
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_current_user(token: str):

    response = requests.get(
        f"{BASE_URL}/users/me",
        headers=_headers(token),
        timeout=30,
    )

    response.raise_for_status()

    return response.json()