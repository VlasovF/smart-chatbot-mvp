# backend/tests/test_security.py
from datetime import timedelta

import pytest

from src.core.security import create_access_token, decode_token


def test_jwt_token():
    data = {"sub": "testuser"}
    token = create_access_token(data)

    assert isinstance(token, str)
    assert len(token) > 0

    decoded = decode_token(token)
    assert decoded["sub"] == "testuser"
    assert "exp" in decoded
    assert "iat" in decoded


def test_expired_token():
    data = {"sub": "testuser"}
    token = create_access_token(data, expires_delta=timedelta(seconds=-1))

    with pytest.raises(ValueError, match="Token expired"):
        decode_token(token)
