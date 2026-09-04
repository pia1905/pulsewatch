from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.models import (
    Watchlist,
    UserStockState,
    MarketSnapshot,
)


router = APIRouter(
    prefix="/api/demo",
    tags=["Demo"]
)


SCENARIOS = {
    "TCS": 0.94,
    "INFY": 1.045,
    "RELIANCE": 0.985,
    "HDFCBANK": 1.065,
    "ICICIBANK": 0.96,
}


@router.post("/simulate/{watchlist_id}/{symbol}")
def simulate_market_move(
    watchlist_id: int,
    symbol: str,
    db: Session = Depends(get_db),
):
    symbol = symbol.upper()

    stock = (
        db.query(Watchlist)
        .filter(
            Watchlist.id == watchlist_id,
            Watchlist.user_id == 1
        )
        .first()
    )

    if not stock:
        raise HTTPException(
            status_code=404,
            detail="Watchlist not found"
        )

    state = (
        db.query(UserStockState)
        .filter(
            UserStockState.user_id == 1,
            UserStockState.symbol == symbol
        )
        .first()
    )

    if not state:
        raise HTTPException(
            status_code=404,
            detail="Mark the watchlist as visited first."
        )

    multiplier = SCENARIOS.get(
        symbol,
        0.95
    )

    simulated_price = round(
        state.last_seen_price * multiplier,
        2
    )

    timestamp = datetime.now(timezone.utc)

    snapshot = MarketSnapshot(
        symbol=symbol,
        price=simulated_price,
        volume=None,
        timestamp=timestamp,
        source="PulseWatch Demo"
    )

    db.add(snapshot)
    db.commit()

    return {
        "demo": True,
        "symbol": symbol,
        "last_seen_price": state.last_seen_price,
        "simulated_price": simulated_price,
        "change_percent": round(
            (
                (
                    simulated_price
                    - state.last_seen_price
                )
                / state.last_seen_price
            ) * 100,
            2
        ),
        "timestamp": timestamp,
        "source": "PulseWatch Demo",
        "note": "DEMO DATA — simulated market movement"
    }