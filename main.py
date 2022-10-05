from typing import List
import fastapi
from fastapi import FastAPI, Depends

import sqlalchemy.orm as _orm
import src.services as _services
import src.schemas as _schemas

app = FastAPI()

_services.create_database()


@app.post("/users/", response_model=_schemas.User)
def create_user(
        user: _schemas.UserCreate, db: _orm.Session = Depends(_services.get_db)
):
    db_user = _services.get_user_by_email(db=db, email=user.email)

    if db_user:
        raise fastapi.HTTPException(status_code=404, detail="woops the email is in use")
    return _services.create_user(db=db, user=user)


@app.get("/users/", response_model=List[_schemas.User])
def get_user_list(
        skip: int = 0, limit: int = 10, db: _orm.Session = Depends(_services.get_db)
):
    user_list = _services.get_user_list(db=db, skip=skip, limit=limit)
    return user_list


@app.get("/users/{user_id}", response_model=_schemas.User)
def get_user_info(
        user_id: int, db: _orm.Session = Depends(_services.get_db)
):
    db_user = _services.get_user_by_id(db=db, user_id=user_id)

    if db_user is None:
        raise fastapi.HTTPException(status_code=404, detail="sorry this user does not exist")

    return db_user


@app.post("/posts/", response_model=_schemas.Post)
def create_post(
        post: _schemas.PostCreate, user_id: int, db: _orm.Session = Depends(_services.get_db)
):
    post = _services.create_post(db=db, post=post, user_id=user_id)

    if post is None:
        raise fastapi.HTTPException(status_code=404, detail="sorry this user does not exist")

    return post


@app.get("/posts/", response_model=List[_schemas.Post])
def get_post_list(
        skip: int = 0, limit: int = 10, db: _orm.Session = Depends(_services.get_db)
):
    post_list = _services.get_post_list(db=db, skip=skip, limit=limit)
    return post_list


@app.get("/posts/{post_id}", response_model=_schemas.Post)
def get_post_info(
        post_id: int, db: _orm.Session = Depends(_services.get_db)
):
    post = _services.get_post_info(db=db, post_id=post_id)

    if post is None:
        raise fastapi.HTTPException(status_code=404, detail=f"The post_id: {post_id} is not created")

    return post


@app.delete("/posts/{post_id}")
def delete_post(
        post_id: int, db: _orm.Session = Depends(_services.get_db)
):
    _services.delete_post(db=db, post_id=post_id)
    return {"message": f"The post_id: {post_id} is deleted!"}


@app.put("/posts/{post_id}", response_model=_schemas.Post)
def update_post(
        post_id: int,
        post: _schemas.PostCreate,
        db: _orm.Session = Depends(_services.get_db)
):
    db_post = _services.update_post(db=db, post=post, post_id=post_id)
    return db_post
