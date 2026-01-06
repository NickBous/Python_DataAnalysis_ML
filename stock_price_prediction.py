import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from datetime import date, timedelta
import warnings

warnings.filterwarnings("ignore")

# 1. FETCH & PREPARE DATA
def fetch_and_prepare_data(ticker, period="1y"):

    print(f"\n--- 1. Fetching historical data for {ticker} over {period}...")

    data = yf.download(ticker, period=period)

    if data.empty:
        print("ERROR: No data downloaded.")
        return None

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # Ensure Close exists
    if 'Close' not in data.columns:
        raise RuntimeError("Close column not found after cleaning columns!")

    # FEATURE ENGINEERING
    data['Prev_Close'] = data['Close'].shift(1)
    data['MA_5'] = data['Close'].rolling(5).mean()
    data['MA_20'] = data['Close'].rolling(20).mean()
    data['Momentum_3d'] = data['Close'].pct_change(3) * 100
    data['Volatility_5d'] = data['Close'].pct_change().rolling(5).std()

    # TARGET CREATION (100% SAFE)
    PREDICTION_DAYS = 5
    print(f"--- 2. Defining target: Percentage change in {PREDICTION_DAYS} days.")

    data['Future_Close'] = data['Close'].shift(-PREDICTION_DAYS)

    data['Target_Percent'] = (
        (data['Future_Close'] - data['Close']) / data['Close']
    ) * 100

    # CLEAN DATA
    data.dropna(inplace=True)

    # HARD SAFETY CHECK
    if 'Target_Percent' not in data.columns:
        raise RuntimeError("Target_Percent column was NOT created!")

    print(f"Data ready. Training points: {len(data)}")

    return data, PREDICTION_DAYS


# 2. TRAIN & PREDICT
def train_and_predict(data, prediction_days):

    features = ['Prev_Close', 'MA_5', 'MA_20', 'Momentum_3d', 'Volatility_5d']

    X = data[features].values
    y = data['Target_Percent'].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, shuffle=False
    )

    print("--- 3. Training Linear Regression Model...")

    model = LinearRegression()
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print(f"Model trained. R² score: {score:.4f}")

    last_features = data[features].iloc[[-1]].values
    last_features_scaled = scaler.transform(last_features)

    prediction = model.predict(last_features_scaled)[0]

    return prediction, prediction_days, data.index[-1].strftime('%Y-%m-%d')


# 3. MAIN
if __name__ == "__main__":

    # MULTI-ASSET CONFIGURATION
    ASSETS = {
        "ETH-USD": "Ethereum",
        "NVDA": "NVIDIA",
        "GOOGL": "Google Alphabet A",
        "TSLA": "Tesla",
        "MSFT": "Microsoft",
        "AMZN": "Amazon"
    }

    for TICKER, NAME in ASSETS.items():

        stock = yf.Ticker(TICKER)
        info = stock.info

        current_price = info.get("currentPrice", "N/A")
        market_cap = info.get("marketCap", "N/A")
        sector = info.get("sector", "Crypto / N/A")

        result = fetch_and_prepare_data(TICKER)

        if result is not None:

            processed_data, DAYS_TO_PREDICT = result

            prediction, days, last_date_used = train_and_predict(
                processed_data, DAYS_TO_PREDICT
            )

            future_date = date.today() + timedelta(days=days)

            print("\n" + "=" * 65)
            print(f"FINANCIAL PRICE PREDICTION REPORT FOR {NAME} ({TICKER})")
            print(f"Prediction Date: {date.today()}")
            print(f"Data Used Up To: {last_date_used}")
            print(f"Target Period: {days} trading days")
            print(f"Approx Target Date: {future_date}")
            print(f"Sector: {sector}")
            print(f"Market Cap: {market_cap}")
            print("=" * 65)

            direction = "increase" if prediction >= 0 else "decrease"

            print(f"The model predicts a price {direction} of: {abs(prediction):.2f}%")
            print(f"Current close: ${processed_data['Close'].iloc[-1]:.2f}")
            print(f"Expected change: {prediction:.2f}% in {days} days")
            print("=" * 65)
