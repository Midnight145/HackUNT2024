import fastapi

from api import auth
from api import db
import score

db.init()
app = fastapi.FastAPI()
app.include_router(db.route)
app.include_router(auth.route)

@app.get("/search/{product}")
def search(product: str):
    return score.parse(product)