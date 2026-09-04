from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.models import User, Watchlist, WatchlistStock


router = APIRouter(
    prefix="/api/watchlists",
    tags=["Watchlists"]
)


@router.post("/")
def create_watchlist(
    name: str,
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    """
    Create a new watchlist for a user.
    """

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    watchlist = Watchlist(
        name=name,
        user_id=user_id
    )

    db.add(watchlist)
    db.commit()
    db.refresh(watchlist)

    return {
        "id": watchlist.id,
        "name": watchlist.name,
        "user_id": watchlist.user_id,
        "created_at": watchlist.created_at
    }


@router.get("/")
def get_watchlists(
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    """
    Get all watchlists belonging to a user.
    """

    watchlists = (
        db.query(Watchlist)
        .filter(Watchlist.user_id == user_id)
        .all()
    )

    return [
        {
            "id": watchlist.id,
            "name": watchlist.name,
            "user_id": watchlist.user_id,
            "created_at": watchlist.created_at
        }
        for watchlist in watchlists
    ]


@router.post("/{watchlist_id}/stocks")
def add_stock(
    watchlist_id: int,
    symbol: str,
    company_name: str,
    db: Session = Depends(get_db)
):
    """
    Add a stock to a watchlist.
    """

    watchlist = (
        db.query(Watchlist)
        .filter(Watchlist.id == watchlist_id)
        .first()
    )

    if not watchlist:
        raise HTTPException(
            status_code=404,
            detail="Watchlist not found"
        )

    symbol = symbol.upper()

    existing_stock = (
        db.query(WatchlistStock)
        .filter(
            WatchlistStock.watchlist_id == watchlist_id,
            WatchlistStock.symbol == symbol
        )
        .first()
    )

    if existing_stock:
        raise HTTPException(
            status_code=400,
            detail=f"{symbol} is already in this watchlist"
        )

    stock = WatchlistStock(
        watchlist_id=watchlist_id,
        symbol=symbol,
        company_name=company_name
    )

    db.add(stock)
    db.commit()
    db.refresh(stock)

    return {
        "message": "Stock added successfully",
        "id": stock.id,
        "symbol": stock.symbol,
        "company_name": stock.company_name,
        "watchlist_id": stock.watchlist_id
    }


@router.get("/{watchlist_id}/stocks")
def get_stocks(
    watchlist_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all stocks in a watchlist.
    """

    watchlist = (
        db.query(Watchlist)
        .filter(Watchlist.id == watchlist_id)
        .first()
    )

    if not watchlist:
        raise HTTPException(
            status_code=404,
            detail="Watchlist not found"
        )

    stocks = (
        db.query(WatchlistStock)
        .filter(WatchlistStock.watchlist_id == watchlist_id)
        .all()
    )

    return [
        {
            "id": stock.id,
            "symbol": stock.symbol,
            "company_name": stock.company_name,
            "added_at": stock.added_at
        }
        for stock in stocks
    ]


@router.delete("/{watchlist_id}/stocks/{symbol}")
def remove_stock(
    watchlist_id: int,
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    Remove a stock from a watchlist.
    """

    symbol = symbol.upper()

    stock = (
        db.query(WatchlistStock)
        .filter(
            WatchlistStock.watchlist_id == watchlist_id,
            WatchlistStock.symbol == symbol
        )
        .first()
    )

    if not stock:
        raise HTTPException(
            status_code=404,
            detail=f"{symbol} not found in watchlist"
        )

    db.delete(stock)
    db.commit()

    return {
        "message": f"{symbol} removed successfully"
    }