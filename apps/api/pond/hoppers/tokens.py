from datetime import timedelta

import jwt
from django.conf import settings
from django.utils import timezone


def make_access_token(hopper) -> str:
    payload = {
        'sub': str(hopper.pk),
        'username': hopper.username,
        'exp': timezone.now() + timedelta(seconds=settings.ACCESS_TOKEN_LIFETIME_SECONDS),
        'iat': timezone.now(),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])


def set_auth_cookies(response, hopper, refresh_token) -> str:
    access = make_access_token(hopper)
    secure = not settings.DEBUG
    response.set_cookie(
        settings.ACCESS_TOKEN_COOKIE,
        access,
        max_age=settings.ACCESS_TOKEN_LIFETIME_SECONDS,
        httponly=True,
        samesite='Lax',
        secure=secure,
    )
    response.set_cookie(
        settings.REFRESH_TOKEN_COOKIE,
        refresh_token.token,
        max_age=settings.REFRESH_TOKEN_LIFETIME_SECONDS,
        httponly=True,
        samesite='Lax',
        secure=secure,
    )
    return access
