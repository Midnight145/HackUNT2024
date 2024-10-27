from uuid import uuid4

import fastapi

import score
from api import auth
from api import db

db.init()
app = fastapi.FastAPI()
from fastapi.responses import JSONResponse
from fastapi import Response, Request, HTTPException
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

SECRET_KEY = "supersecretkey"  # Use a strong, unique key in production


class DynamicCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(request.cookies)
        origin = request.headers.get("origin")
        if not origin:
            origin = "*"

        # Handle CORS for preflight requests
        if request.method == "OPTIONS":
            print("Handling preflight request")
            if True or origin in auth.allowed_origins:
                response = JSONResponse(content={"message": "Preflight request OK"})
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
                response.headers["Access-Control-Allow-Headers"] = ','.join(["Accept", "Accept-Language", "Content-Language",
                                                                    "Content-Type"])
                response.headers["Access-Control-Allow-Credentials"] = "true"
                return response
            else:
                return JSONResponse(status_code=403, content={"message": "Origin not allowed"})

        # Handle CORS for actual requests
        print("Handling actual request")
        response = await call_next(request)
        if True or origin in auth.allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE"
            response.headers["Access-Control-Allow-Headers"] = ','.join(["Accept", "Accept-Language", "Content-Language",
                                                                    "Content-Type"])
            response.headers["Access-Control-Allow-Credentials"] = "true"
        return response

app.add_middleware(
    DynamicCORSMiddleware
)
# Add session middleware to FastAPI
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie="session_id",  # Name of the session cookie
)


app.include_router(db.route)
app.include_router(auth.route)

@app.get("/search/{product_name}")
def search(product_name: str, request: Request, response: Response):
    cookie = request.cookies.get("session_id")
    print(cookie)
    token = auth.verify_session_cookie(cookie)
    if not token:
        print("No token")
        raise HTTPException(status_code=401, detail="Unauthorized")
    sub = token["sub"]
    if not sub:
        print("No sub")
        raise HTTPException(status_code=401, detail="Unauthorized")
    if not db.get_user(sub):
        print("No user")
        raise HTTPException(status_code=401, detail="Unauthorized")
    product = score.parse(product_name)

    product_uuid = str(uuid4())
    product["product_id"] = product_uuid
    product["product_name"] = product_name
    db.push_item(product, "products")
    seen_products = db.seen_products(sub)
    if not seen_products:
        seen_products = []

    seen_products.append(product_uuid)
    db.update_seen_products(sub, seen_products)

    return product
