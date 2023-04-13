from datetime import datetime

from sqlalchemy.orm import Session

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