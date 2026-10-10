from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User, UserRole
from app.repositories.user_repo import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.auth import RegisterRequest, LoginRequest


class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
        self.db = db

    def register(self, data: RegisterRequest) -> User:
        if self.repo.get_by_email(data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        user = User(
            name=data.name,
            email=data.email.lower(),
            password_hash=hash_password(data.password),
            role=UserRole.CUSTOMER,
        )
        self.repo.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def login(self, data: LoginRequest) -> str:
        user = self.repo.get_by_email(data.email.lower())
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return create_access_token(user.id)