import os
from typing import Any

import dotenv
from auth0.authentication import Database, GetToken
from auth0.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier, TokenValidationError
from fastapi import APIRouter, Response, Request
from itsdangerous import URLSafeTimedSerializer
from pydantic import BaseModel

from api.db import push_item


class LoginModel(BaseModel):
    username: str
    password: str


dotenv.load_dotenv()
route = APIRouter()

AUTH0_DOMAIN = os.getenv("DOMAIN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SECRET_KEY = os.getenv("SIGNING_KEY")  # used for signing cookies

auth0 = Database(AUTH0_DOMAIN, client_id=CLIENT_ID)
get_token = GetToken(AUTH0_DOMAIN, client_id=os.getenv("CLIENT_ID"), client_secret=CLIENT_SECRET)

SIGNER = URLSafeTimedSerializer(SECRET_KEY)


def create_session_cookie(data: dict) -> str:
    """
    Utility to create a session cookie
    :param data: the data to store in the cookie
    :return: the signed cookie
    """
    return SIGNER.dumps(data)


# Utility to decode and verify a session cookie
def verify_session_cookie(cookie: str) -> dict | None:
    """
    Utility to verify and load session cookie
    :param cookie: the cookie to verify
    :return: the data stored in the cookie, None otherwise
    """
    # noinspection PyBroadException
    try:
        return SIGNER.loads(cookie, max_age=3600)  # Expires after 1 hour
    except Exception:
        return None


def login_with_username_password(username: str, password: str) -> Any:
    """
    Attempts to log in with a username and password
    :param username:
    :param password:
    :return: the response from the login attempt, otherwise None
    """
    try:
        response = get_token.login(
            username=username,
            password=password,
            realm='Username-Password-Authentication'
        )
        return response
    except Exception as e:
        print(f"Error during username/password login: {e}")
        return None


def register_username_password(email: str, password: str) -> dict[str, Any] | None:
    """
    Registers a new user with the given username and password
    :param email:
    :param password:
    :return: the user object if successful, otherwise None
    """
    try:
        user = auth0.signup(email=email, password=password, connection="Username-Password-Authentication")
        return user
    except Exception as e:
        print("Error during username/password registration:", e)
        return None

def verify_token(token) -> dict[str, Any] | None:
    """
    Verifies a JWT token
    :param token: the token to verify
    :return: the verified token if successful, otherwise None
    """
    jwks_url = 'https://{}/.well-known/jwks.json'.format(AUTH0_DOMAIN)
    issuer = 'https://{}/'.format(AUTH0_DOMAIN)
    sv = AsymmetricSignatureVerifier(jwks_url)
    tv = TokenVerifier(signature_verifier=sv, issuer=issuer, audience=CLIENT_ID)
    try:
        return tv.verify(token)
    except TokenValidationError:
        return None

def login_helper(login_data: LoginModel) -> str | None:
    """
    Helper function to log in a user and return their sub
    :param login_data:
    :return: the token sub if successful, otherwise None
    """
    auth_response = login_with_username_password(login_data.username, login_data.password)
    if auth_response:
        token = verify_token(auth_response["id_token"])
        if token:
            return token["sub"]
    return None

@route.post("/auth/login")
def login(login_data: LoginModel, resp: Response) -> dict:
    if sub := login_helper(login_data) is not None:
        resp.status_code = 200
        resp.set_cookie(
            "session_id",
            value=create_session_cookie({"sub": sub}),
            httponly=True,
            secure=True,
            samesite="none",
            path="/"
        )
        return {"message": "Login successful"}
    resp.status_code = 401
    return {"message": "Login failed"}

@route.post("/auth/register")
def register(login_data: LoginModel, resp: Response) -> dict:
    user = register_username_password(login_data.username, login_data.password)
    if user:  # registration successful, log in
        if sub := login_helper(login_data) is not None:
            resp.status_code = 200
            resp.set_cookie(
                "session_id",
                value=create_session_cookie({"sub": sub}),
                httponly=True,
                secure=True,
                samesite="lax",
                path="/"
            )

            # this is a new user, we need to add them to the database
            user_ = {
                "userid": sub,
                "username": user["nickname"],
                "email": user["email"],
                "seen_products": []
            }
            if push_item(user_, "users"):
                return {"message": "Login successful"}

    resp.status_code = 500
    return {"message": "Registration failed"}

@route.get("/auth/logout")
def logout(resp: Response) -> dict:
    resp.delete_cookie("session_id")
    return {"message": "Logged out"}


@route.get("/auth/verify")
def verify(resp: Response, request: Request) -> dict:
    cookie = request.cookies.get("session_id")
    token = verify_session_cookie(cookie)
    if token:
        resp.status_code = 200
        return {"message": "Session valid", "token": token}
    resp.status_code = 401
    return {"message": "Session invalid"}
