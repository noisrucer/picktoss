from typing import Optional

import requests
from fastapi import APIRouter, Depends

from reminder.config import load_config
from reminder.dependency.db import DBSessionDep
from reminder.domain.member.dependency import get_current_member_id, member_service
from reminder.domain.member.dtos import CallbackResponse
from reminder.domain.member.entity import EMember

router = APIRouter(tags=["member"])


cfg = load_config()


@router.get("/oauth/url")
def oauth_url_api():
    response = member_service.redirect_response()
    return response


@router.get("/callback", response_model=CallbackResponse)
async def oauth_callback(session: DBSessionDep, code: Optional[str] = None) -> CallbackResponse:
    token = member_service.token_auth(code=code)
    member_info = member_service.get_member_info(token["access_token"])
    access_token = member_service.create_access_token(member_info["id"])

    emember = EMember(
        id=member_info["id"],
        name=member_info["properties"]["nickname"],
    )

    await member_service.verify_member(session=session, emember=emember)
    return CallbackResponse(access_token=access_token, token_type="Bearer")


# @router.get('/logout')
# def kakaoLogout(request: Request, response: Response):
#     url = "https://kapi.kakao.com/v1/user/logout"
#     headers = {
#       "Authorization": f"Bearer WQj4T8f1lCw1I2gDRkTzK-3na9-GKnNVw-sKPXTZAAABjYRejBwq17LwdM8QAg"
#     }
#     res = requests.post(
#       url=url,
#       headers=headers
#     )

#     return {"logout": res.json()}


@router.get("/unlink")
def kakaoLogout():
    url = "https://kapi.kakao.com/v1/user/unlink"
    headers = {"Authorization": f"Bearer A4h3PKwYlkGUGg9b1KbklVmL9h8k4VnFH7kKKiURAAABjYhiqOsq17LwdM8QAg"}
    res = requests.post(url=url, headers=headers)
    return {"logout": res.json()}


@router.get("/protected")
def protect(current_user_id: str = Depends(get_current_member_id)):
    return {"current_user_id": current_user_id}
