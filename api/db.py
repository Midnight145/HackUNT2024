from typing import Mapping

from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.database import Database
import dotenv
import os
from fastapi import APIRouter, Response


# noinspection PyTypeChecker
db: Database = None
route = APIRouter()

def init() -> None:
    global db
    dotenv.load_dotenv()
    uri = os.getenv("MONGO_URI")

    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["HackUNT2024"]
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


def push_item(item: dict, collection: str) -> bool:
    """
    Pushes an item to the database
    :param item: the item to push
    :param collection: the table to push to
    :return: whether the operation was successful
    """
    # noinspection PyBroadException
    try:
        collection = db[collection]
        collection.insert_one(dict(item))
        return True
    except:
        return False

def get_user(user_id: str) -> dict | None:
    """
    Fetches a user from the database
    :param user_id: the user to fetch
    :return: the user if found, None otherwise
    """
    collection = db["users"]
    user = collection.find_one({"userid": user_id})
    if not user:
        return None
    user.pop("_id", None)
    if user:
        return dict(user)
    return None

def seen_products(user_id: str) -> list | None:
    """
    Fetches the products a user has seen
    :param user_id: the user whose seen products we want to fetch
    :return: the list of seen products, or None if the user doesn't exist
    """
    collection = db["users"]
    user = collection.find_one({"userid": user_id})
    if user:
        return user["seen_products"]
    return None

def update_seen_products(user_id: str, seen_products_: list) -> bool:
    """
    Updates the seen products of a user
    :param user_id: the user to update
    :param seen_products_: the new list of seen products
    :return: whether the operation was successful
    """
    collection = db["users"]
    # noinspection PyBroadException
    try:
        collection.update_one({"userid": user_id}, {"$set": {"seen_products": seen_products_}})
        return True
    except:
        return False

def fetch_review(url: str) -> dict | None:
    """
    Fetches a review from the database
    :param url: the reddit url of the review
    :return: the parsed information if found, None otherwise
    """
    collection = db["reviews"]
    review = collection.find_one({"url": url})
    return review

@route.get("/db/fetch_product/{product_id}")
def fetch_product(product_id: str, resp: Response) -> Mapping:
    collection = db["products"]
    product = collection.find_one({"product_id": product_id})
    if product is None:
        resp.status_code = 404
        return {"message": "404 Not Found"}
    product.pop("_id", None)  # pydantic models don't like ObjectId so we remove it
    if product:
        resp.status_code = 200
        return product
    return {"message": "404 Not Found"}

def fetch_product_by_name(product_name: str) -> dict | None:
    """
    Fetches a product by name
    :param product_name: the name of the product
    :return: the product if found, None otherwise
    """
    collection = db["products"]
    product = collection.find_one({"product_name": product_name})
    if product:
        return dict(product)
    return None

@route.get("/db/fetch_user/{user_id}")
def fetch_user(user_id: str, resp: Response) -> dict:
    user = get_user(user_id)
    if user:
        resp.status_code = 200
        return dict(user)
    return {"message": "404 Not Found"}