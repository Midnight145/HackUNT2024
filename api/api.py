import os

import fastapi
from api import db
from api import auth
from dotenv import load_dotenv



load_dotenv()


print(os.getenv("DOMAIN"), os.getenv("CLIENT_ID"))

# Replace these with your actual Auth0 credentials
AUTH0_DOMAIN = os.getenv("DOMAIN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")



if __name__ == "__main__":
    db.init()
    username = "rubikscubeboy27@gmail.com"
    password = "jQ8LiX7zvlmi4OIx"
    auth_response = login_with_username_password(username, password)
    if auth_response:
        print("Login successful:", auth_response)
        domain = AUTH0_DOMAIN
        jwks_url = 'https://{}/.well-known/jwks.json'.format(domain)
        issuer = 'https://{}/'.format(domain)
        sv = AsymmetricSignatureVerifier(jwks_url)
        tv = TokenVerifier(signature_verifier=sv, issuer=issuer, audience=CLIENT_ID)
        token = tv.verify(auth_response["id_token"])
        print("Token verified:", token)
        print(token["sub"])
        user = db.create_user_row(token["sub"], token["nickname"], token["name"])
        db.push_user(user)
    else:
        print("Login failed.")
