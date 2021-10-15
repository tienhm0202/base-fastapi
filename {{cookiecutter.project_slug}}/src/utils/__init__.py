import logging
import secrets
import string
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.hash import bcrypt
from src.config import settings
from src.utils.logger import get_base_logger


def unique_id(length: int = 8, prefix: str = "Z"):
    alphabet = string.digits + string.ascii_letters
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return prefix + password


def get_db_id() -> str:
    return unique_id(16, "ID_")


def get_secret() -> str:
    return unique_id(32, "KEY_")


def get_activation_code() -> str:
    alphabet = string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(6))


def verify_password(plain_password, hashed_password) -> str:
    return bcrypt.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return bcrypt.hash(password)


def get_logger(name: str):
    level = logging.getLevelName(settings.LOG_LEVEL)

    new_logger = get_base_logger(name)
    new_logger.setLevel(level)

    return new_logger


def get_login_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.TOKEN_EXPIRES)
    to_encode.update({"exp": expire})
    to_encode["dob"] = to_encode["dob"].strftime("%Y-%m-%d")
    encoded_jwt = jwt.encode(to_encode, settings.SERVER_SECRET)
    return encoded_jwt
