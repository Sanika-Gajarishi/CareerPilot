import requests


BASE_URL = "http://127.0.0.1:8000/api/v1/job-tracker"


def _headers(token):
    return {"Authorization": f"Bearer {token}"}


def _json_dates(data):
    return {
        key: value.isoformat() if hasattr(value, "isoformat") else value
        for key, value in data.items()
    }


def get_applications(token):
    response = requests.get(
        BASE_URL,
        headers=_headers(token),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def create_application(data, token):
    response = requests.post(
        BASE_URL,
        json=_json_dates(data),
        headers=_headers(token),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def update_application(application_id, data, token):
    response = requests.put(
        f"{BASE_URL}/{application_id}",
        json=_json_dates(data),
        headers=_headers(token),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def delete_application(application_id, token):
    response = requests.delete(
        f"{BASE_URL}/{application_id}",
        headers=_headers(token),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
