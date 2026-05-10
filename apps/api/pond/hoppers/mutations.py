from datetime import date
from typing import Optional

import jwt
import strawberry
from strawberry.types import Info

from pond.hoppers.models import Hopper, Pair, RefreshToken
from pond.hoppers.tokens import decode_access_token, set_auth_cookies
from pond.hoppers.types import HopperType


def _require_auth(info: Info) -> Hopper:
    from django.conf import settings
    token = info.context.request.COOKIES.get(settings.ACCESS_TOKEN_COOKIE)
    if not token:
        raise PermissionError('Authentication required')
    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise PermissionError('Token expired')
    except jwt.InvalidTokenError:
        raise PermissionError('Invalid token')
    return Hopper.objects.get(pk=payload['sub'])


@strawberry.type
class AuthPayload:
    hopper: HopperType
    access_token: str


@strawberry.type
class HopperMutations:

    @strawberry.mutation
    def register(self, info: Info, username: str, email: str, password: str) -> AuthPayload:
        if Hopper.objects.filter(username=username).exists():
            raise ValueError('Username already taken')
        hopper = Hopper.objects.create_user(username=username, email=email, password=password)
        refresh = RefreshToken.issue(hopper)
        access = set_auth_cookies(info.context.response, hopper, refresh)
        return AuthPayload(hopper=hopper, access_token=access)

    @strawberry.mutation
    def login(self, info: Info, username: str, password: str) -> AuthPayload:
        from django.contrib.auth import authenticate
        hopper = authenticate(info.context.request, username=username, password=password)
        if hopper is None:
            raise ValueError('Invalid credentials')
        refresh = RefreshToken.issue(hopper)
        access = set_auth_cookies(info.context.response, hopper, refresh)
        return AuthPayload(hopper=hopper, access_token=access)

    @strawberry.mutation
    def refresh_token(self, info: Info) -> AuthPayload:
        from django.conf import settings
        raw = info.context.request.COOKIES.get(settings.REFRESH_TOKEN_COOKIE)
        if not raw:
            raise ValueError('No refresh token')
        try:
            old = RefreshToken.objects.select_related('hopper').get(token=raw)
        except RefreshToken.DoesNotExist:
            raise ValueError('Invalid refresh token')
        if not old.is_valid():
            old.delete()
            raise ValueError('Refresh token expired')
        hopper = old.hopper
        old.delete()
        new_refresh = RefreshToken.issue(hopper)
        access = set_auth_cookies(info.context.response, hopper, new_refresh)
        return AuthPayload(hopper=hopper, access_token=access)

    @strawberry.mutation
    def logout(self, info: Info) -> bool:
        from django.conf import settings
        raw = info.context.request.COOKIES.get(settings.REFRESH_TOKEN_COOKIE)
        if raw:
            RefreshToken.objects.filter(token=raw).delete()
        resp = info.context.response
        resp.delete_cookie(settings.ACCESS_TOKEN_COOKIE)
        resp.delete_cookie(settings.REFRESH_TOKEN_COOKIE)
        return True

    @strawberry.mutation
    def update_hopper(
        self,
        info: Info,
        name: Optional[str] = None,
        email: Optional[str] = None,
        birth_date: Optional[str] = None,
    ) -> HopperType:
        hopper = _require_auth(info)
        if name is not None:
            hopper.name = name
        if email is not None:
            hopper.email = email
        if birth_date is not None:
            hopper.birth_date = date.fromisoformat(birth_date)
        hopper.save()
        return hopper

    @strawberry.mutation
    def follow_hopper(self, info: Info, slug: str) -> HopperType:
        me = _require_auth(info)
        try:
            target = Hopper.objects.get(slug=slug)
        except Hopper.DoesNotExist:
            raise ValueError('Hopper not found')
        if target == me:
            raise ValueError('Cannot follow yourself')
        pair, created = Pair.objects.get_or_create(first_hopper=me, second_hopper=target)
        if not created:
            pair.delete()
        return target

