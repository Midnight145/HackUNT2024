from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    userid: str
    seen_products: list[str]

class Product(BaseModel):
    productid: str
    product_name: str
    description: str

class Review(BaseModel):
    reviewid: str
    productid: str
    summary: str
    recommended: str

class Login(BaseModel):
    username: str
    password: str