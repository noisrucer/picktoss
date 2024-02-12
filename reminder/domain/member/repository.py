from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from reminder.domain.member.entity import EMember
from reminder.domain.member.exceptions import MemberNotFoundError
from reminder.domain.member.model import Member


class MemberRepository:

    # async def verify_member(self, session: AsyncSession, emember: EMember) -> int:
    #     verified_member = (await session.scalars(select(Member).where(Member.id == emember.id))).first()

    #     if verified_member:
    #         return

    #     member = self._to_member_entity(emember=emember)
    #     session.add(member)
    #     await session.commit()

    async def save(self, session: AsyncSession, member: Member) -> str:
        session.add(member)
        await session.commit()
        return member.id

    def sync_find_all(self, session: Session) -> list[Member]:
        query = select(Member)
        result = session.execute(query)
        return result.scalars().fetchall()

    def _to_member_entity(self, emember: EMember) -> Member:
        return Member(id=emember.id, name=emember.name, email=emember.email)

    async def get_member_or_none_by_id(self, session: AsyncSession, member_id: str) -> Member:
        return (await session.scalars(select(Member).where(Member.id == member_id))).first()

    async def get_member_by_id(self, session: AsyncSession, member_id: str) -> Member:
        member = await self.get_member_or_none_by_id(session, member_id)
        if member is None:
            raise MemberNotFoundError(member_id)
        return member
