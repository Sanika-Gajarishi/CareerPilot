from app.auth.jwt_handler import create_access_token
from app.auth.password import (
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(
        self,
        full_name: str,
        email: str,
        password: str,
    ):

        existing = self.repository.get_by_email(email)

        if existing:
            raise ValueError("Email already exists")

        user = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
        )

        return self.repository.create(user)

    def login(
        self,
        email: str,
        password: str,
    ):

        user = self.repository.get_by_email(email)

        if not user:
            return None

        if not verify_password(
            password,
            user.password_hash,
        ):
            return None

        token = create_access_token(
            {"sub": user.email}
        )

        return token