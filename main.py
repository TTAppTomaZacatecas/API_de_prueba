from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid

app = FastAPI()

posts = []

# Post model
class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    crated_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False

@app.get("/")
def root():
    return "Hola mundo"

@app.get("/holajson")
def bienvenida():
    return {"welcome": "Bienvenido"}

@app.get("/saludo/{mensaje}")
def get_lol(mensaje: str):
    return f"Hola!, aqui te estoy saludando ${mensaje}"

@app.get("/posts")
def get_posts():
    return posts

@app.post("/posts")
def save_post(post: Post):
    # dict() sirve para darle el formato necesario para almacenarlo en dormato de diccionario de javascript
    post.id = str(uuid())
    posts.append(post.dict())
    return posts[-1]

@app.get("/post/{post_id}")
def get_post(post_id: str):
    for post in posts:
        if post["id"] == post_id:
            return post
    return HTTPException(status_code=404, detail="Post no encontrado")

@app.delete("/post/{post_id}")
def delete_post(post_id: str):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            # pop() quita el elemento con el intex que yo le indique
            posts.pop(index)
            return {"message": "Pot has been deleted successfully"}
    return HTTPException(status_code=404, detail="Post no encontrado")

@app.put("/posts/{post_id}")
def save_post(post_id: str, updatedPost: Post):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts[index]["title"] = updatedPost.title
            posts[index]["content"] = updatedPost.content
            posts[index]["author"] = updatedPost.author
            return {"message": "Pot has been updated successfully"}
    return HTTPException(status_code=404, detail="Post no encontrado")
