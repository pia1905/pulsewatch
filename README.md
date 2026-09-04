PulseWatch 📈
Attention-first smart market watchlist

PulseWatch remembers what you last saw, detects meaningful market changes, and explains why a stock deserves your attention.

PulseWatch is an end-to-end smart market watchlist built for the Code, by Groww 2026 engineering challenge.

Traditional watchlists tell users what the market looks like right now. PulseWatch focuses on a more useful question:

"What meaningfully changed since I last checked?"

Instead of relying only on daily percentage change, PulseWatch stores the user's last-seen state and compares it with the latest available market information. It then prioritizes stocks based on the magnitude of the change and provides an explanation for why a stock deserves attention.

🚨 Problem

A conventional market watchlist can contain dozens of stocks, but users often have to manually scan every stock to determine:

What changed since their last visit?
Which movement is actually meaningful?
Which stock deserves attention first?
Is the movement significant relative to their own preferences?
Is the displayed market data fresh?

Daily percentage change alone does not answer these questions.

For example:

Yesterday / Last Visit

TCS          ₹4,000
INFOSYS      ₹1,500
RELIANCE     ₹1,400

When the user returns:

TCS          ₹3,760
INFOSYS      ₹1,525
RELIANCE     ₹1,415

A normal watchlist shows the current values.

PulseWatch instead highlights:

🔴 TCS

₹3,760 ↓ 6%

Your last seen price: ₹4,000

Price moved significantly down
since your last visit.

This reduces the amount of information the user needs to process.

💡 Our Solution

PulseWatch introduces an attention-first layer on top of a traditional watchlist.

The system:

Stores the user's watchlist.
Fetches the latest available market data.
Stores the user's last-seen price for each stock.
Compares the current price against that personalized baseline.
Evaluates price and volume movement.
Calculates an attention score.
Classifies the stock as STABLE, MEDIUM, or HIGH.
Explains why the stock was highlighted.
Handles stale or unavailable market data explicitly.

The result is a dashboard focused on:

What changed → How meaningful is it → Why should I care?

⭐ What Makes PulseWatch Different?

The core idea is the personalized comparison baseline.

Most watchlists focus on:

Current Price
+
Today's Change

PulseWatch focuses on:

Current Price
        ↓
Compare with
        ↓
User's Last-Seen Price
        ↓
Meaningful Change
        ↓
Attention Score
        ↓
Explanation

✨ Key Features
1. Smart Watchlist

Users can:

Create a watchlist
Add stocks
Remove stocks
View tracked stocks
Persist watchlist information

Example:

YOUR WATCHLIST

TCS             ₹3,950
INFOSYS         ₹1,532
RELIANCE        ₹1,421
HDFC BANK       ₹1,721

2. Since Your Last Visit

PulseWatch stores the last price seen by the user.

When the user returns, the system calculates:

Change % =
(Current Price - Last Seen Price)
-------------------------------- × 100
        Last Seen Price

Example:

Last seen price: ₹899
Current price:   ₹850

Change: -5.45%

The dashboard then identifies this as a significant movement.

3. Meaningful Change Detection

We deliberately chose a simple and explainable rule-based system.

Default price threshold:

< 1.5%       → STABLE
1.5% - <3%   → MEDIUM
≥ 3%          → HIGH

A significant volume movement can also trigger a HIGH attention state.

Default volume threshold:

Current Volume / Recent Average Volume ≥ 1.5×

This allows the system to detect both:

Significant price movement
Unusual trading activity

🎯 Personalized Attention Thresholds

Different users may have different definitions of "meaningful".

PulseWatch therefore allows users to configure:

Price movement threshold
Volume movement threshold

For example:

User A

Price threshold: 3%
Volume threshold: 1.5×

Another user could choose:
Another user could choose:

User B

Price threshold: 2%
Volume threshold: 1.5×

The same stock movement can therefore receive different attention levels depending on the user's preferences.
📊 Attention Score

Every stock receives an attention score between:

0 ─────────────────── 100
Low                  High

The score considers:

Magnitude of price movement
User's price threshold
Unusual volume
How strongly the movement exceeds the user's threshold

The dashboard sorts stocks by attention score so that the most important changes appear first.

🧠 Explainable Change Engine

PulseWatch does not simply show:

🔴 HIGH

It also explains why.

Examples:

Price moved 5.4% down since your last visit.

or:

Strong price movement combined with unusual
trading activity.

This makes the system deterministic and explainable.

❓ Why Am I Seeing This?

Each meaningful change can be explained to the user.

For example:

TCS

₹3,760 ↓ 6%

HIGH ATTENTION

Why am I seeing this?

Price moved significantly down
since your last visit.

The goal is to avoid making the attention system feel like a black box.

🕒 Stale Data Handling

Market data may be delayed or temporarily unavailable.

PulseWatch therefore stores:

Market timestamp
Data source
Latest available value

The system checks whether data may be stale and explicitly communicates that state.

Example:

⚠ Data may be delayed

Latest available data:
15 minutes ago

The application does not present delayed information as guaranteed real-time data.

🛡️ Failure Handling

PulseWatch considers several real-world scenarios.

Scenario	Behaviour
First time tracking a stock	NEW
Small movement	STABLE
Moderate movement	MEDIUM
Significant movement	HIGH
Delayed data	STALE
No market data	UNAVAILABLE
Duplicate stock	Prevented
Invalid threshold	API validation
Market API failure	Graceful unavailable/fallback state
Unpredictable demo movement	Controlled demo mode
🎬 Demo Mode

A live market can change unpredictably during a presentation.

To make the product behaviour deterministic, PulseWatch includes a controlled demo mode.

Example:

TCS

Last seen:
₹4,000

Simulated movement:
-6%

Current:
₹3,760

🔴 HIGH ATTENTION

The simulated data is explicitly labelled as demo data.

This allows the complete product flow to be demonstrated reliably without pretending that simulated values are real market data.

🏗️ System Architecture
                         USER
                           │
                           ▼
                 ┌──────────────────┐
                 │   React + Vite   │
                 │    Frontend      │
                 └────────┬─────────┘
                          │
                       REST API
                          │
                          ▼
                 ┌──────────────────┐
                 │     FastAPI      │
                 │     Backend      │
                 └────────┬─────────┘
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
   ┌────────────┐  ┌──────────────┐  ┌────────────┐
   │ Watchlist  │  │ Change Engine│  │ Preferences│
   │ Management │  │              │  │            │
   └────────────┘  └──────┬───────┘  └────────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │  Market Data     │
                 │    Service       │
                 └────────┬─────────┘
                          │
                 ┌────────┴────────┐
                 │                 │
                 ▼                 ▼
          ┌──────────────┐  ┌──────────────┐
          │ Market Data  │  │ PulseWatch   │
          │ Provider     │  │ Demo Data    │
          └──────────────┘  └──────────────┘

                          │
                          ▼
                 ┌──────────────────┐
                 │      SQLite      │
                 │     Database     │
                 └──────────────────┘
🛠️ Tech Stack
Frontend
React
Vite
JavaScript
Axios
Lucide React
CSS
Backend
Python
FastAPI
SQLAlchemy
REST APIs
Database
SQLite
Authentication
Google OAuth
@react-oauth/google
Market Data
Yahoo Finance
PulseWatch controlled demo data
🗄️ Database Design

PulseWatch separates shared market information from user-specific state.

User
id
name
email
created_at
Watchlist
id
user_id
name
created_at
WatchlistStock
id
watchlist_id
symbol
company_name
added_at
MarketSnapshot
id
symbol
price
volume
timestamp
source
UserStockState
id
user_id
symbol
last_seen_price
last_seen_at
Preference
id
user_id
price_threshold
volume_threshold
🔄 Core User Flow
Google Login
     │
     ▼
Open Watchlist
     │
     ▼
Fetch Latest Market Data
     │
     ▼
Retrieve User's Last-Seen State
     │
     ▼
Calculate Price Movement
     │
     ▼
Evaluate Volume Signal
     │
     ▼
Calculate Attention Score
     │
     ▼
Classify Change
     │
     ├──── STABLE
     ├──── MEDIUM
     └──── HIGH
     │
     ▼
Explain Why
     │
     ▼
User Reviews Changes
     │
     ▼
Record Visit
     │
     ▼
Current State Becomes New Baseline
🔐 Authentication

PulseWatch supports Google login using Google OAuth.

For the current MVP, authentication is implemented on the frontend and the application maintains a simplified user mapping.

A production deployment would additionally perform:

Server-side Google ID-token verification
Secure session/JWT management
Proper user creation and lookup
Per-user authorization on every protected API endpoint

The current implementation keeps authentication lightweight so the core watchlist and market-change problem remains the focus of the MVP.

📁 Project Structure
pulsewatch/
│
├── backend/
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── changes.py
│   │   ├── demo.py
│   │   ├── market.py
│   │   ├── preferences.py
│   │   └── watchlist.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── change_engine.py
│   │   └── market_data.py
│   │
│   ├── database.py
│   ├── main.py
│   └── seed.py
│
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
⚙️ Local Setup
Prerequisites

Install:

Python 3.10+
Node.js
npm
Git
1. Clone Repository
git clone https://github.com/pia1905/pulsewatch.git
cd pulsewatch
2. Backend Setup

Open a terminal:

cd backend

Create a virtual environment:

python -m venv venv

Activate it:

venv\Scripts\activate

Install dependencies:

pip install fastapi uvicorn sqlalchemy requests python-dotenv

Create the initial demo user:

python seed.py

Start the backend:

uvicorn main:app --reload

Backend:

http://localhost:8000

API documentation:

http://localhost:8000/docs
3. Frontend Setup

Open a second terminal:

cd frontend

Install dependencies:

npm install

Create:

frontend/.env

Add:

VITE_GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID

Start the frontend:

npm run dev

Frontend:

http://localhost:5173
🔑 Google OAuth Setup

Create a Google OAuth Web Application client.

Add the following as an authorized JavaScript origin:

http://localhost:5173

Then add your client ID to:

frontend/.env

Example:

VITE_GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
Important

Do not commit .env files to GitHub.

🧪 Running the Application

Once both servers are running:

Terminal 1
cd backend
venv\Scripts\activate
uvicorn main:app --reload
Terminal 2
cd frontend
npm run dev

Open:

http://localhost:5173
🎥 Recommended Demo Flow

For evaluation, the following flow demonstrates the core idea clearly.

Step 1 — Login

Login using Google.

Step 2 — Open Watchlist

Show the tracked stocks and latest market values.

Step 3 — Establish Baseline

Record the current visit.

PulseWatch now knows:

"What the user last saw"
Step 4 — Simulate Market Movement

Use Demo Mode to simulate a significant movement.

Step 5 — Return / Refresh

PulseWatch compares:

Last Seen Price
        ↓
Current Price
Step 6 — Show Attention

The stock appears under:

SINCE YOUR LAST VISIT

with a HIGH/MEDIUM/STABLE classification.

Step 7 — Explain

Open:

Why am I seeing this?
Step 8 — Personalize

Change the user's attention threshold and demonstrate how the classification changes.

🖼️ Screenshots

Screenshots can be added here to make the project easier to understand without running it.

Recommended screenshots:

1. Login
![PulseWatch Login](docs/screenshots/login.png)
2. Dashboard
![PulseWatch Dashboard](docs/screenshots/dashboard.png)
3. Since Your Last Visit
![Market Changes](docs/screenshots/changes.png)
4. Why Am I Seeing This?
![Change Explanation](docs/screenshots/explanation.png)
5. Settings
![Settings](docs/screenshots/settings.png)
6. Demo Mode
![Demo Mode](docs/screenshots/demo.png)
Recommended folder structure

Create:

docs/
└── screenshots/
    ├── login.png
    ├── dashboard.png
    ├── changes.png
    ├── explanation.png
    ├── settings.png
    └── demo.png

You don't need all six. Even 3–4 strong screenshots are enough.

🧩 Engineering Decisions & Trade-offs
Why compare against the last-seen price?

Daily change is based on a fixed market reference point.

It does not necessarily represent what changed since the user personally checked.

Using last-seen state makes the product contextual to the user.

Why deterministic rules?

The problem involves numerical signals such as:

Percentage change
Volume ratios
Thresholds

A deterministic system provides:

Predictable behaviour
Explainability
Low latency
Easy testing
No dependency on an external AI model

An LLM would add complexity without being necessary for the core decision.

Why SQLite?

SQLite keeps the MVP:

Simple
Lightweight
Easy to run
Easy to demonstrate

The database schema is structured so it can later migrate to PostgreSQL.

Why separate MarketSnapshot and UserStockState?

Market information is shared across users.

Last-seen state is user-specific.

Separating them avoids storing the same market information repeatedly for every user.

Conceptually:

                    MarketSnapshot
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
       User A          User B         User C
    last-seen state  last-seen state last-seen state
📈 Scalability

The MVP intentionally avoids unnecessary infrastructure.

For a larger deployment:

SQLite
   ↓
PostgreSQL

Direct market API calls
   ↓
Market Data Service
   ↓
Redis / Cache

Synchronous refresh
   ↓
Background Workers

Single API instance
   ↓
Horizontally scalable backend

Market data can be cached because the same stock may be present in many users' watchlists.

User-specific last-seen state remains separate.

This provides a natural scaling path without over-engineering the MVP.

🛡️ Reliability Considerations

The system is designed around the principle:

Never present uncertain data as certain.

PulseWatch tracks:

Data source
Timestamp
Data availability
User's previous state

This allows the UI to distinguish between:

Fresh data
Stale data
Unavailable data
Demo data
🔮 Future Improvements

Potential production improvements include:

Server-side Google token verification
Secure authentication/session management
PostgreSQL
Redis caching
Background market-data refresh
Multiple watchlists
Historical price charts
More market-data providers
WebSocket/live updates
Push notifications
Advanced anomaly detection
Sector-level attention
Market-wide attention ranking

These are deliberately outside the MVP so that the core product remains simple and reliable.

🎯 Product Philosophy

PulseWatch is built around one principle:

Don't make users scan the market. Tell them what changed.

The product is not intended to replace a trading terminal.

It focuses on one useful question:

"What deserves my attention now?"
📝 100-Word Product Pitch

PulseWatch is an attention-first smart market watchlist that answers a question traditional watchlists miss: what meaningfully changed since I last checked? Instead of relying only on daily movement, PulseWatch stores each user's last-seen stock state and compares it with the latest available market data. A deterministic change engine combines personalized price thresholds and unusual volume to classify movements and generate an attention score. The dashboard prioritizes important changes and explains why each stock is highlighted. We deliberately kept the architecture simple with FastAPI, React, SQLAlchemy and SQLite while designing clear paths toward PostgreSQL, caching and background processing.

🏆 Built For

Code, by Groww — 2026

Challenge

Build a Smart Market Watchlist

Project

PulseWatch

Focus

Personalized market change detection and attention prioritization

👩‍💻 Team

Built as a solo engineering project for the Code, by Groww 2026 challenge.

📌 Final Note

PulseWatch is intentionally not just another watchlist.

The product decision is simple:

Traditional Watchlist
        ↓
"What is the market doing?"

PulseWatch
        ↓
"What changed for me?"
        ↓
"What deserves my attention?"
        ↓
"Why?"

That is the problem PulseWatch is designed to solve.


## 📸 About the screenshots

**Yes, absolutely add screenshots.** For this particular challenge, I'd put them fairly high in the README, because a judge can understand the product in 30 seconds without cloning it.

I'd take these **4 screenshots from your existing app**:

1. **Login page** — shows Google authentication + product branding
2. **Main dashboard** — shows the overall PulseWatch experience
3. **"Since Your Last Visit" with a HIGH stock** — this is your most important screenshot
4. **"Why am I seeing this?" modal + Settings** — demonstrates explainability and personalization

Don't take screenshots of code or Swagger unless there's a specific reason.

### One important correction before you paste this

Your current project uses the actual market-data implementation we've built, so **don't blindly add any dependency that isn't actually in your `package.json` or backend environment** just because it's mentioned in a README. The README should describe what works in the repo.

Also, since you've already pushed the repository, after replacing the README:

```powershell
git add README.md
git commit -m "Improve project documentation"
git push

