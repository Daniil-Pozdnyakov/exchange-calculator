from fastapi import FastAPI
import uvicorn
import models
import routers
from db import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(routers.router)
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
