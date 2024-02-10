from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from reminder.domain.member.entity import EMember
from reminder.domain.member.model import Member
from sqlalchemy.orm import Session


class MemberRepository:

    async def verify_member(self, session: AsyncSession, emember: EMember) -> int:
        verified_member = (await session.scalars(select(Member).where(Member.id == emember.id))).first()

        if verified_member:
            return

        member = self._to_member_entity(emember=emember)
        session.add(member)
        await session.commit()

    def sync_find_all(self, session: Session) -> list[Member]:
        query = select(Member)
        result = session.execute(query)
        return result.scalars().fetchall()

    def _to_member_entity(self, emember: EMember) -> Member:
        return Member(id=emember.id, name=emember.name, email=emember.email)

    # async def get_member_by_id(self, session: AsyncSession, member_id: str):
    #     member = (await session.scalars(select(Member).where(Member.member_id == member_id))).first()

    #     if not member:
    #         return None

    #     return
