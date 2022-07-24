from ast import Str
import string
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    class Config:
        orm_mode = True
    

class CreatedPost(Post):
    pass 
    class Config:
        orm_mode = True


    

class Posted(Post):
    id : int