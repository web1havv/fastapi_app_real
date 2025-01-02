from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from app import schemas, models, oauth2
from app.database import get_db, engine

models.Base.metadata.create_all(bind=engine)
router = APIRouter(tags=['posts'])


@router.get("/posts")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('''SELECT * FROM posts ''')
    # posts=cursor.fetchall()
    posts = db.query(models.Post).all()
    print(posts)

    return posts


@router.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """, (new_post.title,new_post.content,new_post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    print(current_user.email)

    new_post = models.Post(**new_post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    print('POST CREATED SUCCESSFULLY')

    return new_post


# @app.get('/posts/latest')
# def get_latest_post():
#     post = my_posts[len(my_posts) - 1]
#     return post


@router.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    print(id)
    # cursor.execute("""SELECT * FROM posts WHERE ID = (%s)""",(str(id),))
    # particular_post= cursor.fetchone()
    # print(particular_post)
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'invalid post,post not found')

    print(post)
    return post


@router.delete("/posts/{id}")
def delete_post(id, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute('''DELETE FROM posts where id = %s RETURNING *''',(str(id),))
    # deleted_post=cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'invalid post,post not found')
    post.delete(synchronize_session=False)
    db.commit()
    return {"message": "post deleted successfully"}


@router.put('/posts/{id:int}')
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)

):
# index=find_index_posts(id)
# if index is None:
#     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'invalid post,post not found')
# post_dict=post.model_dump()
# post_dict['id']=id
# my_posts[index]=post_dict
# cursor.execute('''UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *''',(post.title,post.content,post.published,(str(id),)))
# updated_post=cursor.fetchone()
# conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    first_post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'invalid post,post not found')
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return {'data': post_query.first()}
