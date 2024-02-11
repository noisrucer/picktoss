from datetime import datetime, timedelta

import requests
from fastapi.responses import RedirectResponse
from jose import ExpiredSignatureError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from reminder.config import load_config
from reminder.domain.document.constant import get_max_document_num_by_subscription_plan
from reminder.domain.document.service import DocumentService
from reminder.domain.member.entity import EMember
from reminder.domain.member.exceptions import InvalidTokenScopeError, JWTError
from reminder.domain.member.model import Member
from reminder.domain.member.repository import MemberRepository
from reminder.domain.member.response.get_member_info_response import (
    GetMemberInfoDocumentDto,
    GetMemberInfoResponse,
    GetMemberInfoSubScriptionDto,
)
from reminder.domain.subscription.enum import SubscriptionPlanType
from reminder.domain.subscription.model import Subscription
from reminder.domain.subscription.repository import SubscriptionRepository
from reminder.domain.subscription.service import SubscriptionService

cfg = load_config()


class MemberService:
    def __init__(
        self,
        member_repository: MemberRepository,
        subscription_repository: SubscriptionRepository,
        subscription_service: SubscriptionService,
        document_service: DocumentService
    ):
        self.member_repository = member_repository
        self.subscription_repository = subscription_repository
        self.subscription_service = subscription_service
        self.document_service = document_service

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

    def get_google_member_info(self, access_token):
        return requests.get(
            url="https://www.googleapis.com/oauth2/v2/userinfo", headers={"Authorization": f"Bearer {access_token}"}
        ).json()

    async def verify_member(self, session: AsyncSession, emember: EMember):
        existing_member = await self.member_repository.get_member_or_none_by_id(session, emember.id)
        if existing_member:
            return

        # If new member
        new_member = Member(id=emember.id, name=emember.name, email=emember.email)
        await self.member_repository.save(session, new_member)

        # Create new Free Subscription entry
        now = datetime.utcnow()
        free_subscription = Subscription(
            plan_type=SubscriptionPlanType.FREE,
            purchased_date=now,
            expire_date=now + timedelta(days=30),
            member_id=new_member.id,
        )
        await self.subscription_repository.save(session, free_subscription)

    async def get_member_info(self, session: AsyncSession, member_id: str) -> GetMemberInfoResponse:
        subscription: Subscription = await self.subscription_service.get_current_subscription_by_member_id(
            session, member_id
        )
        used_document_num = (
            await self.document_service.get_num_uploaded_documents_for_current_subscription_by_member_id(
                session, member_id
            )
        )
        return GetMemberInfoResponse(
            subscription=GetMemberInfoSubScriptionDto(
                plan=subscription.plan_type,
                purchasedDate=subscription.purchased_date,
                expireDate=subscription.expire_date,
            ),
            document=GetMemberInfoDocumentDto(
                currentSubscriptionCycleTotalDocuments=get_max_document_num_by_subscription_plan(
                    subscription.plan_type
                ),
                currentSubscriptionCycleUsedDocuments=used_document_num,
            ),
        )

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
