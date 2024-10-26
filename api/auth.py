import os
from typing import Optional

from fastapi import APIRouter, Response, Request, HTTPException
from itsdangerous import URLSafeTimedSerializer

from auth0.authentication import Database, GetToken
from auth0.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier, TokenValidationError
import dotenv
from api.models import Login

dotenv.load_dotenv()
route = APIRouter()

AUTH0_DOMAIN = os.getenv("DOMAIN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
auth0 = Database(AUTH0_DOMAIN, client_id=CLIENT_ID)
get_token = GetToken(AUTH0_DOMAIN, client_id=os.getenv("CLIENT_ID"), client_secret=CLIENT_SECRET)


# Secret key for signing cookies
SECRET_KEY = "supersecretkey"  # Use a strong, unique key in production
SIGNER = URLSafeTimedSerializer(SECRET_KEY)


def create_session_cookie(data: dict) -> str:
    return SIGNER.dumps(data)


# Utility to decode and verify a session cookie
def verify_session_cookie(cookie: str) -> Optional[dict]:
    try:
        return SIGNER.loads(cookie, max_age=3600)  # Expires after 1 hour
    except Exception:
        return None


def login_with_username_password(username, password):
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


def register_username_password(email, password):
    try:
        user = auth0.signup(email=email, password=password, connection="Username-Password-Authentication")
        return user
    except Exception as e:
        print("Error during username/password registration:", e)
        return None

def verify_login(auth_response):
    jwks_url = 'https://{}/.well-known/jwks.json'.format(AUTH0_DOMAIN)
    issuer = 'https://{}/'.format(AUTH0_DOMAIN)
    sv = AsymmetricSignatureVerifier(jwks_url)
    tv = TokenVerifier(signature_verifier=sv, issuer=issuer, audience=CLIENT_ID)
    try:
        token = tv.verify(auth_response["id_token"])
    except TokenValidationError as e:
        return None
    return token

@route.post("/auth/login")
def login(login_data: Login, resp: Response):
    auth_response = login_with_username_password(login_data.username, login_data.password)
    if auth_response:
        token = verify_login(auth_response)
        if token:
            resp.status_code = 200
            resp.set_cookie(
                "session_id",
                value=create_session_cookie({"sub": token["sub"]}),
                httponly=True,
                secure=True,
                samesite="lax",
                path="/"
            )
            return {"message": "Login successful", "token": token}
    resp.status_code = 401
    return {"message": "Login failed"}

@route.get("/verify-cookie")
async def verify_cookie(request: Request):
    print(request.cookies)
    user_id = request.cookies.get("session_id")

    if user_id is None:
        return {"message": "No valid session found"}

    return {"message": "Session is valid", "user_id": user_id}


@route.post("/auth/register")
def register(login_data: Login, resp: Response):
    user = register_username_password(login_data.username, login_data.password)
    if user:
        resp.status_code = 200
        return {"message": "Registration successful", "user": user}
    resp.status_code = 500
    return {"message": "Registration failed"}

@route.get("/auth/logout")
def logout(resp: Response):
    resp.delete_cookie("session_id")
    return {"message": "Logged out"}