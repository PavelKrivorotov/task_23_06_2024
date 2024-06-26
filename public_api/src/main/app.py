from fastapi import FastAPI

from memes.routers import router as memes_router


app = FastAPI()
app.include_router(memes_router, tags=['Memes'])

