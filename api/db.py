from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.database import Database
import dotenv
import os
from fastapi import APIRouter, Response
from api.models import *

# noinspection PyTypeChecker
db: Database = None
route = APIRouter()

def init():
    global db
    dotenv.load_dotenv()
    uri = f"mongodb+srv://rubikscubeboy27:{os.getenv('MONGODB_PASS')}@hackunt2024.tdiel.mongodb.net/?retryWrites=true&w=majority&appName=hackunt2024"

    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["HackUNT2024"]
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


def push_item(item: BaseModel, collection: str):
    # noinspection PyBroadException
    try:
        collection = db[collection]
        collection.insert_one(dict(item))
        return True
    except:
        return False


@route.get("/db/fetch_product/{product_id}")
def fetch_product(product_id: str, resp: Response):
    collection = db["products"]
    product = collection.find_one({"product_id": product_id})
    product.pop("_id", None)
    if product:
        resp.status_code = 200
        return product
    return {"message": "404 Not Found"}

def get_user(user_id: str):
    collection = db["users"]
    user = collection.find_one({"userid": user_id})
    if not user:
        return None
    user.pop("_id", None)
    if user:
        return dict(user)
    return None

def seen_products(user_id: str):
    collection = db["users"]
    user = collection.find_one({"userid": user_id})
    if user:
        return user["seen_products"]
    return None

def update_seen_products(user_id: str, seen_products: list):
    collection = db["users"]
    collection.update_one({"userid": user_id}, {"$set": {"seen_products": seen_products}})

def store_product(product: Product):
    if push_item(product, "products"):
        return {"message": "200 OK"}
    return {"message": "500 Internal Server Error"}

@route.get("/db/fetch_user/{user_id}")
def fetch_user(user_id: str, resp: Response):
    user = get_user(user_id)
    if user:
        resp.status_code = 200
        return dict(user)
    return {"message": "404 Not Found"}

def store_user(user: User):
    if push_item(user, "users"):
        return {
            "userid": user.userid,
            "username": user.username,
            "email": user.email,
            "seen_products": user.seen_products
        }
    return None

def fetch_review(url: str):
    collection = db["reviews"]
    review = collection.find_one({"url": url})
    return review

@route.post("/db/store_review")
def store_review(review: Review, resp: Response):
    if push_item(review, "reviews"):
        resp.status_code = 200
        return {"message": "200 OK"}
    return {"message": "500 Internal Server Error"}

@route.get("/db/fetch_product_reviews")
def fetch_product_reviews():
    collection = db["reviews"]
    reviews = collection.find()
    return [i.pop("_id", None) for i in reviews]
