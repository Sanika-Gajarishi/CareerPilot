import requests


BASE_URL = "http://127.0.0.1:8000/api/v1"


def optimize_resume(
    resume_id: int,
    token: str,
):

    response = requests.post(
        f"{BASE_URL}/optimizer/{resume_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        timeout=180,
    )

    # -------------------------------------------------
    # Successful Response
    # -------------------------------------------------

    if response.ok:

        return response.json()

    # -------------------------------------------------
    # Error Response
    # -------------------------------------------------

    try:

        error_data = response.json()

        detail = error_data.get(
            "detail",
            "Resume optimization failed.",
        )

    except ValueError:

        detail = (
            f"Resume optimization failed "
            f"(HTTP {response.status_code})."
        )

    raise Exception(detail)