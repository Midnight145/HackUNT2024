import os
from uuid import uuid4

import fastapi

import score
from api import auth
from api import db

db.init()
app = fastapi.FastAPI()
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv

load_dotenv()


class DynamicCORSMiddleware(BaseHTTPMiddleware):
    """
    This is entirely so that we can dynamically set the allowed origins based on the request.
    This is not a good idea in production, but it's fine for a hackathon.
    In general, you should have a whitelist of allowed origins and not allow arbitrary origins, but I wasn't sure how
    to pull off what I needed to do without dynamically setting the allowed origins.
    """

    async def dispatch(self, request: Request, call_next):
        print(request.cookies)
        origin = request.headers.get("origin")
        if not origin:
            origin = "*"

        if request.method == "OPTIONS":
            print("Handling preflight request")
            response = JSONResponse(content={"message": "Preflight request OK"})
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = ','.join(["Accept", "Accept-Language", "Content-Language",
                                                                "Content-Type"])
            response.headers["Access-Control-Allow-Credentials"] = "true"
            return response

        # Handle CORS for actual requests
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE"
        response.headers["Access-Control-Allow-Headers"] = ','.join(["Accept", "Accept-Language", "Content-Language",
                                                                "Content-Type"])
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response


# noinspection PyTypeChecker
app.add_middleware(
    DynamicCORSMiddleware
)

# This lets us handle the session cookie for authentication purposes
# noinspection PyTypeChecker
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SIGNING_KEY"),
    session_cookie="session_id",
)


app.include_router(db.route)
app.include_router(auth.route)

@app.get("/search/{product_name}")
def search(product_name: str, request: Request):

    # This just checks if you're authenticated, as it can theoretically fail in several different spots
    cookie = request.cookies.get("session_id")
    token = auth.verify_session_cookie(cookie)
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    sub = token["sub"]
    if not sub:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if not db.get_user(sub):
        raise HTTPException(status_code=401, detail="Unauthorized")


    product = score.parse(product_name)


    # Product is missing id and name, so we add them here before pushing to the database
    product_uuid = str(uuid4())
    product["product_id"] = product_uuid
    product["product_name"] = product_name
    # check if product with same name already exists
    existing_product = db.fetch_product_by_name(product_name)
    if existing_product:
        product_uuid = existing_product["product_id"]
    else:
        db.push_item(product, "products")

    # We also need to update the user's seen products so we have it added to their history
    seen_products = db.seen_products(sub)
    if not seen_products:
        seen_products = []

    seen_products.append(product_uuid)
    db.update_seen_products(sub, seen_products)

    return product
