from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from reminder.domain.member.entity import EMember
from reminder.domain.member.model import Member


class MemberRepository:

    async def verify_member(self, session: AsyncSession, emember: EMember) -> int:
        verified_member = (await session.scalars(select(Member).where(Member.id == emember.id))).first()

        if verified_member:
            return

        member = self._to_member_entity(emember=emember)
        session.add(member)
        await session.commit()

    def _to_member_entity(self, emember: EMember) -> Member:
        return Member(
            id=emember.id,
            name=emember.name,
        )

    # async def get_member_by_id(self, session: AsyncSession, member_id: int):
    #     member = (await session.scalars(select(Member).where(Member.member_id == member_id))).first()

    #     if not member:
    #         return None

    #     return
