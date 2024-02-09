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


class MemberService:
    def __init__(self, member_repository: MemberRepository):
        self.member_repository = member_repository
        self.kakao_auth_server = "https://kauth.kakao.com"
        self.kakao_api_server = "https://kapi.kakao.com"
        self.default_header = {"Content-Type": "application/x-www-form-urlencoded"}

    def redirect_response(self):
        url = f"https://kauth.kakao.com/oauth/authorize?client_id={cfg.oauth.client_id}&response_type=code&redirect_uri={cfg.oauth.redirect_uri}"

        response = RedirectResponse(url)

        return response

    def token_auth(self, code):
        return requests.post(
            url=self.kakao_auth_server + "/oauth/token",
            headers=self.default_header,
            data={
                "grant_type": "authorization_code",
                "client_id": cfg.oauth.client_id,
                "client_secret": cfg.oauth.client_secret,
                "redirect_uri": cfg.oauth.redirect_uri,
                "code": code,
            },
        ).json()

    def get_member_info(self, access_token):
        return requests.post(
            url=self.kakao_api_server + "/v2/user/me",
            headers={
                **self.default_header,
                **{"Authorization": f"Bearer {access_token}"},
            },
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
