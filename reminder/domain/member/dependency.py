from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError

from reminder.config import load_config
from reminder.domain.member.exceptions import InvalidTokenScopeError, JWTError
from reminder.domain.member.repository import MemberRepository
from reminder.domain.member.service import MemberService
from jose import ExpiredSignatureError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/callback", scheme_name="JWT")

cfg = load_config()


def get_current_member_id(token: str = Depends(oauth2_scheme)):
    def decode_access_token(token: str):
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

    return decode_access_token(token)
