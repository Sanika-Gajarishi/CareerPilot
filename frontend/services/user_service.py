import requests


BASE_URL = "http://127.0.0.1:8000/api/v1"


def get_current_user(token: str):
	response = requests.get(
		f"{BASE_URL}/users/me",
		headers={"Authorization": f"Bearer {token}"},
		timeout=30,
	)
	response.raise_for_status()
	return response.json()


def update_current_user(token: str, data: dict):
	response = requests.put(
		f"{BASE_URL}/users/me",
		json=data,
		headers={"Authorization": f"Bearer {token}"},
		timeout=30,
	)
	response.raise_for_status()
	return response.json()


def delete_current_user(token: str):
	response = requests.delete(
		f"{BASE_URL}/users/me",
		headers={"Authorization": f"Bearer {token}"},
		timeout=30,
	)
	response.raise_for_status()
	return response.json()
