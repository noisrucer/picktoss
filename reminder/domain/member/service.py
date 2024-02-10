from datetime import datetime, timedelta

import requests
from fastapi.responses import RedirectResponse
from jose import ExpiredSignatureError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from reminder.config import load_config
from reminder.domain.member.entity import EMember
from reminder.domain.member.exceptions import InvalidTokenScopeError, JWTError
from reminder.domain.member.repository import MemberRepository

cfg = load_config()


"""
1. Client -> 
"""


class MemberService:
    def __init__(self, member_repository: MemberRepository):
        self.member_repository = member_repository

    def redirect_response(self):
        url = f"https://accounts.google.com/o/oauth2/auth?client_id={cfg.oauth.client_id}&response_type=code&redirect_uri={cfg.oauth.redirect_uri}&scope=openid%20email%20profile"
        response = RedirectResponse(url)

        return response

    def token_auth(self, code):
        return requests.post(
            url="https://oauth2.googleapis.com/token",
            data={
                "grant_type": "authorization_code",
                "client_id": cfg.oauth.client_id,
                "client_secret": cfg.oauth.client_secret,
                "redirect_uri": cfg.oauth.redirect_uri,
                "code": code,
            },
        ).json()

    def get_member_info(self, access_token):
        return requests.get(
            url="https://www.googleapis.com/oauth2/v2/userinfo", headers={"Authorization": f"Bearer {access_token}"}
        ).json()

    async def verify_member(self, session: AsyncSession, emember: EMember):
        await self.member_repository.verify_member(session=session, emember=emember)

    def create_access_token(self, sub: str | int):
        payload = {
            "sub": str(sub),
            "scope": "access_token",
            "exp": datetime.utcnow() + timedelta(minutes=cfg.jwt.access_token_expire_minutes),
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, cfg.jwt.secret_key, cfg.jwt.algorithm)

    def decode_access_token(self, token: str):
        try:
            payload = jwt.decode(token, cfg.jwt.secret_key, algorithms=[cfg.jwt.algorithm])
            if payload["scope"] != "access_token":
                raise InvalidTokenScopeError
            member_id = payload["sub"]
            return member_id
        except ExpiredSignatureError:
            raise JWTError()
        except Exception:
            raise JWTError()
