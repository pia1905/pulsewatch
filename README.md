# PulseWatch 📈

### Attention-first smart market watchlist

> **PulseWatch remembers what you last saw, detects meaningful market changes, and explains why a stock deserves your attention.**

PulseWatch is an end-to-end smart market watchlist built for the **Code, by Groww 2026** engineering challenge.

Instead of showing users only today's market movement, PulseWatch compares the latest available price with the **price the user saw during their previous visit**. This creates a personalized "Since Your Last Visit" view and helps users focus on stocks that actually changed.

---

## 🚀 Problem

Traditional watchlists show the latest price and daily percentage change, but they do not answer a simple question:

> **"What changed since I last checked?"**

Users may return after several hours or days and have to manually scan every stock to understand what deserves attention.

PulseWatch solves this by maintaining a lightweight per-user state and automatically identifying meaningful changes.

---

## 💡 Solution

PulseWatch combines:

- Persistent watchlists
- Latest available market data
- User-specific last-seen prices
- Personalized attention thresholds
- Price movement classification
- Volume-based signals
- Attention scores
- Human-readable explanations
- Stale-data handling
- API failure handling
- Demo market simulations

The dashboard prioritizes **attention over information overload**.

---

## ✨ Key Features

### 1. Smart Watchlist

Users can:

- Create a watchlist
- Add stocks
- Remove stocks
- View their tracked stocks
- Persist their watchlist across sessions

Example:

```text
YOUR WATCHLIST

TCS          ₹3,950
INFOSYS      ₹1,532
RELIANCE     ₹1,421
HDFC BANK    ₹1,721