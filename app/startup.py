import asyncio
import signal
import uvicorn
from fastapi import Cookie, FastAPI, HTTPException
from typing import List
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import routers
import login
import exception_handler

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
def root() -> str:
    return "good-kids-app"


def register_routers(app: FastAPI) -> None:
    app.include_router(login.router)
    app.include_router(routers.router)


def rigister_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(Exception, exception_handler.handle_exception)
    app.add_exception_handler(
        HTTPException, exception_handler.handle_exception)


async def shutdown() -> None:
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)


def shutdown_server(signum, frame) -> None:
    print(f"Received signal {signum}, shutting down server.")
    loop = asyncio.get_event_loop()
    loop.create_task(shutdown())


if __name__ == "__main__":
    register_routers(app)
    # rigister_exception_handlers(app)

    loop = asyncio.get_event_loop()
    signal.signal(signal.SIGINT, lambda signum,
                  frame: shutdown_server(signum, frame))
    signal.signal(signal.SIGTERM, lambda signum,
                  frame: shutdown_server(signum, frame))
    uvicorn.run(app, host="0.0.0.0", port=8000)
