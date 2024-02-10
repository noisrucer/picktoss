from typing import Optional

import requests
from fastapi import APIRouter, Depends

from reminder.config import load_config
from reminder.dependency.db import DBSessionDep
from reminder.domain.member.dependency import get_current_member_id, member_service
from reminder.domain.member.dtos import CallbackResponse
from reminder.domain.member.entity import EMember
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["member"])


cfg = load_config()

"""
1. Client -> /oauth/url
2. End user -> google login 페이지 보임 -> 동의후에 클릭
3. Google이 query param에 code를 넣어서 callbackurl에 보냄
4. Backend가 callback endpoint에 들어온 요청에서, "code" query param을 추출을 한다
5. Backend -> Google, client_id, code, 등 넣어서 user 정보 반환
6. JWT token 생성 -> front 반환
"""


@router.get("/oauth/url")
def oauth_url_api():
    return {"oauth_url": f"https://accounts.google.com/o/oauth2/auth?client_id={cfg.oauth.client_id}&response_type=code&redirect_uri={cfg.oauth.redirect_uri}&scope=openid%20email%20profile"}


@router.get("/callback")
async def oauth_callback(session: DBSessionDep, code: Optional[str] = None) -> CallbackResponse:
    token = member_service.token_auth(code=code)
    member_info = member_service.get_member_info(token["access_token"])
    access_token = member_service.create_access_token(member_info["id"])

    emember = EMember(id=member_info["id"], name=member_info["name"], email=member_info["email"])

    await member_service.verify_member(session=session, emember=emember)

    return RedirectResponse(f"http://localhost:5173/oauth?access-token={access_token}")
    # return RedirectResponse(f"https://pick-toss.vercel.app/oauth?access-token={access_token}")
    # return CallbackResponse(access_token=access_token, token_type="Bearer")


@router.get("/protected")
def protect(current_user_id: str = Depends(get_current_member_id)):
    return {"current_user_id": current_user_id}
