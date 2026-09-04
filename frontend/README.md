# PulseWatch

### Know what changed. Know what matters.

PulseWatch is an attention-first smart market watchlist that remembers what a user last saw, detects meaningful changes, and explains why a stock deserves attention.

## Problem

Traditional watchlists show prices, but users still have to scan every stock to understand what actually matters.

PulseWatch solves this by comparing the current market state with the user's last-seen state and ranking stocks by attention.

## Key Features

- Create and manage a personal watchlist
- View latest available market prices
- Persist user's last-seen stock prices
- Detect meaningful price movements
- Detect unusual volume when available
- Personalized attention thresholds
- Explainable Attention Score from 0–100
- "Why this matters" explanation for every flagged stock
- Stale-data detection
- API failure fallback
- Clearly labelled demo mode for reliable demonstrations

## How It Works

1. User adds stocks to the watchlist.
2. PulseWatch fetches the latest available market data.
3. The system compares the current price with the user's last-seen price.
4. Price and volume signals are evaluated against personalized thresholds.
5. Each stock receives an attention score.
6. Stocks are ranked from highest to lowest attention.
7. The user can inspect why a stock was flagged.

## Change Classification

| Condition | Status |
|---|---|
| Below threshold | Stable |
| Moderate movement | Medium |
| Significant movement | High |
| Delayed data | Stale |
| Data unavailable | Unavailable |

## Architecture

Frontend:
- React
- Vite
- Axios
- React Router
- Lucide Icons

Backend:
- FastAPI
- SQLAlchemy
- SQLite
- REST APIs

Market Data:
- Yahoo Finance / Finnhub
- Source and timestamp displayed with market values

## Database Design

The system separates shared market information from user-specific state.

Main entities:

- Users
- Watchlists
- Watchlist Stocks
- Market Snapshots
- User Stock State
- Preferences

This allows market data to be reused while keeping each user's last-seen state and attention preferences personalized.

## Running Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
python seed.py
python -m uvicorn main:app --reload