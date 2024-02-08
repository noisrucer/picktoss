from fastapi import Depends
from jose import ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer

from reminder.domain.member.repository import MemberRepository
from reminder.domain.member.exceptions import JWTError
from reminder.domain.member.service import MemberService
from reminder.config import load_config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/callback", scheme_name="JWT")

member_repository = MemberRepository()
member_service = MemberService(member_repository=member_repository)
cfg = load_config()


def get_current_member_id(token: str = Depends(oauth2_scheme)):
    return member_service.decode_access_token(token)



# def get_token(token: str = Depends(oauth2_scheme)):
#     return token