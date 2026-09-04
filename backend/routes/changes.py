from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.models import (
    Watchlist,
    UserStockState,
    Preference,
    MarketSnapshot,
)
from services.market_data import get_market_data
from services.change_engine import analyze_stock


router = APIRouter(
    prefix="/api/watchlists",
    tags=["Changes"]
)

IST = ZoneInfo("Asia/Kolkata")


def calculate_volume_ratio(
    current_volume,
    symbol,
    db,
):
    if current_volume is None or current_volume <= 0:
        return None

    snapshots = (
        db.query(MarketSnapshot)
        .filter(
            MarketSnapshot.symbol == symbol,
            MarketSnapshot.volume.isnot(None),
            MarketSnapshot.volume > 0
        )
        .order_by(
            MarketSnapshot.timestamp.desc()
        )
        .limit(20)
        .all()
    )

    if len(snapshots) < 2:
        return None

    historical_volumes = [
        s.volume
        for s in snapshots[1:]
        if s.volume
    ]

    if not historical_volumes:
        return None

    average_volume = (
        sum(historical_volumes)
        / len(historical_volumes)
    )

    if average_volume <= 0:
        return None

    return round(
        current_volume / average_volume,
        2
    )


def generate_attention_message(
    change_percent,
    volume_ratio,
    status,
):
    if status == "HIGH":

        if (
            volume_ratio is not None
            and volume_ratio >= 1.5
            and abs(change_percent or 0) >= 3
        ):
            return (
                "Strong price movement combined "
                "with unusual trading activity."
            )

        if abs(change_percent or 0) >= 3:
            direction = (
                "up"
                if change_percent > 0
                else "down"
            )

            return (
                f"Price moved significantly {direction} "
                "since your last visit."
            )

        return (
            "Trading activity is significantly "
            "higher than usual."
        )

    if status == "MEDIUM":

        direction = (
            "up"
            if change_percent > 0
            else "down"
        )

        return (
            f"Moderate movement {direction} "
            "since your last visit."
        )

    if status == "NEW":
        return (
            "This is the first time PulseWatch "
            "is tracking this stock for you."
        )

    if status == "STALE":
        return (
            "Latest market data may be delayed. "
            "The displayed value is the most recent "
            "available data."
        )

    if status == "UNAVAILABLE":
        return (
            "Market data is currently unavailable."
        )

    return (
        "Movement is below your attention threshold."
    )


def is_stale(timestamp):

    if timestamp is None:
        return True

    now = datetime.now(timezone.utc)

    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(
            tzinfo=timezone.utc
        )

    timestamp_ist = timestamp.astimezone(IST)
    now_ist = now.astimezone(IST)

    if timestamp_ist > now_ist:
        return False

    if timestamp_ist.date() == now_ist.date():

        market_open = now_ist.replace(
            hour=9,
            minute=15,
            second=0,
            microsecond=0
        )

        market_close = now_ist.replace(
            hour=15,
            minute=30,
            second=0,
            microsecond=0
        )

        if now_ist < market_open:
            return True

        if now_ist >= market_close:
            return False

        age = now - timestamp

        return age > timedelta(minutes=15)

    return True


def get_latest_demo_snapshot(
    symbol,
    db,
):
    snapshot = (
        db.query(MarketSnapshot)
        .filter(
            MarketSnapshot.symbol == symbol,
            MarketSnapshot.source == "PulseWatch Demo"
        )
        .order_by(
            MarketSnapshot.timestamp.desc()
        )
        .first()
    )

    if not snapshot:
        return None

    age = (
        datetime.now(timezone.utc)
        - (
            snapshot.timestamp.replace(
                tzinfo=timezone.utc
            )
            if snapshot.timestamp.tzinfo is None
            else snapshot.timestamp
        )
    )

    # Demo mode remains active for 10 minutes.
    if age > timedelta(minutes=10):
        return None

    return {
        "symbol": snapshot.symbol,
        "price": snapshot.price,
        "volume": snapshot.volume,
        "timestamp": snapshot.timestamp,
        "source": snapshot.source,
    }


@router.get("/{watchlist_id}/changes")
def get_changes(
    watchlist_id: int,
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    watchlist = (
        db.query(Watchlist)
        .filter(
            Watchlist.id == watchlist_id,
            Watchlist.user_id == user_id
        )
        .first()
    )

    if not watchlist:
        raise HTTPException(
            status_code=404,
            detail="Watchlist not found"
        )

    preference = (
        db.query(Preference)
        .filter(
            Preference.user_id == user_id
        )
        .first()
    )

    price_threshold = (
        preference.price_threshold
        if preference
        else 3.0
    )

    volume_threshold = (
        preference.volume_threshold
        if preference
        else 1.5
    )

    changes = []

    for stock in watchlist.stocks:

        # Demo snapshot gets priority.
        market = get_latest_demo_snapshot(
            stock.symbol,
            db,
        )

        if not market:
            market = get_market_data(
                stock.symbol
            )

        if not market:

            changes.append({
                "symbol": stock.symbol,
                "company_name": stock.company_name,
                "current_price": None,
                "last_seen_price": None,
                "change_percent": None,
                "volume_ratio": None,
                "attention_score": 0,
                "price_multiple": 0,
                "status": "UNAVAILABLE",
                "reason": "Market data unavailable",
                "attention_message": (
                    "Market data is currently unavailable."
                ),
                "timestamp": None,
                "source": None,
            })

            continue

        if market["source"] != "PulseWatch Demo":

            snapshot = MarketSnapshot(
                symbol=stock.symbol,
                price=market["price"],
                volume=market.get("volume"),
                timestamp=market["timestamp"],
                source=market["source"],
            )

            db.add(snapshot)
            db.commit()

        volume_ratio = calculate_volume_ratio(
            market.get("volume"),
            stock.symbol,
            db,
        )

        state = (
            db.query(UserStockState)
            .filter(
                UserStockState.user_id == user_id,
                UserStockState.symbol == stock.symbol
            )
            .first()
        )

        if not state:

            changes.append({
                "symbol": stock.symbol,
                "company_name": stock.company_name,
                "current_price": market["price"],
                "last_seen_price": None,
                "change_percent": None,
                "volume_ratio": volume_ratio,
                "attention_score": 0,
                "price_multiple": 0,
                "status": "NEW",
                "reason": "First time viewing this stock",
                "attention_message": (
                    "This is the first time PulseWatch "
                    "is tracking this stock for you."
                ),
                "timestamp": market["timestamp"],
                "source": market["source"],
            })

            continue

        analysis = analyze_stock(
            state.last_seen_price,
            market["price"],
            volume_ratio=volume_ratio,
            price_threshold=price_threshold,
            volume_threshold=volume_threshold,
        )

        change_percent = analysis["change_percent"]
        status = analysis["status"]

        # Demo data is intentionally considered fresh.
        if (
            market["source"] != "PulseWatch Demo"
            and is_stale(market["timestamp"])
        ):
            status = "STALE"

        changes.append({
            "symbol": stock.symbol,
            "company_name": stock.company_name,
            "current_price": market["price"],
            "last_seen_price": state.last_seen_price,
            "change_percent": change_percent,
            "volume_ratio": volume_ratio,
            "attention_score": analysis["attention_score"],
            "price_multiple": analysis.get(
                "price_multiple",
                0
            ),
            "status": status,
            "reason": analysis["reason"],
            "attention_message": generate_attention_message(
                change_percent,
                volume_ratio,
                status,
            ),
            "last_seen_at": state.last_seen_at,
            "timestamp": market["timestamp"],
            "source": market["source"],
            "demo": (
                market["source"]
                == "PulseWatch Demo"
            ),
        })

    changes.sort(
        key=lambda x: x.get(
            "attention_score",
            0
        ),
        reverse=True,
    )

    return {
        "watchlist_id": watchlist.id,
        "watchlist_name": watchlist.name,
        "preferences": {
            "price_threshold": price_threshold,
            "volume_threshold": volume_threshold,
        },
        "changes": changes,
    }


@router.post("/{watchlist_id}/visit")
def record_visit(
    watchlist_id: int,
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    watchlist = (
        db.query(Watchlist)
        .filter(
            Watchlist.id == watchlist_id,
            Watchlist.user_id == user_id
        )
        .first()
    )

    if not watchlist:
        raise HTTPException(
            status_code=404,
            detail="Watchlist not found"
        )

    updated = []

    for stock in watchlist.stocks:

        market = get_market_data(
            stock.symbol
        )

        if not market:
            continue

        state = (
            db.query(UserStockState)
            .filter(
                UserStockState.user_id == user_id,
                UserStockState.symbol == stock.symbol
            )
            .first()
        )

        if state:

            state.last_seen_price = market["price"]
            state.last_seen_at = market["timestamp"]

        else:

            state = UserStockState(
                user_id=user_id,
                symbol=stock.symbol,
                last_seen_price=market["price"],
                last_seen_at=market["timestamp"],
            )

            db.add(state)

        updated.append(stock.symbol)

    db.commit()

    return {
        "message": "Visit recorded",
        "updated_stocks": updated,
    }