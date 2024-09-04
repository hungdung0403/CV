from fastapi import FastAPI

from api.api_v1.routes.routes import router

app = FastAPI()
app.include_router(router)
