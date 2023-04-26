from datetime import datetime
from typing import List
from fastapi import HTTPException

from sqlalchemy.orm import Session, joinedload

from mfs.backend import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first() #type: ignore


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first() #type: ignore

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first() #type: ignore


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query( models.User).offset(skip).limit(limit).all() #type: ignore


def create_user(db: Session, user: schemas.UserCreateFull):
    db_user = models.User(
        email=user.email, 
        username=user.username, 
        name=user.name, 
        password=user.password,
        subscription_datetime=user.subscription_datetime,
        last_active_datetime=user.last_active_datetime        
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_is_active(db: Session, username: str, is_active: bool):
    db_user = get_user_by_username(db, username=username)
    if db_user is None:
        return None
    db_user.is_active = is_active
    db.commit()
    db.refresh(db_user)
    return db_user


def update_last_is_active_datetime(db: Session, username: str):
    db_user = get_user_by_username(db, username=username)
    if db_user is None:
        return None
    db_user.last_active_datetime = datetime.now()
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_email(db: Session, username: str, email: str):
    db_user = get_user_by_username(db, username=username)
    if db_user is None:
        return None
    db_user.email = email
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user_by_username(db: Session, username: str) -> bool:
    user = get_user_by_username(db, username=username)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True


def get_item(db: Session, item_id: str):
    return db.query(models.Item).filter(models.Item.id == item_id).first() #type: ignore


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all() #type: ignore


def create_user_item(db: Session, item: schemas.ItemCreate, username: str):
    db_user = get_user_by_username(db, username)
    db_item = models.Item(**item.dict(), owner_id=db_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_user_group(db: Session, user_group: schemas.UserGroupCreate):
    db_user_group = models.UserGroup(**user_group.dict())
    db.add(db_user_group)
    db.commit()
    db.refresh(db_user_group)
    return db_user_group

def add_user_to_user_group(db: Session, username: str, group_id: str):
    user = db.query(models.User).filter_by(username=username).first()
    group = db.query(models.UserGroup).filter_by(id=group_id).first()
    if user.username in [_user.username for _user in group.members]:
        raise HTTPException(403)

    group.members.append(user)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

def get_all_user_groups(db: Session):
    return db.query(models.UserGroup).all()

def get_user_groups(db: Session, username: str):
    user = db.query(models.User).filter_by(username=username).first()
    return user.groups

def create_message_for_user_group(db: Session, message: schemas.MessageCreate, group_id: int):
    user = db.query(models.User).filter(models.User.username == message.sender_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    group = db.query(models.UserGroup).filter(models.UserGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="User group not found")
    db_message = models.Message(**message.dict(), group_id=group_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_latest_messages_for_user_group(db: Session, group_id: int, n: int):
    group = db.query(models.UserGroup).filter(models.UserGroup.id == group_id).first()
    if not group:
        raise HTTPException(404, "Group not found")
    messages = db.query(models.Message).filter(models.Message.group_id == group_id).order_by(models.Message.timestamp.asc()).limit(n).all()
    return messages


def get_users_in_user_group(db: Session, group_id: int) -> List[schemas.User]:
    group = db.query(models.UserGroup).filter(models.UserGroup.id == group_id).first()
    if not group:
        return []
    return group.members