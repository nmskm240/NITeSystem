from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.dialects.sqlite import INTEGER, TEXT, DATETIME
from sqlalchemy.sql.functions import current_timestamp

from . import base

class Member(base.Base):
    __tablename__ = "members"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    student_id = Column(INTEGER)
    discord_id = Column(TEXT)
    name = Column(TEXT)
    created_at = Column(DATETIME, nullable=True, server_default=current_timestamp())

    __table_args__ = (
        UniqueConstraint("student_id", "discord_id", name="unique_id"),
    )
