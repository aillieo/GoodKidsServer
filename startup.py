import asyncio
import signal
from fastapi.responses import JSONResponse
import uvicorn
from fastapi import Cookie, FastAPI, Request
import importlib
import os
from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import depends
import models
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()

# CORS support
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:7456",
        "http://127.0.0.1:7456",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def root():
    return "good-kids-app"

@app.post("/login")
async def login(request: Request, session: Session = Depends(depends.get_session)):
    print(request)
    print(request.body)
    data = await request.json()
    print(data)
    name = data.get("name")
    password = data.get("password")

    user = session.query(models.User).filter(models.User.name == name, models.User.password == password).first()
    if user:
        response = JSONResponse({"user" : user.id})
        response.set_cookie(key="user", value=user.id)
        return response
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

def register_routers(app):
    folder_name = "routers"
    router_files = [f for f in os.listdir(folder_name) if f.endswith(".py")]

    for router_file in router_files:
        module_name = f"{folder_name}.{router_file.rpartition('.')[0]}"
        module = importlib.import_module(module_name)
        app.include_router(module.router)


async def shutdown():
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)


def shutdown_server(signum, frame):
    print(f"Received signal {signum}, shutting down server.")
    loop = asyncio.get_event_loop()
    loop.create_task(shutdown())


if __name__ == "__main__":
    register_routers(app)

    loop = asyncio.get_event_loop()
    signal.signal(signal.SIGINT, lambda signum,
                  frame: shutdown_server(signum, frame))
    signal.signal(signal.SIGTERM, lambda signum,
                  frame: shutdown_server(signum, frame))
    uvicorn.run(app, host="0.0.0.0", port=8000)
