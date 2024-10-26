import os

from fastapi import APIRouter, Response

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
            return {"message": "Login successful", "token": token}
    resp.status_code = 401
    return {"message": "Login failed"}


@route.post("/auth/register")
def register(login_data: Login, resp: Response):
    user = register_username_password(login_data.username, login_data.password)
    if user:
        resp.status_code = 200
        return {"message": "Registration successful", "user": user}
    resp.status_code = 500
    return {"message": "Registration failed"}

@route.post("/auth/logout")
def logout():
    return {"message": "Logged out"}