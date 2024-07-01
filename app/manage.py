import uvicorn
from fastapi import FastAPI
from .db import engine
from .models import Base
from .auth.login import auth_router
from .view.fetch import get_router
from .view.create import post_router
from .view.update import put_router
from .view.delete import delete_router
from .view.custom_queries import custom_query_router


Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(auth_router)
app.include_router(get_router)
app.include_router(post_router)
app.include_router(put_router)
app.include_router(delete_router)
app.include_router(custom_query_router)


if __name__ == "__main__":
    uvicorn.run("app.manage:app", host="localhost", port=5001, reload=True)
