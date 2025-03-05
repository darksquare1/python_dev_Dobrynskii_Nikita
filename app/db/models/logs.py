import datetime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import CheckConstraint
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class SpaceType(Base):
    __tablename__ = 'space_type'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(6), unique=True, nullable=False)

    __table_args__ = (
        CheckConstraint("name IN ('global', 'blog', 'post')", name='check_space_type'),
    )


class EventType(Base):
    __tablename__ = 'event_type'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)

    __table_args__ = (
        CheckConstraint("name IN ('login', 'logout', 'comment', 'create_post', 'delete_post')",
                        name='check_event_type'),
    )


class Logs(Base):
    __tablename__ = 'logs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_time: Mapped[datetime] = mapped_column('datetime', DateTime(timezone=True), server_default=func.now())
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    space_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('space_type.id'))
    event_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('event_type.id'))

    __table_args__ = (
        # Так как значения name фиксированы в таблицах event_type, space_type и вносим их туда мы, то имеем право добавить чек по id
        CheckConstraint(
            "(space_type_id = 1 AND event_type_id IN (1, 2)) OR "  # global -> login/logout
            "(space_type_id = 2 AND event_type_id IN (3, 4)) OR "  # blog -> create_post/delete_post
            "(space_type_id = 3 AND event_type_id = 5)",  # post -> comment
            name='check_space_event_combination'
        ),
    )
