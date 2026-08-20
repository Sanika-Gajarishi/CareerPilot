import requests

BASE_URL = "http://127.0.0.1:8000/roadmap"


def get_headers(token: str):
    return {
        "Authorization": f"Bearer {token}"
    }


# ----------------------------
# Generate Roadmap
# ----------------------------

def generate_roadmap(data, token):

    response = requests.post(
        f"{BASE_URL}/generate",
        json=data,
        headers=get_headers(token),
        timeout=120,
    )

    response.raise_for_status()

    return response.json()


# ----------------------------
# Get All Roadmaps
# ----------------------------

def get_roadmaps(token):

    response = requests.get(
        BASE_URL,
        headers=get_headers(token),
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


# ----------------------------
# Get One Roadmap
# ----------------------------

def get_roadmap(roadmap_id, token):

    response = requests.get(
        f"{BASE_URL}/{roadmap_id}",
        headers=get_headers(token),
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def update_roadmap_progress(roadmap_id, progress, token):
    response = requests.patch(
        f"{BASE_URL}/{roadmap_id}/progress/{progress}",
        headers=get_headers(token),
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


# ----------------------------
# Delete Roadmap
# ----------------------------

def delete_roadmap(
    roadmap_id,
    token,
):

    response = requests.delete(
        f"{BASE_URL}/{roadmap_id}",
        headers=get_headers(token),
        timeout=30,
    )

    response.raise_for_status()

    return response.json()