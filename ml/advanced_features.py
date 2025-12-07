import pandas as pd

# --- RSI ---
def compute_rsi(series, window=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()

    rs = avg_gain / (avg_loss + 1e-9)
    return 100 - (100 / (1 + rs))


# --- MACD ---
def compute_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()

    macd = ema_fast - ema_slow
    macd_signal = macd.ewm(span=signal, adjust=False).mean()
    macd_hist = macd - macd_signal

    return macd, macd_signal, macd_hist


# --- Bollinger Bands ---
def compute_bollinger(series, window=20, num_std=2):
    sma = series.rolling(window).mean()
    std = series.rolling(window).std()

    upper = sma + num_std * std
    lower = sma - num_std * std

    return sma, upper, lower


# --- Rolling Volatility ---
def compute_volatility(series, window=20):
    return series.pct_change().rolling(window).std()


# --- Momentum ---
def compute_momentum(series, window=10):
    return series.diff(window)


# --- Correlations ---
def compute_correlation(series1, series2, window=20):
    return series1.rolling(window).corr(series2)


# --- Build all features ---
def build_advanced_features(df, price_col="close_value"):
    """
    מחזיר DataFrame עם כל הפיצ'רים המתקדמים.
    """

    s = df[price_col]

    features = pd.DataFrame()

    # RSI
    features["rsi_14"] = compute_rsi(s)

    # MACD
    macd, macd_signal, macd_hist = compute_macd(s)
    features["macd"] = macd
    features["macd_signal"] = macd_signal
    features["macd_hist"] = macd_hist

    # Bollinger
    sma, upper, lower = compute_bollinger(s)
    features["bb_sma"] = sma
    features["bb_upper"] = upper
    features["bb_lower"] = lower

    # Volatility
    features["volatility_20"] = compute_volatility(s)

    # Momentum
    features["momentum_10"] = compute_momentum(s)

    # Normalized price change
    features["pct_change_1d"] = s.pct_change()
    features["pct_change_5d"] = s.pct_change(5)

    # Return the final feature table
    return features.fillna(0)
