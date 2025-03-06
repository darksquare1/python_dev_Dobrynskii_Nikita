from fastapi import FastAPI
from app.routes.api import router

app = FastAPI()

app.include_router(router, prefix='/api', tags=['api'])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
