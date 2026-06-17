from datetime import datetime, timedelta

import bcrypt
from authlib.jose import JsonWebSignature, JsonWebToken
from authlib.jose.errors import BadSignatureError, ExpiredTokenError

from src.core.config import settings

# Инициализация JWT
jwt = JsonWebToken(["HS256"])
jws = JsonWebSignature()


def hash_password(password: str) -> str:
    """Хеширует пароль с помощью bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль"""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(
    data: dict, expires_delta: timedelta | None = None
) -> str:
    """Создаёт JWT токен"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire, "iat": datetime.utcnow()})

    # Создаём заголовок и payload
    header = {"alg": "HS256", "typ": "JWT"}

    # Кодируем токен
    token = jwt.encode(header, to_encode, settings.SECRET_KEY)
    return token.decode("utf-8")


def decode_token(token: str) -> dict:
    """Декодирует и валидирует JWT токен"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
        payload.validate()
        return payload
    except (BadSignatureError, ExpiredTokenError) as e:
        raise ValueError(f"Invalid token: {str(e)}") from e
