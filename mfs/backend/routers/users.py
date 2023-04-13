
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from mfs.backend import crud, schemas
from mfs.backend.dependencies import get_db
from mfs.backend.emailsender import EmailSender
from mfs.backend.factories.emailsenderfactory import create_env_email_sender

router = APIRouter(tags=["users"])

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreateFull, db: Session = Depends(get_db)):
    db_username_user = crud.get_user_by_username(db=db, username=user.username)
    db_email_user = crud.get_user_by_email(db=db, email=user.email)
    if db_email_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if db_username_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db=db,skip=skip, limit=limit)
    return users

@router.get("/users/id/{user_id}", response_model=schemas.User)
def read_user_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db,user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/email/{user_email}/", response_model=schemas.User)
def read_user_email(user_email: str, db: Session = Depends(get_db)):

    db_user = crud.get_user_by_email(db=db,email=user_email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/username/{username}/", response_model=schemas.User)
def read_user_username(username: str, db: Session = Depends(get_db)):

    db_user = crud.get_user_by_username(db=db,username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/username_password/{username}/", response_model=schemas.UserLoginResponse, include_in_schema=False)
def read_username_password(username: str,db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db=db,username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserLoginResponse(id=db_user.id, name=db_user.name, email=db_user.email, username=db_user.username, password=db_user.password, last_active_datetime=db_user.last_active_datetime)


@router.put("/users/{username}/email/", response_model=schemas.User)
def update_user_email(username: str, email: str, db: Session = Depends(get_db)):
    db_user = crud.update_user_email(db=db, username=username, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/users/{username}/is_active/", response_model=schemas.User)
def update_user_is_active(username: str, is_active: bool, db: Session = Depends(get_db)):
    db_user = crud.update_user_is_active(db=db, username=username, is_active=is_active)
    db_user = crud.update_last_is_active_datetime(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/users/{username}")
async def delete_user(username: str, db: Session = Depends(get_db)):#, current_user: schemas.User = Depends(get_current_active_user)):
    # if not current_user.username == username:
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")
    if not crud.delete_user_by_username(db, username):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"detail": "User deleted"}



@router.post("/users/{username}/items/", response_model=schemas.Item)
def create_item_for_user(
    username: str, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, username=username)


@router.post("/users/send_signup_email/{username}/")
def send_sign_up_email_to_user(username: str, db: Session = Depends(get_db), email_sender: EmailSender = Depends(create_env_email_sender)):
    db_user = crud.get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    email_sender.send_sign_up_email(db_user.name, db_user.email)
