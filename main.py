from fastapi import FastAPI

from routers.security.main import router as security
from routers.users.main import router as users
from routers.items.main import router as items

from database import engine
from routers.users import models as usersModels
from routers.items import models as itemsModels

usersModels.Base.metadata.create_all(bind=engine)
itemsModels.Base.metadata.create_all(bind=engine)

description = """
## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users.",
    },
    {
        "name": "items",
        "description": "Manage items",
        # "externalDocs": {
        #     "description": "Items external docs",
        #     "url": "https://fastapi.tiangolo.com/",
        # },
    },
]


app = FastAPI(
    title="Practice",
    description=description,
    summary="App for adding items to users.",
    version="0.0.1",
    # terms_of_service="http://example.com/terms/",
    contact={
        "name": "Mayokun Ajiboye",
        "url": "http://x-force.example.com/contact/",
        "email": "phynormynal@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata
)

# Depends(get_query_token)


app.include_router(security)
app.include_router(users, tags=["users"])
app.include_router(items, tags=["items"])


@app.get("/")
async def root():
    return {"message": "Hello! You can't do anything with this."}
