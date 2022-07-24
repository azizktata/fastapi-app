

from fastapi import FastAPI

from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import  Models, Schemas
import os
from dotenv import load_dotenv

import uvicorn


load_dotenv(".env")

app = FastAPI()



app.add_middleware(DBSessionMiddleware, db_url="postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    posts = db.session.query(Models.Post).all()
    return posts

@app.get("/posts/{id}")
def get_post(id:int): 
    post = db.session.query(Models.Post).filter(Models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=404, detail=f"post with id : {id} does not exist")
    return  post

@app.post("/posts", response_model=Schemas.CreatedPost, status_code=201)
def post(post: Schemas.Post):
    db_post = Models.Post(**post.dict())
    db.session.add(db_post)
    db.session.commit()
    db.session.refresh(db_post)
    
    return db_post

@app.put("/posts/{id}",response_model=Schemas.Post, status_code=200)
def update_post(id: int, post: Schemas.Post):
    found_post = db.session.query(Models.Post).filter(Models.Post.id == id)
    if found_post.first() == None:
        raise HTTPException(status_code=404, detail=f"post with id : {id} do not exist")

    found_post.update(post.dict())
    db.commit()

    return found_post.first()

@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int):
    post = db.session.query(Models.Post).filter(Models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=404, detail=f"post with id : {id} do not exist")

    post.delete()
    db.commit()
    return "successfuly deleted"

if __name__=='__main__':
    uvicorn.run(app, port=8000, host="0.0.0.0")

