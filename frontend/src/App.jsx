import { useEffect, useState } from "react";
import { GoogleLogin } from "@react-oauth/google";
import axios from "axios";
import {
  TrendingUp,
  TrendingDown,
  RefreshCw,
  Plus,
  Trash2,
  Activity,
  Clock3,
  Settings,
  X,
  Save,
  Zap,
  Brain,
  Sparkles,
  ChevronRight,
  ArrowRight,
  ShieldCheck,
  Eye,
  EyeOff,
  LogOut,
  User,
  LockKeyhole,
  CheckCircle2,
} from "lucide-react";
import "./App.css";

const API = "http://localhost:8000";
const WATCHLIST_ID = 1;

function LoginPage({ onLogin }) {
  const [email, setEmail] = useState("demo@pulsewatch.com");
  const [password, setPassword] = useState("pulsewatch");
  const [showPassword, setShowPassword] = useState(false);
  const [loggingIn, setLoggingIn] = useState(false);
  const [loginError, setLoginError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    if (!email.trim() || !password.trim()) {
      setLoginError("Please enter your email and password.");
      return;
    }

    try {
      setLoggingIn(true);
      setLoginError("");

      await new Promise((resolve) => setTimeout(resolve, 650));

      const session = {
        userId: 1,
        name: "Demo User",
        email: email.trim(),
      };

      localStorage.setItem(
        "pulsewatch_session",
        JSON.stringify(session)
      );

      onLogin(session);
    } catch (err) {
      console.error(err);
      setLoginError("Unable to sign in. Please try again.");
    } finally {
      setLoggingIn(false);
    }
  };

  const continueDemo = () => {
    const session = {
      userId: 1,
      name: "Demo User",
      email: "demo@pulsewatch.com",
    };

    setEmail(session.email);
    setPassword("pulsewatch");

    localStorage.setItem(
      "pulsewatch_session",
      JSON.stringify(session)
    );

    onLogin(session);
  };

  return (
    <div className="login-page">
      <div className="login-grid">
        <section className="login-brand-panel">
          <div className="login-brand">
            <div className="login-brand-icon">
              <Activity size={24} />
            </div>

            <span>PulseWatch</span>
          </div>

          <div className="login-message">
            <div className="login-kicker">
              <Sparkles size={14} />
              PERSONALIZED MARKET INTELLIGENCE
            </div>

            <h1>
              Know what changed.
              <br />
              <span>Know what matters.</span>
            </h1>

            <p>
              A smarter watchlist that remembers what you last saw
              and surfaces the market movements that deserve your
              attention.
            </p>

            <div className="login-features">
              <div>
                <CheckCircle2 size={17} />
                <span>Last-seen price tracking</span>
              </div>

              <div>
                <CheckCircle2 size={17} />
                <span>Explainable attention scoring</span>
              </div>

              <div>
                <CheckCircle2 size={17} />
                <span>Transparent market data</span>
              </div>
            </div>
          </div>

          <div className="login-footer">
            <span>Built for smarter market awareness</span>
            <span>© 2026 PulseWatch</span>
          </div>
        </section>

        <section className="login-form-panel">
          <div className="login-card">
            <div className="mobile-brand">
              <div className="login-brand-icon">
                <Activity size={22} />
              </div>
              PulseWatch
            </div>

            <div className="login-heading">
              <div className="login-icon">
                <LockKeyhole size={19} />
              </div>

              <h2>Welcome back</h2>

              <p>
                Sign in to continue to your market pulse.
              </p>
            </div>

            <form onSubmit={handleLogin}>
              <label>Email address</label>

              <div className="input-wrapper">
                <User size={17} />

                <input
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>

              <label>Password</label>

              <div className="input-wrapper">
                <LockKeyhole size={17} />

                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() =>
                    setShowPassword(!showPassword)
                  }
                >
                  {showPassword ? (
                    <EyeOff size={16} />
                  ) : (
                    <Eye size={16} />
                  )}
                </button>
              </div>

              {loginError && (
                <div className="login-error">
                  {loginError}
                </div>
              )}

              <button
                className="login-submit"
                type="submit"
                disabled={loggingIn}
              >
                {loggingIn ? "Signing in..." : "Sign in"}

                {!loggingIn && <ArrowRight size={17} />}
              </button>
            </form>

            <div className="google-login">
  <GoogleLogin
    onSuccess={(credentialResponse) => {
      try {
        const credential = credentialResponse?.credential;

        if (!credential) {
          setLoginError("Google sign-in failed. Please try again.");
          return;
        }

        const payload = JSON.parse(
          atob(
            credential
              .split(".")[1]
              .replace(/-/g, "+")
              .replace(/_/g, "/")
          )
        );

        const session = {
          userId: 1,
          name: payload.name || "Google User",
          email: payload.email || "",
          picture: payload.picture || "",
          provider: "google",
        };

        localStorage.setItem(
          "pulsewatch_session",
          JSON.stringify(session)
        );

        onLogin(session);
      } catch (err) {
        console.error(err);
        setLoginError("Unable to complete Google sign-in.");
      }
    }}
    onError={() => {
      setLoginError("Google sign-in failed. Please try again.");
    }}
    useOneTap={false}
    theme="outline"
    size="large"
    width="100%"
    text="continue_with"
    shape="rectangular"
  />
</div>

            <div className="login-divider">
              <span>or</span>
            </div>

            <button
              className="demo-login"
              onClick={continueDemo}
            >
              <Sparkles size={16} />
              Continue as Demo User
            </button>

            <div className="demo-account">
              <div>
                <ShieldCheck size={15} />
                <span>Demo environment</span>
              </div>

              <small>
                No real trading or financial actions are performed.
              </small>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

function App() {
  const [user, setUser] = useState(null);

  const [stocks, setStocks] = useState([]);
  const [changes, setChanges] = useState([]);

  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [savingSettings, setSavingSettings] = useState(false);
  const [demoRunning, setDemoRunning] = useState(false);

  const [error, setError] = useState("");

  const [symbol, setSymbol] = useState("");
  const [company, setCompany] = useState("");

  const [showSettings, setShowSettings] = useState(false);
  const [selectedStock, setSelectedStock] = useState(null);

  const [priceThreshold, setPriceThreshold] = useState(3);
  const [volumeThreshold, setVolumeThreshold] = useState(1.5);

  useEffect(() => {
    const savedSession = localStorage.getItem(
      "pulsewatch_session"
    );

    if (savedSession) {
      try {
        setUser(JSON.parse(savedSession));
      } catch {
        localStorage.removeItem("pulsewatch_session");
      }
    }

    setLoading(false);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("pulsewatch_session");
    setUser(null);
  };

  const loadDashboard = async () => {
    try {
      setError("");

      const stocksResponse = await axios.get(
        `${API}/api/watchlists/${WATCHLIST_ID}/stocks`
      );

      const changesResponse = await axios.get(
        `${API}/api/watchlists/${WATCHLIST_ID}/changes`
      );

      setStocks(stocksResponse.data);
      setChanges(changesResponse.data.changes);

      if (changesResponse.data.preferences) {
        setPriceThreshold(
          changesResponse.data.preferences.price_threshold
        );

        setVolumeThreshold(
          changesResponse.data.preferences.volume_threshold
        );
      }
    } catch (err) {
      console.error(err);
      setError("Unable to load market data.");
    } finally {
      setLoading(false);
    }
  };

  const loadPreferences = async () => {
    try {
      const response = await axios.get(
        `${API}/api/preferences/`
      );

      setPriceThreshold(response.data.price_threshold);
      setVolumeThreshold(response.data.volume_threshold);
    } catch (err) {
      console.error(err);
    }
  };

  const refreshDashboard = async () => {
    setRefreshing(true);

    await loadDashboard();

    setRefreshing(false);
  };

  const recordVisit = async () => {
    try {
      await axios.post(
        `${API}/api/watchlists/${WATCHLIST_ID}/visit`
      );

      await loadDashboard();
    } catch (err) {
      console.error(err);
      setError("Could not record visit.");
    }
  };

  const runDemo = async () => {
    if (!stocks.length) {
      alert("Add at least one stock first.");
      return;
    }

    try {
      setDemoRunning(true);
      setError("");

      const demoStock =
        stocks.find((stock) => stock.symbol === "TCS") ||
        stocks[0];

      await axios.post(
        `${API}/api/demo/simulate/${WATCHLIST_ID}/${demoStock.symbol}`
      );

      const response = await axios.get(
        `${API}/api/watchlists/${WATCHLIST_ID}/changes`
      );

      const updatedChanges = response.data.changes;

      setChanges(updatedChanges);

      const updatedStock = updatedChanges.find(
        (stock) => stock.symbol === demoStock.symbol
      );

      if (updatedStock) {
        setSelectedStock(updatedStock);
      }
    } catch (err) {
      console.error(err);

      alert(
        err.response?.data?.detail ||
          "Mark the watchlist as visited first, then run the demo."
      );
    } finally {
      setDemoRunning(false);
    }
  };

  const savePreferences = async (e) => {
    e.preventDefault();

    if (
      Number(priceThreshold) <= 0 ||
      Number(volumeThreshold) <= 0
    ) {
      alert("Thresholds must be greater than 0.");
      return;
    }

    try {
      setSavingSettings(true);

      await axios.put(`${API}/api/preferences/`, null, {
        params: {
          price_threshold: Number(priceThreshold),
          volume_threshold: Number(volumeThreshold),
        },
      });

      setShowSettings(false);

      await loadDashboard();
    } catch (err) {
      console.error(err);

      alert(
        err.response?.data?.detail ||
          "Could not update settings."
      );
    } finally {
      setSavingSettings(false);
    }
  };

  const addStock = async (e) => {
    e.preventDefault();

    if (!symbol.trim() || !company.trim()) {
      return;
    }

    try {
      await axios.post(
        `${API}/api/watchlists/${WATCHLIST_ID}/stocks`,
        null,
        {
          params: {
            symbol: symbol.trim().toUpperCase(),
            company_name: company.trim(),
          },
        }
      );

      setSymbol("");
      setCompany("");

      await loadDashboard();
    } catch (err) {
      alert(
        err.response?.data?.detail ||
          "Could not add stock."
      );
    }
  };

  const removeStock = async (stockSymbol) => {
    try {
      await axios.delete(
        `${API}/api/watchlists/${WATCHLIST_ID}/stocks/${stockSymbol}`
      );

      await loadDashboard();
    } catch (err) {
      alert(
        err.response?.data?.detail ||
          "Could not remove stock."
      );
    }
  };

  useEffect(() => {
    if (user) {
      loadDashboard();
      loadPreferences();
    }
  }, [user]);

  const high = changes.filter(
    (s) => s.status === "HIGH"
  ).length;

  const medium = changes.filter(
    (s) => s.status === "MEDIUM"
  ).length;

  const stable = changes.filter(
    (s) => s.status === "STABLE"
  ).length;

  const stale = changes.filter(
    (s) => s.status === "STALE"
  ).length;

  const sortedChanges = [...changes].sort(
    (a, b) =>
      (b.attention_score || 0) -
      (a.attention_score || 0)
  );

  if (!user) {
    return <LoginPage onLogin={setUser} />;
  }

  if (loading) {
    return (
      <div className="loading">
        <Activity size={28} />
        Loading PulseWatch...
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-left">
          <div className="brand">
            <Activity size={25} />
            PulseWatch
          </div>

          <p>
            Know what changed. Know what matters.
          </p>
        </div>

        <div className="header-actions">
          <button
            className="demo-btn"
            onClick={runDemo}
            disabled={demoRunning}
          >
            <Sparkles size={17} />

            {demoRunning
              ? "Running Demo..."
              : "Run Live Demo"}
          </button>

          <button
            className="settings-btn"
            onClick={() => setShowSettings(true)}
          >
            <Settings size={17} />
            Attention Settings
          </button>

          <button
            className="refresh-btn"
            onClick={refreshDashboard}
          >
            <RefreshCw size={17} />

            {refreshing
              ? "Refreshing..."
              : "Refresh"}
          </button>

          <div className="user-menu">
            <div className="user-avatar">
              {user.name?.charAt(0).toUpperCase() || "D"}
            </div>

            <div className="user-details">
              <strong>{user.name}</strong>
              <span>Demo account</span>
            </div>

            <button
              className="logout-btn"
              onClick={handleLogout}
              title="Sign out"
            >
              <LogOut size={16} />
            </button>
          </div>
        </div>
      </header>

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      <main>
        <section className="hero">
          <div>
            <div className="eyebrow">
              <Zap size={14} />
              PERSONALIZED MARKET INTELLIGENCE
            </div>

            <h1>Your Market Pulse</h1>

            <p>
              What changed since your last visit,
              ranked by what matters to you.
            </p>
          </div>

          <button
            className="visit-btn"
            onClick={recordVisit}
          >
            <Clock3 size={17} />
            Mark as visited
          </button>
        </section>

        <section className="stats">
          <div className="stat high">
            <span>🔴</span>

            <div>
              <strong>{high}</strong>
              <small>Need Attention</small>
            </div>
          </div>

          <div className="stat medium">
            <span>🟡</span>

            <div>
              <strong>{medium}</strong>
              <small>Meaningful Changes</small>
            </div>
          </div>

          <div className="stat stable">
            <span>🟢</span>

            <div>
              <strong>{stable}</strong>
              <small>Stable</small>
            </div>
          </div>

          <div className="stat stale">
            <span>🟠</span>

            <div>
              <strong>{stale}</strong>
              <small>Stale Data</small>
            </div>
          </div>
        </section>

        <section className="insight-bar">
          <div className="insight-icon">
            <Brain size={20} />
          </div>

          <div className="insight-content">
            <strong>
              PulseWatch decides what deserves your attention
            </strong>

            <p>
              Every stock is scored using your thresholds,
              price movement and available market signals.
            </p>
          </div>

          <div className="threshold-summary">
            <span>
              Price:{" "}
              <strong>{priceThreshold}%</strong>
            </span>

            <span>
              Volume:{" "}
              <strong>{volumeThreshold}x</strong>
            </span>
          </div>
        </section>

        <section>
          <div className="section-title">
            <div>
              <h2>Since your last visit</h2>

              <p>Highest attention first</p>
            </div>

            <span className="live-label">
              ● Latest available data
            </span>
          </div>

          <div className="cards">
            {sortedChanges.length === 0 ? (
              <div className="empty-state">
                <Activity size={30} />

                <strong>
                  Your watchlist is empty
                </strong>

                <p>
                  Add a stock below to start
                  tracking market changes.
                </p>
              </div>
            ) : (
              sortedChanges.map((stock) => (
                <StockCard
                  key={stock.symbol}
                  stock={stock}
                  onExplain={() =>
                    setSelectedStock(stock)
                  }
                />
              ))
            )}
          </div>
        </section>

        <section className="watchlist-section">
          <div className="section-title">
            <div>
              <h2>My Stocks</h2>

              <p>Your personal watchlist</p>
            </div>

            <span className="stock-count">
              {stocks.length}{" "}
              {stocks.length === 1
                ? "stock"
                : "stocks"}
            </span>
          </div>

          <form
            className="add-form"
            onSubmit={addStock}
          >
            <input
              placeholder="Symbol e.g. TCS"
              value={symbol}
              onChange={(e) =>
                setSymbol(e.target.value)
              }
            />

            <input
              placeholder="Company name"
              value={company}
              onChange={(e) =>
                setCompany(e.target.value)
              }
            />

            <button type="submit">
              <Plus size={17} />
              Add Stock
            </button>
          </form>

          <div className="stock-list">
            {stocks.map((stock) => {
              const change = changes.find(
                (c) => c.symbol === stock.symbol
              );

              return (
                <div
                  className="stock-row"
                  key={stock.id}
                >
                  <div className="stock-info">
                    <strong>{stock.symbol}</strong>

                    <span>
                      {stock.company_name}
                    </span>
                  </div>

                  <div className="stock-price">
                    {change?.current_price
                      ? `₹${change.current_price.toLocaleString(
                          "en-IN"
                        )}`
                      : "—"}
                  </div>

                  <StatusBadge
                    status={
                      change?.status || "NEW"
                    }
                  />

                  <button
                    className="delete-btn"
                    onClick={() =>
                      removeStock(stock.symbol)
                    }
                    title="Remove stock"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              );
            })}
          </div>
        </section>
      </main>

      {selectedStock && (
        <div
          className="modal-overlay"
          onClick={() =>
            setSelectedStock(null)
          }
        >
          <div
            className="why-modal"
            onClick={(e) =>
              e.stopPropagation()
            }
          >
            <div className="why-header">
              <div>
                <div className="why-kicker">
                  <Sparkles size={14} />
                  WHY THIS MATTERS
                </div>

                <h2>{selectedStock.symbol}</h2>

                <p>
                  {selectedStock.company_name}
                </p>
              </div>

              <button
                className="close-btn"
                onClick={() =>
                  setSelectedStock(null)
                }
              >
                <X size={20} />
              </button>
            </div>

            {selectedStock.demo && (
              <div className="demo-warning">
                <Sparkles size={15} />
                DEMO DATA — simulated movement
              </div>
            )}

            <div className="why-price">
              <div>
                <span>Current price</span>

                <strong>
                  ₹
                  {selectedStock.current_price?.toLocaleString(
                    "en-IN"
                  )}
                </strong>
              </div>

              <div
                className={
                  selectedStock.change_percent >= 0
                    ? "why-positive"
                    : "why-negative"
                }
              >
                {selectedStock.change_percent >= 0 ? (
                  <TrendingUp size={19} />
                ) : (
                  <TrendingDown size={19} />
                )}

                {selectedStock.change_percent > 0
                  ? "+"
                  : ""}

                {selectedStock.change_percent}%
              </div>
            </div>

            <div className="score-box">
              <div>
                <span>Attention Score</span>

                <strong>
                  {selectedStock.attention_score}
                  <small>/100</small>
                </strong>
              </div>

              <div className="score-bar">
                <div
                  style={{
                    width: `${Math.min(
                      selectedStock.attention_score || 0,
                      100
                    )}%`,
                  }}
                />
              </div>
            </div>

            <div className="why-grid">
              <div>
                <span>You last saw</span>

                <strong>
                  {selectedStock.last_seen_price
                    ? `₹${selectedStock.last_seen_price.toLocaleString(
                        "en-IN"
                      )}`
                    : "First visit"}
                </strong>
              </div>

              <div>
                <span>Your threshold</span>

                <strong>
                  {priceThreshold}%
                </strong>
              </div>

              <div>
                <span>Movement</span>

                <strong>
                  {selectedStock.change_percent !==
                    null &&
                  selectedStock.change_percent !==
                    undefined
                    ? `${Math.abs(
                        selectedStock.change_percent
                      )}%`
                    : "—"}
                </strong>
              </div>

              <div>
                <span>Threshold multiple</span>

                <strong>
                  {selectedStock.price_multiple ?? 0}×
                </strong>
              </div>
            </div>

            <div className="reason-box">
              <div className="reason-title">
                <Brain size={16} />

                <strong>
                  Why you're seeing this
                </strong>
              </div>

              <p>
                {selectedStock.attention_message}
              </p>

              <div className="reason-detail">
                <ChevronRight size={14} />

                {selectedStock.reason}
              </div>
            </div>

            <div className="why-footer">
              <span>
                Source:{" "}
                {selectedStock.source ||
                  "Unknown"}
              </span>

              <span>
                Last checked:{" "}
                {selectedStock.timestamp
                  ? new Date(
                      selectedStock.timestamp
                    ).toLocaleString()
                  : "Unavailable"}
              </span>
            </div>
          </div>
        </div>
      )}

      {showSettings && (
        <div
          className="modal-overlay"
          onClick={() =>
            setShowSettings(false)
          }
        >
          <div
            className="settings-modal"
            onClick={(e) =>
              e.stopPropagation()
            }
          >
            <div className="modal-header">
              <div>
                <div className="modal-icon">
                  <Settings size={19} />
                </div>

                <h2>Attention Settings</h2>

                <p>
                  Tell PulseWatch what matters to you.
                </p>
              </div>

              <button
                className="close-btn"
                onClick={() =>
                  setShowSettings(false)
                }
              >
                <X size={20} />
              </button>
            </div>

            <form
              onSubmit={savePreferences}
              className="settings-form"
            >
              <div className="setting-card">
                <div className="setting-title">
                  <div>
                    <strong>
                      Price movement
                    </strong>

                    <p>
                      Flag a stock when it moves
                      beyond this percentage
                      since your last visit.
                    </p>
                  </div>

                  <span>
                    {priceThreshold}%
                  </span>
                </div>

                <input
                  type="range"
                  min="0.5"
                  max="10"
                  step="0.5"
                  value={priceThreshold}
                  onChange={(e) =>
                    setPriceThreshold(
                      e.target.value
                    )
                  }
                />

                <div className="range-labels">
                  <span>0.5%</span>
                  <span>10%</span>
                </div>
              </div>

              <div className="setting-card">
                <div className="setting-title">
                  <div>
                    <strong>
                      Volume anomaly
                    </strong>

                    <p>
                      Flag unusual trading activity
                      when volume exceeds the recent
                      average.
                    </p>
                  </div>

                  <span>
                    {volumeThreshold}x
                  </span>
                </div>

                <input
                  type="range"
                  min="1"
                  max="5"
                  step="0.1"
                  value={volumeThreshold}
                  onChange={(e) =>
                    setVolumeThreshold(
                      e.target.value
                    )
                  }
                />

                <div className="range-labels">
                  <span>1x</span>
                  <span>5x</span>
                </div>
              </div>

              <div className="settings-note">
                <Zap size={16} />

                <span>
                  PulseWatch combines price movement
                  and unusual volume to determine
                  whether a stock deserves attention.
                </span>
              </div>

              <button
                className="save-settings"
                type="submit"
                disabled={savingSettings}
              >
                <Save size={17} />

                {savingSettings
                  ? "Saving..."
                  : "Save Attention Rules"}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

function StockCard({ stock, onExplain }) {
  const positive =
    stock.change_percent !== null &&
    stock.change_percent > 0;

  const negative =
    stock.change_percent !== null &&
    stock.change_percent < 0;

  return (
    <div
      className={`stock-card ${stock.status.toLowerCase()}`}
    >
      <div className="card-top">
        <div>
          <span className="symbol">
            {stock.symbol}
          </span>

          <span className="company">
            {stock.company_name}
          </span>
        </div>

        <StatusBadge status={stock.status} />
      </div>

      <div className="price">
        {stock.current_price
          ? `₹${stock.current_price.toLocaleString(
              "en-IN"
            )}`
          : "—"}
      </div>

      {stock.change_percent !== null && (
        <div
          className={`change ${
            positive ? "positive" : ""
          } ${negative ? "negative" : ""}`}
        >
          {positive && <TrendingUp size={18} />}

          {negative && <TrendingDown size={18} />}

          {stock.change_percent > 0 ? "+" : ""}
          {stock.change_percent}%

          <span className="change-label">
            since last visit
          </span>
        </div>
      )}

      <div className="attention-row">
        <div className="attention-score">
          <Brain size={13} />

          <span>Attention score</span>

          <strong>
            {stock.attention_score ?? 0}/100
          </strong>
        </div>
      </div>

      <div className="attention-message">
        {stock.attention_message}
      </div>

      <div className="card-bottom">
        <span>
          {stock.demo
            ? "Demo scenario"
            : stock.reason}
        </span>

        <button
          className="explain-btn"
          onClick={onExplain}
        >
          Why?
          <ChevronRight size={14} />
        </button>
      </div>

      {stock.last_seen_price !== null &&
        stock.last_seen_price !== undefined && (
          <div className="last-seen">
            Last seen: ₹
            {stock.last_seen_price.toLocaleString(
              "en-IN"
            )}
          </div>
        )}

      {stock.timestamp && (
        <div className="timestamp">
          Data:{" "}
          {new Date(
            stock.timestamp
          ).toLocaleString()}
          {" · "}
          {stock.source}
        </div>
      )}
    </div>
  );
}

function StatusBadge({ status }) {
  const labels = {
    HIGH: "HIGH",
    MEDIUM: "MEDIUM",
    STABLE: "STABLE",
    NEW: "NEW",
    STALE: "STALE DATA",
    UNAVAILABLE: "UNAVAILABLE",
  };

  return (
    <span
      className={`badge ${status.toLowerCase()}`}
    >
      {labels[status] || status}
    </span>
  );
}

export default App;