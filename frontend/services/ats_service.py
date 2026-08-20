import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"


def analyze_resume(resume_id: int, token=None):

    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.post(
        f"{BASE_URL}/ats/analyze/{resume_id}",
        headers=headers,
        timeout=180,
    )

    response.raise_for_status()

    return response.json()


def get_history(token=None):

    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(
        f"{BASE_URL}/ats/history",
        headers=headers,
        timeout=60,
    )

    response.raise_for_status()

    return response.json()


def get_analysis(
    analysis_id,
    token=None,
):

    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(
        f"{BASE_URL}/ats/{analysis_id}",
        headers=headers,
        timeout=60,
    )

    response.raise_for_status()

    return response.json()