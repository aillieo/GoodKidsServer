import asyncio
import signal
from fastapi.responses import JSONResponse
import uvicorn
from fastapi import Cookie, FastAPI, Request
from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import depends
import models
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import routers
import schemas
import security

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


@app.get("/")
def root():
    return "good-kids-app"


@app.post("/login")
async def login(request: Request, session: Session = Depends(depends.get_session)) -> schemas.Token:
    data = await request.json()
    name = data.get("name")
    password = data.get("password")

    user = session.query(models.User).filter(
        models.User.name == name, models.User.password == password).first()
    if user:
        token = schemas.Token(
            token=security.create_token(user.id), uid=user.id)
        return token
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


def register_routers(app):
    app.include_router(routers.router)


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
