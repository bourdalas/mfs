from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mfs.backend import crud, schemas
from mfs.backend.dependencies import get_db

router = APIRouter(
    prefix="/user_groups",
    tags=["user_groups"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[schemas.UserGroup])
def read_all_usergroups(db: Session = Depends(get_db)):
    return crud.get_all_user_groups(db)


@router.post("/create/", response_model=schemas.UserGroup)
def create_new_usergroup(group: schemas.UserGroupCreate, db: Session = Depends(get_db)):
    return crud.create_user_group(db, user_group=group)


@router.put("/add/", response_model=schemas.UserGroup)
def add_user_to_group(data: schemas.UserGroupJoin, db: Session = Depends(get_db)):
    return crud.add_user_to_user_group(db, **data.dict())


@router.get("/{group_id}/users", response_model=List[schemas.User])
def read_users_in_user_group(group_id: int, db: Session = Depends(get_db)):
    return crud.get_users_in_user_group(db, group_id=group_id)

@router.get("/{group_id}/latest_messages/{n}", response_model=List[schemas.Message])
def read_latest_messages_for_user_group(group_id: int, n: int = 100, db: Session = Depends(get_db)):
    return crud.get_latest_messages_for_user_group(db, group_id=group_id, n=n)

@router.post("/{group_id}/messages", response_model=schemas.Message)
def create_message(group_id: int, message: schemas.MessageCreate, db: Session = Depends(get_db)):
    return crud.create_message_for_user_group(db, message=message, group_id=group_id)
