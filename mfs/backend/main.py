from fastapi import FastAPI

from mfs.backend.database import Base, engine
from mfs.backend.routers import items, users, usergroups

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(usergroups.router)