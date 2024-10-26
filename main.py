import fastapi

from api import auth
from api import db
import score

db.init()
app = fastapi.FastAPI()

from fastapi import FastAPI, Depends, Response, Request, HTTPException
from starlette.middleware.sessions import SessionMiddleware
from typing import Optional
SECRET_KEY = "supersecretkey"  # Use a strong, unique key in production


# Add session middleware to FastAPI
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie="session_id",  # Name of the session cookie
)


app.include_router(db.route)
app.include_router(auth.route)

@app.get("/search/{product}")
def search(product: str, request: Request):
    if not auth.verify_cookie(request):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return score.parse(product)