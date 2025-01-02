import time

import psycopg2
from fastapi import FastAPI, Depends
from psycopg2.extras import RealDictCursor  # type: ignore
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db
from .routers import posts,users,auth


# Dependency to get DB session


models.Base.metadata.create_all(bind=engine)

my_posts = [{"title": "Post 1", "body": "This is post 1 content", 'id': 1},
            {"title": "Post 2", "body": "This is post 2 content", 'id': 2}

            ]






app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"Hello": "World!!!!!"}


@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)

    return posts
