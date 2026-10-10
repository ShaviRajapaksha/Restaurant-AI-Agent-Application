from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import auth, restaurants, reservations, orders, conversations, agent
from app.agent.tools import register_all_tools


app = FastAPI(
    title="Restaurant AI Agent API",
    version="1.0.0",
    description="Backend for the Restaurant AI Agent application.",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


register_all_tools()


@app.on_event("startup")
def on_startup():
    pass


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(restaurants.router)
app.include_router(reservations.router)
app.include_router(orders.router)
app.include_router(conversations.router)
app.include_router(agent.router)