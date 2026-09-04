from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    watchlists = relationship("Watchlist", back_populates="user")


class Watchlist(Base):
    __tablename__ = "watchlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="watchlists")
    stocks = relationship(
        "WatchlistStock",
        back_populates="watchlist",
        cascade="all, delete-orphan"
    )


class WatchlistStock(Base):
    __tablename__ = "watchlist_stocks"

    id = Column(Integer, primary_key=True, index=True)
    watchlist_id = Column(Integer, ForeignKey("watchlists.id"), nullable=False)

    symbol = Column(String, nullable=False, index=True)
    company_name = Column(String, nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)

    watchlist = relationship("Watchlist", back_populates="stocks")


class MarketSnapshot(Base):
    __tablename__ = "market_snapshots"

    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False)
    volume = Column(Float, nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)
    source = Column(String, nullable=False)


class UserStockState(Base):
    __tablename__ = "user_stock_state"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(String, nullable=False, index=True)

    last_seen_price = Column(Float, nullable=False)
    last_seen_at = Column(DateTime, default=datetime.utcnow)


class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    price_threshold = Column(Float, default=3.0)
    volume_threshold = Column(Float, default=1.5)