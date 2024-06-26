from fastapi import FastAPI

from meme_images.routers import router as minio_router


app = FastAPI()
app.include_router(minio_router, tags=['Minio'])

