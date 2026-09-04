from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from models.models import (
    User,
    Watchlist,
    WatchlistStock,
    MarketSnapshot,
    UserStockState,
    Preference,
)

from routes.market import router as market_router
from routes.watchlist import router as watchlist_router
from routes.changes import router as changes_router
from routes.preferences import router as preferences_router
from routes.demo import router as demo_router


app = FastAPI(
    title="PulseWatch API",
    description="Smart market watchlist API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(market_router)
app.include_router(watchlist_router)
app.include_router(changes_router)
app.include_router(preferences_router)
app.include_router(demo_router)


Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "PulseWatch API is running!"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy"
    }