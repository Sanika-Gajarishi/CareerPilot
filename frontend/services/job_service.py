import requests

BASE_URL = "http://localhost:8000/api/v1"


def analyze_job_match(
    resume_id: int,
    job_description: str,
    token: str,
):
    url = f"{BASE_URL}/job/match/{resume_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(
        url,
        json={
            "job_description": job_description
        },
        headers=headers,
    )

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()