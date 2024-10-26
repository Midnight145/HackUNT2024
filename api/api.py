import os

import fastapi
from auth0.authentication import Database, GetToken
from dotenv import load_dotenv

import search
from api import lib

load_dotenv()
app = fastapi.FastAPI()
auth0 = Database(domain=os.getenv("DOMAIN"), client_id=os.getenv("CLIENT_ID"))
get_token = GetToken(domain=os.getenv("DOMAIN"), client_id=os.getenv("CLIENT_ID"))

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/login")
def login(username: str, password: str):
    return get_token.login(username, password, realm='Username-Password-Authentication')

@app.post("/register")
def register(username: str, password: str):
    return auth0.signup(username, password, connection='Username-Password-Authentication')

@app.post("/search")
def search_(query: str):
    return search.search_reddit(query)

@app.post("/fetch_viewed_products")
def fetch_viewed_products(token: str):
    return lib.fetch_viewed_products(token)