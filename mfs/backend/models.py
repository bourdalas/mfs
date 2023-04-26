from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from mfs.backend.database import Base


user_group_members = Table(
    "user_group_members",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("user_group_id", ForeignKey("user_groups.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    password = Column(String)
    subscription_datetime = Column(DateTime)
    last_active_datetime = Column(DateTime)
    is_active = Column(Boolean, default=False)

    items = relationship("Item", back_populates="owner")

    groups = relationship(
        "UserGroup", secondary=user_group_members, back_populates="members"
    )
    messages_sent = relationship("Message", back_populates="sender")


class UserGroup(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, index=True)

    members = relationship("User", secondary=user_group_members, back_populates="groups")
    messages = relationship("Message", back_populates="group")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    sender_username = Column(Integer, ForeignKey("users.username"))
    group_id = Column(Integer, ForeignKey("user_groups.id"))
    timestamp = Column(DateTime, default=datetime.utcnow())

    sender = relationship("User")
    group = relationship("UserGroup")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")