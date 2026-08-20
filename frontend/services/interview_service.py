import requests

from config import API_BASE_URL


def start_interview(
    token,
    target_role,
    company,
    difficulty,
    interview_type,
):
    url = f"{API_BASE_URL}/interview/start"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "target_role": target_role,
        "company": company,
        "difficulty": difficulty,
        "interview_type": interview_type,
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
    )

    response.raise_for_status()

    return response.json()


def get_interview(
    interview_id,
    token,
):
    url = f"{API_BASE_URL}/interview/{interview_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        url,
        headers=headers,
    )

    response.raise_for_status()

    return response.json()


def submit_answer(
    interview_id,
    question_number,
    answer,
    token,
):
    url = f"{API_BASE_URL}/interview/{interview_id}/answer"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "question_number": question_number,
        "answer": answer,
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
    )

    response.raise_for_status()

    return response.json()


def interview_history(token):

    url = f"{API_BASE_URL}/interview"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        url,
        headers=headers,
    )

    response.raise_for_status()

    return response.json()