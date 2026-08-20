from services.api import (
    delete_resume,
    download_resume,
    get_resume,
    get_resume_list,
    upload_resume,
)


def _token():
    from utils.session import get_token

    return get_token()


def upload_resume_to_backend(uploaded_file):
    return upload_resume(uploaded_file, _token())


def fetch_resume_history():
    return get_resume_list(_token())


def fetch_resume_details(resume_id):
    return get_resume(resume_id, _token())


def remove_resume(resume_id):
    return delete_resume(resume_id, _token())


def get_resume_file(resume_id):
    return download_resume(resume_id, _token())
import requests

BASE_URL = "http://127.0.0.1:8000/api/v1/roadmap"


def generate_roadmap(data, token):

    response = requests.post(
        f"{BASE_URL}/generate",
        json=data,
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    response.raise_for_status()

    return response.json()


def get_all_roadmaps(token):

    response = requests.get(
        BASE_URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    response.raise_for_status()

    return response.json()


def get_roadmap(roadmap_id, token):

    response = requests.get(
        f"{BASE_URL}/roadmap/{roadmap_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    response.raise_for_status()

    return response.json()


def delete_roadmap(roadmap_id, token):

    response = requests.delete(
        f"{BASE_URL}/{roadmap_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    response.raise_for_status()

    return response.json()