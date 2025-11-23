# # top of backend.py — must be first lines (before importing matplotlib.pyplot or anything that may import matplotlib)
# import os
# os.environ["PYTHONHASHSEED"] = "42"
# os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# # Force non-interactive Matplotlib very early
# os.environ["MPLBACKEND"] = "Agg"   # env var fallback
# import matplotlib
# matplotlib.use("Agg")

# from pathlib import Path
# import random
# import numpy as np
# import pandas as pd
# import joblib
# import time
# from threading import Lock  # NEW: for rate limiting

# from sklearn.metrics import mean_squared_error, r2_score
# from sklearn.preprocessing import StandardScaler
# from sklearn.cluster import KMeans

# import matplotlib.pyplot as plt  # <-- for plots

# # Flask imports
# from flask import Flask, jsonify, request
# from flask_cors import CORS

# # ---------------- NEW IMPORTS: ENV + BLOCKCHAIN + FIREBASE ----------------
# from dotenv import load_dotenv
# load_dotenv()

# from web3 import Web3
# import firebase_admin
# from firebase_admin import credentials, firestore

# # ======================= ENV CONFIG FOR INTEGRATIONS =======================

# FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")

# GANACHE_RPC_URL = os.getenv("GANACHE_RPC_URL", "http://127.0.0.1:7545")
# GANACHE_PRIVATE_KEY = os.getenv("GANACHE_PRIVATE_KEY")
# GANACHE_ACCOUNT_ADDRESS = os.getenv("GANACHE_ACCOUNT_ADDRESS")
# FORECAST_CONTRACT_ADDRESS = os.getenv("FORECAST_CONTRACT_ADDRESS")
# GANACHE_CHAIN_ID = int(os.getenv("GANACHE_CHAIN_ID", "1337"))

# API_SECRET_KEY = os.getenv("API_SECRET_KEY", "supersecret")

# # ===== RATE LIMIT CONFIG =====
# # Allow up to MAX_LOG_REQUESTS_PER_WINDOW logs every LOG_RATE_LIMIT_WINDOW_SECONDS seconds.
# # Default: 2 logs every 180 seconds (3 mins). You can change via env:
# # LOG_MAX_REQUESTS_PER_WINDOW, LOG_RATE_LIMIT_WINDOW_SECONDS (e.g., 300 for 5 mins).
# MAX_LOG_REQUESTS_PER_WINDOW = int(os.getenv("LOG_MAX_REQUESTS_PER_WINDOW", "2"))
# LOG_RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("LOG_RATE_LIMIT_WINDOW_SECONDS", "180"))

# # Globals for integrations
# firebase_app = None
# firestore_client = None

# w3 = None
# forecast_contract = None
# blockchain_account_address = None
# blockchain_private_key = None

# # Globals for rate limiting state (fixed window)
# rate_limit_lock = Lock()
# window_start_ts = 0.0
# window_request_count = 0


# def check_rate_limit():
#     """
#     Fixed-window rate limit for *logging* to blockchain + Firebase.

#     Logic:
#       - Window length: LOG_RATE_LIMIT_WINDOW_SECONDS
#       - Max requests per window: MAX_LOG_REQUESTS_PER_WINDOW
#       - Allow up to MAX_LOG_REQUESTS_PER_WINDOW, then block until window resets.

#     Returns:
#         allowed (bool), cooldown_remaining (float seconds)
#     """
#     global window_start_ts, window_request_count
#     now = time.time()
#     with rate_limit_lock:
#         # If window not started or expired -> reset window
#         if window_start_ts == 0.0 or (now - window_start_ts) >= LOG_RATE_LIMIT_WINDOW_SECONDS:
#             window_start_ts = now
#             window_request_count = 0

#         if window_request_count < MAX_LOG_REQUESTS_PER_WINDOW:
#             # Allow request inside current window
#             window_request_count += 1
#             return True, 0.0

#         # Window still active and max count reached -> rate limited
#         elapsed = now - window_start_ts
#         cooldown = max(0.0, LOG_RATE_LIMIT_WINDOW_SECONDS - elapsed)
#         return False, cooldown

# # ======================= INITIALIZE FIREBASE =======================

# def init_firebase():
#     """
#     Initialize Firebase Admin SDK (Firestore).
#     Uses FIREBASE_CREDENTIALS path from .env.
#     """
#     global firebase_app, firestore_client

#     if firebase_app is not None:
#         return

#     if not FIREBASE_CREDENTIALS:
#         print("⚠ FIREBASE_CREDENTIALS not set. Firebase logging disabled.")
#         return

#     try:
#         cred = credentials.Certificate(FIREBASE_CREDENTIALS)
#         firebase_app = firebase_admin.initialize_app(cred)
#         firestore_client = firestore.client()
#         print("✅ Firebase initialized successfully.")
#     except Exception as e:
#         print(f"⚠ Firebase initialization failed: {e}")
#         firebase_app = None
#         firestore_client = None

# # ======================= INITIALIZE BLOCKCHAIN (GANACHE) =======================

# def get_forecast_logger_abi():
#     """
#     Minimal ABI for the ForecastLogger contract you deployed with Hardhat.
#     Matches:

#     contract ForecastLogger {
#         uint256 public latestForecast;
#         string public latestModelVersion;
#         uint256 public lastUpdatedAt;
#         event ForecastSaved(uint256 value, string modelVersion, uint256 timestamp);
#         function saveForecast(uint256 _value, string calldata _modelVersion) external;
#     }
#     """
#     return [
#         {
#             "inputs": [],
#             "stateMutability": "nonpayable",
#             "type": "constructor"
#         },
#         {
#             "anonymous": False,
#             "inputs": [
#                 {
#                     "indexed": False,
#                     "internalType": "uint256",
#                     "name": "value",
#                     "type": "uint256"
#                 },
#                 {
#                     "indexed": False,
#                     "internalType": "string",
#                     "name": "modelVersion",
#                     "type": "string"
#                 },
#                 {
#                     "indexed": False,
#                     "internalType": "uint256",
#                     "name": "timestamp",
#                     "type": "uint256"
#                 }
#             ],
#             "name": "ForecastSaved",
#             "type": "event"
#         },
#         {
#             "inputs": [],
#             "name": "latestForecast",
#             "outputs": [
#                 {
#                     "internalType": "uint256",
#                     "name": "",
#                     "type": "uint256"
#                 }
#             ],
#             "stateMutability": "view",
#             "type": "function"
#         },
#         {
#             "inputs": [],
#             "name": "latestModelVersion",
#             "outputs": [
#                 {
#                     "internalType": "string",
#                     "name": "",
#                     "type": "string"
#                 }
#             ],
#             "stateMutability": "view",
#             "type": "function"
#         },
#         {
#             "inputs": [],
#             "name": "lastUpdatedAt",
#             "outputs": [
#                 {
#                     "internalType": "uint256",
#                     "name": "",
#                     "type": "uint256"
#                 }
#             ],
#             "stateMutability": "view",
#             "type": "function"
#         },
#         {
#             "inputs": [
#                 {
#                     "internalType": "uint256",
#                     "name": "_value",
#                     "type": "uint256"
#                 },
#                 {
#                     "internalType": "string",
#                     "name": "_modelVersion",
#                     "type": "string"
#                 }
#             ],
#             "name": "saveForecast",
#             "outputs": [],
#             "stateMutability": "nonpayable",
#             "type": "function"
#         }
#     ]

# def init_blockchain():
#     """
#     Initialize Web3 + ForecastLogger contract instance using Ganache.
#     Requires GANACHE_RPC_URL, GANACHE_PRIVATE_KEY, FORECAST_CONTRACT_ADDRESS.
#     """
#     global w3, forecast_contract, blockchain_account_address, blockchain_private_key

#     if w3 is not None and forecast_contract is not None:
#         return

#     if not GANACHE_RPC_URL or not GANACHE_PRIVATE_KEY or not FORECAST_CONTRACT_ADDRESS:
#         print("⚠ Blockchain env vars missing (GANACHE_RPC_URL / GANACHE_PRIVATE_KEY / FORECAST_CONTRACT_ADDRESS).")
#         return

#     try:
#         w3_local = Web3(Web3.HTTPProvider(GANACHE_RPC_URL))
#         if not w3_local.is_connected():
#             print("⚠ Could not connect to Ganache RPC. Blockchain logging disabled.")
#             return

#         blockchain_private_key = GANACHE_PRIVATE_KEY

#         if GANACHE_ACCOUNT_ADDRESS:
#             blockchain_account_address = Web3.to_checksum_address(GANACHE_ACCOUNT_ADDRESS)
#         else:
#             acct = w3_local.eth.account.from_key(blockchain_private_key)
#             blockchain_account_address = acct.address

#         contract_address = Web3.to_checksum_address(FORECAST_CONTRACT_ADDRESS)
#         contract_abi = get_forecast_logger_abi()
#         contract_instance = w3_local.eth.contract(address=contract_address, abi=contract_abi)

#         w3 = w3_local
#         forecast_contract = contract_instance

#         print(f"✅ Connected to Ganache at {GANACHE_RPC_URL}")
#         print(f"✅ ForecastLogger contract at {contract_address}")
#         print(f"✅ Using account {blockchain_account_address}")
#     except Exception as e:
#         print(f"⚠ Blockchain init failed: {e}")
#         w3 = None
#         forecast_contract = None
#         blockchain_account_address = None
#         blockchain_private_key = None

# # ======================= LOG TO BLOCKCHAIN + FIREBASE =======================

# def log_forecast_onchain_and_firebase(total_forecast, model_version="lstm_weekly_v1"):
#     """
#     Take the numeric 'total_forecast' (next 4 weeks total sales),
#     push it to:
#       1) ForecastLogger smart contract (Ganache)
#       2) Firebase Firestore 'forecast_logs' collection

#     Returns a dict with metadata so endpoints can surface it to the UI.
#     """
#     result = {
#         "onchain": False,
#         "firebase": False,
#         "tx_hash": None,
#         "logged_value_int": None,
#         "model_version": model_version,
#     }

#     if total_forecast is None:
#         print("⚠ No forecast value to log on-chain / Firebase.")
#         return result

#     # Normalize to int for uint256 (we store INR with no decimals)
#     try:
#         value_int = int(round(float(total_forecast)))
#     except Exception:
#         print("⚠ Could not convert forecast to integer for blockchain.")
#         return result

#     result["logged_value_int"] = value_int

#     # --- Initialize integrations (lazy) ---
#     init_blockchain()
#     init_firebase()

#     # --- 1) Blockchain: call saveForecast(value_int, model_version) ---
#     if (
#         w3 is not None
#         and forecast_contract is not None
#         and blockchain_account_address is not None
#         and blockchain_private_key is not None
#     ):
#         try:
#             nonce = w3.eth.get_transaction_count(blockchain_account_address)

#             tx = forecast_contract.functions.saveForecast(
#                 value_int,
#                 model_version
#             ).build_transaction(
#                 {
#                     "from": blockchain_account_address,
#                     "nonce": nonce,
#                     "gas": 300000,
#                     "gasPrice": w3.eth.gas_price,
#                     "chainId": GANACHE_CHAIN_ID,
#                 }
#             )

#             signed_tx = w3.eth.account.sign_transaction(tx, private_key=blockchain_private_key)

#             # web3.py v6 uses `raw_transaction` (snake_case)
#             tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

#             receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

#             print(f"✅ Saved forecast on-chain. Tx hash: {tx_hash.hex()}")
#             print(f"   Block: {receipt.blockNumber}, Gas used: {receipt.gasUsed}")

#             result["onchain"] = True
#             result["tx_hash"] = tx_hash.hex()
#         except Exception as e:
#             print(f"⚠ Blockchain logging failed: {e}")
#     else:
#         print("⚠ Blockchain not initialized; skipping on-chain logging.")

#     # --- 2) Firebase: add document to 'forecast_logs' ---
#     if firestore_client is not None:
#         try:
#             doc = {
#                 "value_int": value_int,
#                 "value_raw": float(total_forecast),
#                 "currency": "INR",
#                 "model_version": model_version,
#                 "tx_hash": result["tx_hash"],
#                 "source": "backend_forecast_summary",
#                 "created_at": firestore.SERVER_TIMESTAMP,
#             }
#             # .add() uses auto ID -> should not conflict, but rate limiting protects from spam
#             firestore_client.collection("forecast_logs").add(doc)
#             print("✅ Saved forecast to Firebase Firestore (forecast_logs).")
#             result["firebase"] = True
#         except Exception as e:
#             print(f"⚠ Firebase logging failed: {e}")
#     else:
#         print("⚠ Firestore client not available; skipping Firebase logging.")

#     return result

# # =======================
# # TensorFlow / LSTM
# # =======================
# try:
#     import tensorflow as tf
#     TF_IMPORT_ERROR = None

#     # set seeds for reproducibility
#     random.seed(42)
#     np.random.seed(42)
#     tf.random.set_seed(42)
# except Exception as e:
#     tf = None
#     TF_IMPORT_ERROR = e
#     print("⚠ TensorFlow import failed. LSTM model will be skipped.")
#     print("   Reason:", e)

# # =========================================================
# # CONFIG – EDIT ONLY PATH IF NEEDED
# # =========================================================

# # ⚠ Make sure this path + filename matches your actual CSV on disk.
# # CSV_PATH = Path(r"online_retail.csv")  # your dataset
# CSV_PATH = Path(r"Online_Retail_new.csv")  # your dataset

# DATE_COL = "InvoiceDate"
# QTY_COL = "Quantity"
# PRICE_COL = "Price"
# CUSTOMER_COL = "Customer ID"
# INVOICE_COL = "Invoice"
# COUNTRY_COL = "Country"
# DESC_COL = "Description"

# MODELS_DIR = Path("models")
# ARTIFACTS_DIR = Path("artifacts")
# MODELS_DIR.mkdir(exist_ok=True, parents=True)
# ARTIFACTS_DIR.mkdir(exist_ok=True, parents=True)

# DAILY_SALES_PATH = ARTIFACTS_DIR / "daily_sales.csv"
# WEEKLY_SALES_PATH = ARTIFACTS_DIR / "weekly_sales.csv"
# CATEGORY_SALES_PATH = ARTIFACTS_DIR / "category_sales.csv"
# COUNTRY_SALES_PATH = ARTIFACTS_DIR / "country_sales.csv"

# CLEANED_DATA_PATH = ARTIFACTS_DIR / "cleaned_online_retail.csv"

# LSTM_MODEL_PATH = MODELS_DIR / "lstm_model_weekly.h5"
# LSTM_SCALER_PATH = MODELS_DIR / "lstm_scaler_weekly.pkl"
# LSTM_METRICS_PATH = ARTIFACTS_DIR / "lstm_forecast_metrics_weekly.csv"

# # EDA outputs
# EDA_MISSING_PATH = ARTIFACTS_DIR / "eda_missing_values.csv"
# EDA_DESCRIBE_PATH = ARTIFACTS_DIR / "eda_describe_all.csv"
# EDA_MONTHLY_SALES_PATH = ARTIFACTS_DIR / "eda_monthly_sales.csv"
# EDA_TOP_PRODUCTS_PATH = ARTIFACTS_DIR / "eda_top_products.csv"
# EDA_TOP_COUNTRIES_PATH = ARTIFACTS_DIR / "eda_top_countries.csv"

# # 4-week LSTM forecast outputs
# NEXT4W_LSTM_PATH = ARTIFACTS_DIR / "next4weeks_lstm.csv"
# NEXT4W_LSTM_BY_COUNTRY_PATH = ARTIFACTS_DIR / "next4weeks_lstm_by_country.csv"
# NEXT4W_LSTM_BY_CATEGORY_PATH = ARTIFACTS_DIR / "next4weeks_lstm_by_category.csv"

# # Plots output directory
# PLOTS_DIR = ARTIFACTS_DIR / "plots"
# PLOTS_DIR.mkdir(exist_ok=True, parents=True)

# # =========================================================
# # UTILS
# # =========================================================

# def mape(y_true, y_pred, eps=1e-3):
#     """
#     MAPE ignoring very small true values, to avoid exploding percentages.
#     """
#     y_true = np.array(y_true, dtype=float)
#     y_pred = np.array(y_pred, dtype=float)

#     mask = np.abs(y_true) > eps
#     if not np.any(mask):
#         return np.nan

#     return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

# # ---------------- PLOTTING HELPERS ----------------

# def plot_time_series(df, date_col, value_col, title, y_label, file_path):
#     """
#     Generic time series line plot.
#     """
#     plt.figure(figsize=(10, 5))
#     plt.plot(df[date_col], df[value_col])
#     plt.title(title)
#     plt.xlabel("Date")
#     plt.ylabel(y_label)
#     plt.grid(True, linestyle="--", alpha=0.5)
#     plt.tight_layout()
#     plt.savefig(file_path)
#     plt.close()
#     print(f"Saved plot: {file_path}")

# def plot_bar(df, x_col, y_col, title, x_label, y_label, file_path, rotation=45):
#     """
#     Generic bar chart.
#     """
#     plt.figure(figsize=(10, 5))
#     plt.bar(df[x_col].astype(str), df[y_col])
#     plt.title(title)
#     plt.xlabel(x_label)
#     plt.ylabel(y_label)
#     plt.xticks(rotation=rotation, ha="right")
#     plt.tight_layout()
#     plt.savefig(file_path)
#     plt.close()
#     print(f"Saved plot: {file_path}")

# def plot_lstm_forecast(weekly_df, forecast_df, file_path, last_weeks_history=20):
#     """
#     Plot the last few weeks of historical sales and next 4-week LSTM forecast.
#     weekly_df: DataFrame with columns ['ds', 'y']
#     forecast_df: DataFrame with columns ['ds', 'yhat_lstm']
#     """
#     weekly_df = weekly_df.sort_values("ds").copy()
#     hist_tail = weekly_df.tail(last_weeks_history)

#     plt.figure(figsize=(10, 5))
#     # history
#     plt.plot(hist_tail["ds"], hist_tail["y"], label="Historical Weekly Sales")

#     # forecast
#     plt.plot(
#         forecast_df["ds"],
#         forecast_df["yhat_lstm"],
#         marker="o",
#         linestyle="--",
#         label="Next 4 Weeks Forecast",
#     )

#     plt.title("Weekly Sales with Next 4-Week LSTM Forecast")
#     plt.xlabel("Date")
#     plt.ylabel("SalesAmount")
#     plt.grid(True, linestyle="--", alpha=0.5)
#     plt.legend()
#     plt.tight_layout()
#     plt.savefig(file_path)
#     plt.close()
#     print(f"Saved LSTM forecast plot: {file_path}")

# # =========================================================
# # 1. LOAD + CLEAN DATA
# # =========================================================

# def load_raw_data():
#     print(f"Loading data from {CSV_PATH}")
#     df = pd.read_csv(CSV_PATH, encoding="ISO-8859-1")
#     print("Raw shape:", df.shape)
#     print("Columns:", df.columns.tolist())
#     return df

# def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
#     print("\n=== CLEANING: start ===")
#     # ensure date parse
#     df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")

#     initial_rows = len(df)

#     # drop cancelled invoices (Invoice starting with 'C')
#     if INVOICE_COL in df.columns:
#         df[INVOICE_COL] = df[INVOICE_COL].astype(str)
#         df = df[~df[INVOICE_COL].str.startswith("C")]
#         print(f"Removed cancelled invoices. Rows now: {len(df)}")

#     # drop rows with missing critical info
#     df = df.dropna(subset=[DATE_COL, QTY_COL, PRICE_COL])
#     print(f"After dropping rows with NA in [{DATE_COL}, {QTY_COL}, {PRICE_COL}]: {len(df)} rows")

#     # convert quantity and price to numeric (in case of bad strings)
#     df[QTY_COL] = pd.to_numeric(df[QTY_COL], errors="coerce")
#     df[PRICE_COL] = pd.to_numeric(df[PRICE_COL], errors="coerce")

#     df = df.dropna(subset=[QTY_COL, PRICE_COL])
#     print(f"After enforcing numeric {QTY_COL}/{PRICE_COL}: {len(df)} rows")

#     # sales amount
#     df["SalesAmount"] = df[QTY_COL] * df[PRICE_COL]

#     # remove negative/zero sales and quantities
#     df = df[df["SalesAmount"] > 0]
#     df = df[df[QTY_COL] > 0]

#     print(f"After removing negative/zero sales & qty: {len(df)} rows")

#     # remove extreme outliers
#     upper = df["SalesAmount"].quantile(0.999)
#     df = df[df["SalesAmount"] <= upper]
#     print(f"After removing top 0.1% extreme sales: {len(df)} rows (upper={upper:.2f})")

#     # optionally drop rows without customer ID for RFM (not required for forecasting)
#     if CUSTOMER_COL in df.columns:
#         rows_before_cust = len(df)
#         df = df.dropna(subset=[CUSTOMER_COL])
#         print(f"Dropped rows without Customer ID for RFM: {rows_before_cust - len(df)} rows removed")

#     print(f"=== CLEANING: done. Final cleaned rows: {len(df)} (from {initial_rows}) ===")
#     return df

# # =========================================================
# # 1b. EDA
# # =========================================================

# def perform_eda(df: pd.DataFrame):
#     """
#     Perform basic EDA and save outputs as CSVs into artifacts/.
#     Also return some EDA DataFrames for plotting.
#     """
#     print("\n=== EDA: start ===")

#     # Missing values
#     missing = df.isna().sum().sort_values(ascending=False)
#     missing.to_csv(EDA_MISSING_PATH, header=["missing_count"])
#     print(f"Saved missing values report to {EDA_MISSING_PATH}")

#     # Describe (numeric + object); handle pandas versions without datetime_is_numeric
#     try:
#         describe_all = df.describe(include="all", datetime_is_numeric=True)
#     except TypeError:
#         describe_all = df.describe(include="all")
#     describe_all.to_csv(EDA_DESCRIBE_PATH)
#     print(f"Saved full describe() summary to {EDA_DESCRIBE_PATH}")

#     # Monthly sales trend
#     df_month = df.copy()
#     df_month[DATE_COL] = pd.to_datetime(df_month[DATE_COL])
#     df_month["InvoiceMonth"] = df_month[DATE_COL].dt.to_period("M").dt.to_timestamp()
#     monthly_sales = (
#         df_month.groupby("InvoiceMonth")["SalesAmount"]
#         .sum()
#         .reset_index()
#         .sort_values("InvoiceMonth")
#     )
#     monthly_sales.to_csv(EDA_MONTHLY_SALES_PATH, index=False)
#     print(f"Saved monthly sales trend to {EDA_MONTHLY_SALES_PATH}")

#     # Top 20 products by total sales
#     top_products = (
#         df.groupby(DESC_COL)["SalesAmount"]
#         .sum()
#         .reset_index()
#         .sort_values("SalesAmount", ascending=False)
#         .head(20)
#     )
#     top_products.to_csv(EDA_TOP_PRODUCTS_PATH, index=False)
#     print(f"Saved top 20 products by sales to {EDA_TOP_PRODUCTS_PATH}")

#     # Top 20 countries by total sales
#     top_countries = (
#         df.groupby(COUNTRY_COL)["SalesAmount"]
#         .sum()
#         .reset_index()
#         .sort_values("SalesAmount", ascending=False)
#         .head(20)
#     )
#     top_countries.to_csv(EDA_TOP_COUNTRIES_PATH, index=False)
#     print(f"Saved top 20 countries by sales to {EDA_TOP_COUNTRIES_PATH}")

#     print("=== EDA: done. Check artifacts/ folder for CSV summaries. ===")

#     # return for plotting
#     return monthly_sales, top_products, top_countries

# # =========================================================
# # 2. AGGREGATION: DAILY/WEEKLY/CATEGORY/COUNTRY
# # =========================================================

# def build_daily_sales(df: pd.DataFrame) -> pd.DataFrame:
#     daily = (
#         df.set_index(DATE_COL)
#           .resample("D")
#           .agg({"SalesAmount": "sum"})
#           .rename(columns={"SalesAmount": "y"})
#     )
#     daily["y"] = daily["y"].fillna(0)
#     daily = daily.reset_index().rename(columns={DATE_COL: "ds"})
#     return daily

# def build_weekly_sales(df: pd.DataFrame) -> pd.DataFrame:
#     weekly = (
#         df.set_index(DATE_COL)
#           .resample("W")
#           .agg({"SalesAmount": "sum"})
#           .rename(columns={"SalesAmount": "y"})
#     )
#     weekly["y"] = weekly["y"].fillna(0)
#     weekly = weekly.reset_index().rename(columns={DATE_COL: "ds"})
#     return weekly

# def build_category_sales(df: pd.DataFrame) -> pd.DataFrame:
#     cat = (
#         df.groupby([DESC_COL])
#           .agg({"SalesAmount": "sum"})
#           .reset_index()
#           .sort_values("SalesAmount", ascending=False)
#     )
#     return cat

# def build_country_sales(df: pd.DataFrame) -> pd.DataFrame:
#     ctry = (
#         df.groupby([COUNTRY_COL])
#           .agg({"SalesAmount": "sum"})
#           .reset_index()
#           .sort_values("SalesAmount", ascending=False)
#     )
#     return ctry

# # =========================================================
# # 3. LSTM FORECAST MODEL (WEEKLY, 4-WEEK TEST + 4-WEEK FUTURE)
# # =========================================================

# def build_lstm_sequences(y_scaled: np.ndarray, lookback: int):
#     """
#     Convert 1D scaled series to supervised sequences for LSTM.
#     y_scaled: shape (T,)
#     Returns: X (num_samples, lookback, 1), y (num_samples,)
#     """
#     X, y = [], []
#     for i in range(len(y_scaled) - lookback):
#         X.append(y_scaled[i:i + lookback])
#         y.append(y_scaled[i + lookback])
#     X = np.array(X)
#     y = np.array(y)
#     # reshape X to (samples, timesteps, features)
#     X = X.reshape((X.shape[0], X.shape[1], 1))
#     return X, y

# def train_lstm_forecaster(
#     weekly: pd.DataFrame,
#     last_raw_date: pd.Timestamp,
#     lookback: int = 12,
#     test_points: int = 4
# ):
#     """
#     Train an LSTM forecaster on weekly aggregated 'y' series.
#     - lookback: number of past weeks to use as input window.
#     - test_points: number of final target points used as test (here 4 weeks).
#     Also creates a 4-week future forecast and saves it.

#     Future weeks are anchored to the latest date in the raw dataset (last_raw_date),
#     so forecasts correspond to:
#         last_raw_date + 1 week
#         last_raw_date + 2 weeks
#         last_raw_date + 3 weeks
#         last_raw_date + 4 weeks
#     """
#     if tf is None:
#         print("⚠ TensorFlow is not available; skipping LSTM training.")
#         return None, None, None

#     df = weekly.copy().sort_values("ds")
#     y_series = df["y"].values.astype(float)

#     if len(y_series) <= lookback + test_points + 5:
#         raise ValueError("Time series too short for LSTM with given lookback and test_points.")

#     # Scale target series
#     scaler = StandardScaler()
#     y_scaled = scaler.fit_transform(y_series.reshape(-1, 1)).flatten()

#     # Build sequences
#     X_all, y_all = build_lstm_sequences(y_scaled, lookback=lookback)
#     num_sequences = X_all.shape[0]

#     if num_sequences <= test_points:
#         raise ValueError("Not enough sequences for the chosen test_points in LSTM.")

#     # Split train/test on sequences: last test_points as test (time-ordered)
#     split_idx = num_sequences - test_points
#     X_train, X_test = X_all[:split_idx], X_all[split_idx:]
#     y_train, y_test = y_all[:split_idx], y_all[split_idx:]

#     print(f"\nLSTM: total sequences={num_sequences}, train={X_train.shape[0]}, test={X_test.shape[0]}")

#     # Build a slightly deeper LSTM model for better learning
#     model = tf.keras.Sequential([
#         tf.keras.layers.Input(shape=(lookback, 1)),
#         tf.keras.layers.LSTM(64, return_sequences=True, activation="tanh"),
#         tf.keras.layers.LSTM(32, activation="tanh"),
#         tf.keras.layers.Dense(16, activation="relu"),
#         tf.keras.layers.Dense(1)
#     ])

#     model.compile(
#         optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
#         loss="mse"
#     )

#     # Early stopping to avoid overfitting (still deterministic with fixed seeds)
#     callbacks = [
#         tf.keras.callbacks.EarlyStopping(
#             monitor="val_loss",
#             patience=10,
#             restore_best_weights=True
#         )
#     ]

#     # Train – shuffle=False to keep sequences ordered deterministically
#     history = model.fit(
#         X_train, y_train,
#         epochs=100,
#         batch_size=16,
#         verbose=1,
#         validation_split=0.1,
#         shuffle=False,
#         callbacks=callbacks
#     )

#     # Predict on test
#     y_pred_scaled = model.predict(X_test).flatten()

#     # Inverse scale (test)
#     y_test_true = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()
#     y_test_pred = scaler.inverse_transform(y_pred_scaled.reshape(-1, 1)).flatten()

#     # Metrics
#     rmse = np.sqrt(mean_squared_error(y_test_true, y_test_pred))
#     test_mape = mape(y_test_true, y_test_pred)
#     r2 = r2_score(y_test_true, y_test_pred)

#     if np.isnan(test_mape):
#         accuracy_pct = np.nan
#     else:
#         accuracy_pct = max(0.0, 100.0 - test_mape)

#     print("\n=== LSTM Forecast Performance (weekly, last {} points) ===".format(test_points))
#     print(f"RMSE: {rmse:.3f}")
#     if np.isnan(test_mape):
#         print("MAPE: cannot be computed reliably (all true values are ~0).")
#         print("Accuracy: not defined.")
#     else:
#         print(f"MAPE: {test_mape:.3f}%")
#         print(f"Approx. Forecast Accuracy (100 - MAPE, clipped): {accuracy_pct:.2f}%")
#     print(f"R²:   {r2:.4f}")

#     metrics = {
#         "rmse": float(rmse),
#         "mape": float(test_mape) if not np.isnan(test_mape) else None,
#         "r2": float(r2),
#         "accuracy_pct": float(accuracy_pct) if not np.isnan(accuracy_pct) else None
#     }

#     # ===== 4-WEEK FUTURE FORECAST (RECURSIVE) =====
#     last_lookback_scaled = y_scaled[-lookback:]
#     window = last_lookback_scaled.reshape(1, lookback, 1)

#     future_scaled = []
#     steps_ahead = 4
#     for _ in range(steps_ahead):
#         next_scaled = model.predict(window, verbose=0)[0, 0]
#         future_scaled.append(next_scaled)
#         # shift window and append new prediction
#         window = np.roll(window, -1, axis=1)
#         window[0, -1, 0] = next_scaled

#     future_scaled = np.array(future_scaled)
#     future_pred = scaler.inverse_transform(future_scaled.reshape(-1, 1)).flatten()

#     # ---- IMPORTANT: dates based on latest raw date, not weekly bucket ----
#     future_dates = [last_raw_date + pd.Timedelta(weeks=i+1) for i in range(steps_ahead)]

#     next4_lstm_df = pd.DataFrame({
#         "ds": future_dates,
#         "yhat_lstm": future_pred
#     })
#     next4_lstm_df.to_csv(NEXT4W_LSTM_PATH, index=False)
#     print(f"Saved next 4-week LSTM forecast (total sales) to {NEXT4W_LSTM_PATH}")

#     # Save model + scaler
#     model.save(LSTM_MODEL_PATH)
#     joblib.dump(scaler, LSTM_SCALER_PATH)
#     print(f"Saved LSTM weekly model to {LSTM_MODEL_PATH}")
#     print(f"Saved LSTM scaler to {LSTM_SCALER_PATH}")

#     # Save metrics
#     metrics_df = pd.DataFrame([metrics])
#     metrics_df.to_csv(LSTM_METRICS_PATH, index=False)
#     print(f"Saved LSTM forecast metrics to {LSTM_METRICS_PATH}")

#     return model, metrics, next4_lstm_df

# # =========================================================
# # 4. SEASON PEAKS, SHOCKS, SIMPLE ANOMALIES (ON DAILY)
# # =========================================================

# def detect_peaks_and_shocks(daily: pd.DataFrame):
#     df = daily.copy().sort_values("ds")
#     df["rolling_mean_7"] = df["y"].rolling(window=7, min_periods=3).mean()
#     df["rolling_std_7"] = df["y"].rolling(window=7, min_periods=3).std()

#     df["z_score"] = (df["y"] - df["rolling_mean_7"]) / df["rolling_std_7"]
#     peaks = df[df["z_score"] > 2.5]

#     df["diff"] = df["y"].diff()
#     shock_threshold = df["diff"].abs().quantile(0.99)
#     shocks = df[df["diff"].abs() > shock_threshold]

#     print(f"\nDetected {len(peaks)} seasonal peaks (z_score > 2.5)")
#     print(f"Detected {len(shocks)} strong shocks (top 1% changes)")

#     peaks.to_csv(ARTIFACTS_DIR / "peaks.csv", index=False)
#     shocks.to_csv(ARTIFACTS_DIR / "shocks.csv", index=False)

#     return peaks, shocks

# def detect_anomalies(daily: pd.DataFrame):
#     """
#     Simple anomaly detection using deviation from 7-day rolling mean.
#     """
#     df = daily.copy().sort_values("ds")
#     df["rolling_mean_7"] = df["y"].rolling(window=7, min_periods=5).mean()
#     df["rolling_std_7"] = df["y"].rolling(window=7, min_periods=5).std()

#     df["z_score"] = (df["y"] - df["rolling_mean_7"]) / df["rolling_std_7"]
#     anomalies = df[df["z_score"].abs() > 3]

#     anomalies.to_csv(ARTIFACTS_DIR / "anomalies_daily.csv", index=False)
#     print(f"Saved {len(anomalies)} anomalies (|z| > 3) to artifacts/anomalies_daily.csv")

#     return anomalies

# # =========================================================
# # 5. RFM SEGMENTATION (RULE-BASED + KMEANS)
# # =========================================================

# def compute_rfm(df: pd.DataFrame) -> pd.DataFrame:
#     reference_date = df[DATE_COL].max()
#     print("\nRFM reference date:", reference_date)

#     rfm = (
#         df.groupby(CUSTOMER_COL)
#           .agg({
#               DATE_COL: lambda x: (reference_date - x.max()).days,
#               INVOICE_COL: "nunique",
#               "SalesAmount": "sum"
#           })
#           .rename(columns={
#               DATE_COL: "Recency",
#               INVOICE_COL: "Frequency",
#               "SalesAmount": "Monetary"
#           })
#           .reset_index()
#     )

#     rfm = rfm[rfm["Monetary"] > 0]
#     print("RFM customers:", len(rfm))
#     return rfm

# def rfm_rule_based(rfm: pd.DataFrame) -> pd.DataFrame:
#     rfm = rfm.copy()

#     r_quartiles = pd.qcut(rfm["Recency"], 4, labels=[4, 3, 2, 1])
#     f_quartiles = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4])
#     m_quartiles = pd.qcut(rfm["Monetary"], 4, labels=[1, 2, 3, 4])

#     rfm["R_score"] = r_quartiles.astype(int)
#     rfm["F_score"] = f_quartiles.astype(int)
#     rfm["M_score"] = m_quartiles.astype(int)

#     rfm["RFM_score"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]

#     def assign_segment(row):
#         if row["RFM_score"] >= 10:
#             return "Champions"
#         elif row["RFM_score"] >= 8:
#             return "Loyal Customers"
#         elif row["RFM_score"] >= 6:
#             return "Potential Loyalists"
#         elif row["RFM_score"] >= 4:
#             return "At Risk"
#         else:
#             return "Lost Customers"

#     rfm["Segment"] = rfm.apply(assign_segment, axis=1)

#     return rfm

# def rfm_kmeans(rfm: pd.DataFrame, n_clusters: int = 5):
#     rfm_log = rfm[["Recency", "Frequency", "Monetary"]].copy()
#     rfm_log["Recency"] = np.log1p(rfm_log["Recency"])
#     rfm_log["Frequency"] = np.log1p(rfm_log["Frequency"])
#     rfm_log["Monetary"] = np.log1p(rfm_log["Monetary"])

#     scaler = StandardScaler()
#     rfm_scaled = scaler.fit_transform(rfm_log)

#     kmeans = KMeans(n_clusters=n_clusters, random_state=42)
#     rfm["Cluster"] = kmeans.fit_predict(rfm_scaled)

#     rfm["Score"] = (-rfm_log["Recency"]) + rfm_log["Frequency"] + rfm_log["Monetary"]
#     cluster_scores = (
#         rfm.groupby("Cluster")["Score"]
#            .mean()
#            .sort_values(ascending=False)
#            .reset_index()
#     )
#     cluster_scores["Rank"] = cluster_scores["Score"].rank(ascending=False, method="dense").astype(int)

#     cluster_to_segment = {}
#     for _, row in cluster_scores.iterrows():
#         if row["Rank"] == 1:
#             label = "Champions"
#         elif row["Rank"] == 2:
#             label = "Loyal Customers"
#         elif row["Rank"] == 3:
#             label = "Potential Loyalists"
#         elif row["Rank"] == 4:
#             label = "At Risk"
#         else:
#             label = "Lost Customers"
#         cluster_to_segment[row["Cluster"]] = label

#     rfm["Segment"] = rfm["Cluster"].map(cluster_to_segment)

#     SEGMENT_OFFERS = {
#         "Champions": "Offer 15–20% VIP discount and early access.",
#         "Loyal Customers": "Offer 10% loyalty discount + referral bonus.",
#         "Potential Loyalists": "Send personalized recommendations + 5–10% coupon.",
#         "At Risk": "Re-engagement campaign with 10–12% win-back offer.",
#         "Lost Customers": "Strong limited-time reactivation coupon.",
#     }
#     rfm["Offer"] = rfm["Segment"].map(SEGMENT_OFFERS)

#     joblib.dump(
#         {"scaler": scaler, "kmeans": kmeans},
#         MODELS_DIR / "rfm_kmeans.pkl"
#     )
#     print(f"Saved RFM KMeans model to {MODELS_DIR / 'rfm_kmeans.pkl'}")

#     return rfm

# def plot_customer_segmentation_pie(rfm_df, file_path):
#     """
#     Pie chart of RFM customer segments.
#     """
#     segment_counts = rfm_df["Segment"].value_counts()

#     plt.figure(figsize=(8, 8))
#     plt.pie(
#         segment_counts,
#         labels=segment_counts.index,
#         autopct="%1.1f%%",
#         startangle=140
#     )
#     plt.title("Customer Segmentation (RFM)")
#     plt.tight_layout()
#     plt.savefig(file_path)
#     plt.close()
#     print(f"Saved pie chart: {file_path}")

# # =========================================================
# # 6. MAIN DRIVER
# # =========================================================

# def main():
#     TEST_POINTS = 4  # 4-week evaluation horizon

#     # 1. Load raw data
#     df_raw = load_raw_data()

#     # 2. Clean data
#     df = basic_cleaning(df_raw)

#     # 3. Save cleaned data
#     df.to_csv(CLEANED_DATA_PATH, index=False)
#     print(f"Saved cleaned data to {CLEANED_DATA_PATH}")

#     # 4. EDA on cleaned data (also get EDA dfs for plots)
#     monthly_sales, top_products, top_countries = perform_eda(df)

#     # Latest raw date for anchoring future weeks
#     last_raw_date = df[DATE_COL].max()
#     print(f"\nLatest date in dataset (raw): {last_raw_date}")

#     # 5. Aggregations
#     daily = build_daily_sales(df)
#     weekly = build_weekly_sales(df)
#     cat_sales = build_category_sales(df)
#     country_sales = build_country_sales(df)

#     daily.to_csv(DAILY_SALES_PATH, index=False)
#     weekly.to_csv(WEEKLY_SALES_PATH, index=False)
#     cat_sales.to_csv(CATEGORY_SALES_PATH, index=False)
#     country_sales.to_csv(COUNTRY_SALES_PATH, index=False)

#     print(f"\nSaved daily sales to    {DAILY_SALES_PATH}")
#     print(f"Saved weekly sales to   {WEEKLY_SALES_PATH}")
#     print(f"Saved category sales to {CATEGORY_SALES_PATH}")
#     print(f"Saved country sales to  {COUNTRY_SALES_PATH}")

#     # ------ PLOTS for artifacts ------

#     # Daily sales time series
#     plot_time_series(
#         daily,
#         date_col="ds",
#         value_col="y",
#         title="Daily Sales",
#         y_label="SalesAmount",
#         file_path=PLOTS_DIR / "daily_sales.png"
#     )

#     # Weekly sales time series
#     plot_time_series(
#         weekly,
#         date_col="ds",
#         value_col="y",
#         title="Weekly Sales",
#         y_label="SalesAmount",
#         file_path=PLOTS_DIR / "weekly_sales.png"
#     )

#     # Monthly sales time series (from EDA)
#     plot_time_series(
#         monthly_sales,
#         date_col="InvoiceMonth",
#         value_col="SalesAmount",
#         title="Monthly Sales",
#         y_label="SalesAmount",
#         file_path=PLOTS_DIR / "monthly_sales.png"
#     )

#     # Top products bar plot
#     plot_bar(
#         top_products,
#         x_col=DESC_COL,
#         y_col="SalesAmount",
#         title="Top 20 Products by Sales",
#         x_label="Product Description",
#         y_label="SalesAmount",
#         file_path=PLOTS_DIR / "top_products.png",
#         rotation=75
#     )

#     # Top countries bar plot
#     plot_bar(
#         top_countries,
#         x_col=COUNTRY_COL,
#         y_col="SalesAmount",
#         title="Top 20 Countries by Sales",
#         x_label="Country",
#         y_label="SalesAmount",
#         file_path=PLOTS_DIR / "top_countries.png",
#         rotation=45
#     )

#     # 6. LSTM model on WEEKLY data (4-week evaluation + 4-week future forecast)
#     lstm_metrics = None
#     next4_lstm_df = None
#     if tf is not None:
#         try:
#             lstm_model, lstm_metrics, next4_lstm_df = train_lstm_forecaster(
#                 weekly,
#                 last_raw_date=last_raw_date,
#                 lookback=12,
#                 test_points=TEST_POINTS
#             )
#         except Exception as e:
#             print("⚠ LSTM training failed due to:", e)
#     else:
#         print("⚠ Skipping LSTM: TensorFlow not available or import failed.")

#     if lstm_metrics and lstm_metrics.get("accuracy_pct") is not None:
#         print(f"➡ Final Weekly Forecast Accuracy (LSTM, 100 - MAPE): {lstm_metrics['accuracy_pct']:.2f}%")
#         print(f"➡ Next 4-week LSTM forecast (total) saved to: {NEXT4W_LSTM_PATH}")

#     # LSTM forecast plot (history + next 4 weeks)
#     if next4_lstm_df is not None:
#         plot_lstm_forecast(
#             weekly_df=weekly,
#             forecast_df=next4_lstm_df,
#             file_path=PLOTS_DIR / "lstm_forecast_next4weeks.png"
#         )

#     # 6b. Demographic breakdown of forecast (Country / Category)
#     if next4_lstm_df is not None:
#         # Country shares
#         country_share = (
#             df.groupby(COUNTRY_COL)["SalesAmount"]
#               .sum()
#         )
#         country_share = country_share / country_share.sum()
#         country_share = country_share.sort_values(ascending=False)

#         # Category (product description) shares
#         category_share = (
#             df.groupby(DESC_COL)["SalesAmount"]
#               .sum()
#         )
#         category_share = category_share / category_share.sum()
#         category_share = category_share.sort_values(ascending=False)

#         # For practicality, only use top N for each demographic
#         TOP_N_COUNTRIES = 5
#         TOP_N_CATEGORIES = 5

#         top_country_share = country_share.head(TOP_N_COUNTRIES)
#         top_category_share = category_share.head(TOP_N_CATEGORIES)

#         # Expand next4_lstm_df for countries
#         rows_country = []
#         for _, row in next4_lstm_df.iterrows():
#             ds = row["ds"]
#             total_pred = row["yhat_lstm"]
#             for country, share in top_country_share.items():
#                 rows_country.append({
#                     "ds": ds,
#                     "Country": country,
#                     "share": float(share),
#                     "yhat_lstm_country": float(total_pred * share)
#                 })
#         next4_country_df = pd.DataFrame(rows_country)
#         next4_country_df.to_csv(NEXT4W_LSTM_BY_COUNTRY_PATH, index=False)
#         print(f"Saved next 4-week LSTM forecast by COUNTRY to {NEXT4W_LSTM_BY_COUNTRY_PATH}")

#         # Expand next4_lstm_df for categories (products)
#         rows_category = []
#         for _, row in next4_lstm_df.iterrows():
#             ds = row["ds"]
#             total_pred = row["yhat_lstm"]
#             for desc, share in top_category_share.items():
#                 rows_category.append({
#                     "ds": ds,
#                     "Description": desc,
#                     "share": float(share),
#                     "yhat_lstm_category": float(total_pred * share)
#                 })
#         next4_category_df = pd.DataFrame(rows_category)
#         next4_category_df.to_csv(NEXT4W_LSTM_BY_CATEGORY_PATH, index=False)
#         print(f"Saved next 4-week LSTM forecast by CATEGORY to {NEXT4W_LSTM_BY_CATEGORY_PATH}")

#     # 7. Peaks, shocks, anomalies (daily-level)
#     peaks, shocks = detect_peaks_and_shocks(daily)
#     anomalies = detect_anomalies(daily)

#     # 8. RFM + segmentation
#     rfm = compute_rfm(df)
#     rfm_rule = rfm_rule_based(rfm)
#     rfm_rule.to_csv(ARTIFACTS_DIR / "rfm_segments_rule_based.csv", index=False)
#     print(f"Saved rule-based RFM segments to {ARTIFACTS_DIR / 'rfm_segments_rule_based.csv'}")

#     # Customer segmentation pie chart
#     plot_customer_segmentation_pie(
#         rfm_rule,
#         PLOTS_DIR / "customer_segments_pie.png"
#     )

#     rfm_km = rfm_kmeans(rfm, n_clusters=5)
#     rfm_km.to_csv(ARTIFACTS_DIR / "rfm_segments_kmeans.csv", index=False)
#     print(f"Saved KMeans RFM segments to {ARTIFACTS_DIR / 'rfm_segments_kmeans.csv'}")

#     print("\n✅ ALL TASKS COMPLETED (CLEANING + EDA + LSTM 4-WEEK FORECAST + DEMOGRAPHICS + CRM + PLOTS):")
#     print("- Data cleaned and saved")
#     print("- EDA CSVs (missing, describe, monthly trend, top products, top countries) saved")
#     print(f"- Plots saved in: {PLOTS_DIR}")
#     if lstm_metrics and lstm_metrics.get("accuracy_pct") is not None:
#         print("- LSTM weekly forecast + metrics (4-week test)")
#         print(f"  ▸ LSTM Accuracy (100 - MAPE): {lstm_metrics['accuracy_pct']:.2f}%")
#         print(f"- Next 4-week LSTM TOTAL forecast CSV: {NEXT4W_LSTM_PATH}")
#         print(f"- Next 4-week LSTM forecast BY COUNTRY: {NEXT4W_LSTM_BY_COUNTRY_PATH}")
#         print(f"- Next 4-week LSTM forecast BY CATEGORY: {NEXT4W_LSTM_BY_CATEGORY_PATH}")
#         print(f"- LSTM forecast plot: {PLOTS_DIR / 'lstm_forecast_next4weeks.png'}")
#     else:
#         print("- LSTM metrics: not available (see earlier warnings).")
#     print("- Peaks + shocks + anomalies saved (daily)")
#     print("- RFM (rule-based + KMeans) saved")
#     print("- Aggregates for daily/weekly/country/category saved")
#     print(f"- LSTM metrics stored at:   {LSTM_METRICS_PATH}")

#     # --------- RETURN SUMMARY FOR API USE ---------
#     summary = {
#         "cleaned_data_path": str(CLEANED_DATA_PATH),
#         "daily_sales_path": str(DAILY_SALES_PATH),
#         "weekly_sales_path": str(WEEKLY_SALES_PATH),
#         "category_sales_path": str(CATEGORY_SALES_PATH),
#         "country_sales_path": str(COUNTRY_SALES_PATH),
#         "eda": {
#             "missing_path": str(EDA_MISSING_PATH),
#             "describe_path": str(EDA_DESCRIBE_PATH),
#             "monthly_sales_path": str(EDA_MONTHLY_SALES_PATH),
#             "top_products_path": str(EDA_TOP_PRODUCTS_PATH),
#             "top_countries_path": str(EDA_TOP_COUNTRIES_PATH),
#         },
#         "lstm": {
#             "metrics": lstm_metrics,
#             "metrics_path": str(LSTM_METRICS_PATH),
#             "total_forecast_path": str(NEXT4W_LSTM_PATH),
#             "by_country_path": str(NEXT4W_LSTM_BY_COUNTRY_PATH),
#             "by_category_path": str(NEXT4W_LSTM_BY_CATEGORY_PATH) if next4_lstm_df is not None else None,
#         } if lstm_metrics is not None else None,
#         "rfm": {
#             "rule_based_path": str(ARTIFACTS_DIR / "rfm_segments_rule_based.csv"),
#             "kmeans_path": str(ARTIFACTS_DIR / "rfm_segments_kmeans.csv"),
#         },
#         "plots": {
#             "daily_sales": str(PLOTS_DIR / "daily_sales.png"),
#             "weekly_sales": str(PLOTS_DIR / "weekly_sales.png"),
#             "monthly_sales": str(PLOTS_DIR / "monthly_sales.png"),
#             "top_products": str(PLOTS_DIR / "top_products.png"),
#             "top_countries": str(PLOTS_DIR / "top_countries.png"),
#             "lstm_forecast_next4weeks": str(PLOTS_DIR / "lstm_forecast_next4weeks.png") if next4_lstm_df is not None else None,
#             "customer_segments_pie": str(PLOTS_DIR / "customer_segments_pie.png"),
#         },
#         "peaks_path": str(ARTIFACTS_DIR / "peaks.csv"),
#         "shocks_path": str(ARTIFACTS_DIR / "shocks.csv"),
#         "anomalies_path": str(ARTIFACTS_DIR / "anomalies_daily.csv"),
#     }

#     return summary

# # =========================================================
# # FLASK APP FOR REACT INTEGRATION
# # =========================================================

# app = Flask(__name__)
# CORS(app)  # allow requests from your React dev server (e.g. localhost:5173)

# @app.route("/api/run-pipeline", methods=["POST", "GET"])
# def run_pipeline_endpoint():
#     """
#     Runs the full data pipeline and returns key summary info as JSON.
#     Your React app can call this endpoint if you want to force retrain.
#     """
#     try:
#         summary = main()
#         return jsonify({
#             "status": "success",
#             "summary": summary
#         }), 200
#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

# @app.route("/api/forecast-summary", methods=["GET"])
# def forecast_summary():
#     """
#     Return forecast metrics + weekly sales data for charts.

#     weeklySalesData is shaped for ForecastChart:
#       [{ week: "Week 1", actual: <number>, forecast: <number|null> }, ...]
#     Up to last 12 weeks, so your 4/8/12 weeks dropdown works properly.

#     ⚠ NEW:
#     - Also logs the TOTAL forecast for next 4 weeks to:
#         • ForecastLogger smart contract on Ganache
#         • Firebase Firestore (forecast_logs collection)
#       but now with fixed-window rate limiting.
#     """
#     try:
#         # Ensure pipeline artifacts exist; normally already done at startup
#         if (
#             not NEXT4W_LSTM_PATH.exists()
#             or not WEEKLY_SALES_PATH.exists()
#             or not LSTM_METRICS_PATH.exists()
#         ):
#             main()

#         # Load metrics
#         if LSTM_METRICS_PATH.exists():
#             metrics_df = pd.read_csv(LSTM_METRICS_PATH)
#             metrics = metrics_df.iloc[0].to_dict()
#         else:
#             metrics = {}

#         # Load forecast CSV
#         forecast_df = None
#         total_forecast = None
#         if NEXT4W_LSTM_PATH.exists():
#             forecast_df = pd.read_csv(NEXT4W_LSTM_PATH)
#             if "yhat_lstm" in forecast_df.columns:
#                 total_forecast = float(forecast_df["yhat_lstm"].sum())

#         weeklySalesData = []

#         # Load weekly actuals (up to last 12 points)
#         if WEEKLY_SALES_PATH.exists():
#             weekly_df = pd.read_csv(WEEKLY_SALES_PATH)
#             if "ds" in weekly_df.columns and "y" in weekly_df.columns:
#                 weekly_df = weekly_df.sort_values("ds")
#                 n = len(weekly_df)
#                 if n > 0:
#                     last_n = min(12, n)
#                     recent_df = weekly_df.tail(last_n).reset_index(drop=True)

#                     # map forecast (4 points) to last 4 actual weeks in this window
#                     forecast_values = None
#                     if forecast_df is not None and "yhat_lstm" in forecast_df.columns:
#                         forecast_values = forecast_df["yhat_lstm"].values
#                     forecast_len = len(forecast_values) if forecast_values is not None else 0

#                     for idx, row in recent_df.iterrows():
#                         forecast_val = None
#                         if forecast_values is not None and forecast_len > 0:
#                             # last forecast_len positions in this recent window
#                             if idx >= last_n - forecast_len:
#                                 f_index = idx - (last_n - forecast_len)
#                                 if 0 <= f_index < forecast_len:
#                                     forecast_val = float(forecast_values[f_index])

#                         weeklySalesData.append({
#                             "week": f"Week {idx+1}",
#                             "actual": float(row["y"]),
#                             "forecast": forecast_val,
#                         })

#         # ===== CALCULATE KPI METRICS =====
#         kpi_metrics = {
#             "prev_4_weeks_total": None,
#             "last_4_weeks_total": None,
#             "next_4_weeks_forecast": total_forecast,
#             "sales_change_pct": None,
#             "forecast_change_pct": None,
#             "accuracy_pct": metrics.get("accuracy_pct"),
#         }
        
#         # Calculate previous 4 weeks and last 4 weeks
#         if WEEKLY_SALES_PATH.exists():
#             try:
#                 weekly_df_full = pd.read_csv(WEEKLY_SALES_PATH)
#                 if len(weekly_df_full) >= 8:
#                     weekly_df_full = weekly_df_full.sort_values("ds")
#                     prev_4_weeks = weekly_df_full.iloc[-8:-4]["y"].sum()
#                     last_4_weeks = weekly_df_full.iloc[-4:]["y"].sum()
                    
#                     kpi_metrics["prev_4_weeks_total"] = float(prev_4_weeks)
#                     kpi_metrics["last_4_weeks_total"] = float(last_4_weeks)
                    
#                     # Calculate % change (last vs prev)
#                     if prev_4_weeks > 0:
#                         sales_change = ((last_4_weeks - prev_4_weeks) / prev_4_weeks) * 100
#                         kpi_metrics["sales_change_pct"] = float(sales_change)
                    
#                     # Calculate % change (forecast vs last)
#                     if last_4_weeks > 0 and total_forecast is not None:
#                         forecast_change = ((total_forecast - last_4_weeks) / last_4_weeks) * 100
#                         kpi_metrics["forecast_change_pct"] = float(forecast_change)
#             except Exception as e:
#                 print(f"Error calculating KPI metrics: {e}")
        
#         # Merge KPI metrics with loaded metrics
#         metrics.update(kpi_metrics)

#         # ===== NEW: log to blockchain + firebase with fixed-window rate limiting =====
#         blockchain_meta = None
#         rate_limit_info = {
#             "active": False,
#             "cooldownSeconds": 0
#         }
#         try:
#             if total_forecast is not None:
#                 allowed, cooldown = check_rate_limit()
#                 if allowed:
#                     blockchain_meta = log_forecast_onchain_and_firebase(
#                         total_forecast,
#                         model_version="lstm_weekly_v1"
#                     )
#                 else:
#                     rate_limit_info["active"] = True
#                     rate_limit_info["cooldownSeconds"] = int(cooldown)
#                     print(f"⏳ Skipping on-chain/Firebase log due to rate limit. Cooldown ~{cooldown:.1f}s left.")
#         except Exception as e:
#             print(f"⚠ Error logging forecast to blockchain/Firebase: {e}")
#             blockchain_meta = None

#         resp = {
#             "status": "success",
#             "total_forecast": total_forecast,
#             "total_forecast_formatted": (
#                 f"₹{int(round(total_forecast)):,}" if total_forecast is not None else None
#             ),
#             "metrics": metrics,
#             "weeklySalesData": weeklySalesData,
#             "blockchain": blockchain_meta,
#             "rateLimit": rate_limit_info,
#         }
#         return jsonify(resp), 200
#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#         }), 500

# @app.route("/api/segments-summary", methods=["GET"])
# def segments_summary():
#     """
#     Return segment distribution + sample customers derived from RFM.

#     segments: [{ name, value }]
#     customers: [{ id, name, segment, recency, frequency, monetary }]
#     """
#     try:
#         rfm_path = ARTIFACTS_DIR / "rfm_segments_rule_based.csv"
#         # Ensure RFM artifacts exist
#         if not rfm_path.exists():
#             main()

#         if not rfm_path.exists():
#             return jsonify({
#                 "status": "error",
#                 "message": "RFM segments file not found even after pipeline run.",
#             }), 500

#         rfm_df = pd.read_csv(rfm_path)

#         if "Segment" not in rfm_df.columns:
#             return jsonify({
#                 "status": "error",
#                 "message": "Segment column missing in RFM file.",
#             }), 500

#         # Segment distribution: use ALL segments (no 'Others' merge)
#         seg_counts = rfm_df["Segment"].value_counts()
#         segments = [
#             {"name": str(seg), "value": int(cnt)}
#             for seg, cnt in seg_counts.items()
#         ]

#         # All customers (you can slice if you want to limit)
#         customers = []
#         for _, row in rfm_df.iterrows():
#             cust_id = row.get(CUSTOMER_COL, None)
#             customers.append({
#                 "id": str(cust_id) if cust_id is not None else "",
#                 "name": f"Customer {cust_id}" if cust_id is not None else "Customer",
#                 "segment": row.get("Segment", ""),
#                 "recency": int(row.get("Recency", 0)),
#                 "frequency": int(row.get("Frequency", 0)),
#                 "monetary": float(row.get("Monetary", 0.0)),
#             })

#         return jsonify({
#             "status": "success",
#             "segments": segments,
#             "customers": customers,
#         }), 200
#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#         }), 500

# # =========================================================
# # NEW: EXPLICIT ENDPOINT TO LOG LATEST FORECAST ON-CHAIN
# # =========================================================

# @app.route("/api/log-forecast", methods=["POST"])
# def log_forecast_endpoint():
#     """
#     Explicit endpoint to force logging the latest 4-week forecast
#     to blockchain (Ganache) + Firebase.

#     Request body (optional):
#       { "modelVersion": "lstm_weekly_v1", "secret": "API_SECRET_KEY" }

#     It still works without body; modelVersion defaults, and secret is optional
#     for local dev (only checked if provided).
#     """
#     try:
#         body = request.get_json(silent=True) or {}
#         model_version = body.get("modelVersion", "lstm_weekly_v1")
#         secret = body.get("secret")

#         # Very simple optional protection
#         if secret is not None and secret != API_SECRET_KEY:
#             return jsonify({
#                 "status": "error",
#                 "message": "Invalid API secret."
#             }), 403

#         # Rate limit for explicit log endpoint as well
#         allowed, cooldown = check_rate_limit()
#         if not allowed:
#             return jsonify({
#                 "status": "error",
#                 "message": f"Rate limit exceeded. Try again in {int(cooldown)} seconds.",
#                 "rateLimit": {
#                     "active": True,
#                     "cooldownSeconds": int(cooldown)
#                 }
#             }), 429

#         # Ensure forecast artifacts exist
#         if not NEXT4W_LSTM_PATH.exists() or not LSTM_METRICS_PATH.exists():
#             main()

#         total_forecast = None
#         if NEXT4W_LSTM_PATH.exists():
#             forecast_df = pd.read_csv(NEXT4W_LSTM_PATH)
#             if "yhat_lstm" in forecast_df.columns:
#                 total_forecast = float(forecast_df["yhat_lstm"].sum())

#         if total_forecast is None:
#             return jsonify({
#                 "status": "error",
#                 "message": "No forecast available to log."
#             }), 400

#         meta = log_forecast_onchain_and_firebase(total_forecast, model_version=model_version)

#         return jsonify({
#             "status": "success",
#             "total_forecast": total_forecast,
#             "total_forecast_formatted": f"₹{int(round(total_forecast)):,}",
#             "blockchain": meta,
#             "rateLimit": {
#                 "active": False,
#                 "cooldownSeconds": LOG_RATE_LIMIT_WINDOW_SECONDS
#             }
#         }), 200

#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": str(e),
#         }), 500

# # =========================================================
# # APP ENTRYPOINT
# # =========================================================

# if __name__ == "__main__":
#     # Initialize integrations once at startup (best effort)
#     init_firebase()
#     init_blockchain()

#     # ✅ Run pipeline & train model ONCE at startup, then start Flask
#     print("🚀 Running initial data pipeline & model training...")
#     try:
#         main()
#         print("✅ Pipeline ready. Starting Flask server...")
#     except Exception as e:
#         print("⚠ Initial pipeline failed:", e)

#     app.run(host="0.0.0.0", port=5000, debug=True)


# # top of backend.py — must be first lines (before importing matplotlib.pyplot or anything that may import matplotlib)
# import os
# os.environ["PYTHONHASHSEED"] = "42"
# os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# # Force non-interactive Matplotlib very early
# os.environ["MPLBACKEND"] = "Agg"   # env var fallback
# import matplotlib
# matplotlib.use("Agg")

# from pathlib import Path
# import random
# import numpy as np
# import pandas as pd
# import joblib
# import time
# from threading import Lock  # for rate limiting

# from sklearn.metrics import mean_squared_error, r2_score
# from sklearn.preprocessing import StandardScaler
# from sklearn.cluster import KMeans

# import matplotlib.pyplot as plt  # <-- for plots

# # Flask imports
# from flask import Flask, jsonify, request
# from flask_cors import CORS

# # ---------------- NEW IMPORTS: ENV + BLOCKCHAIN + FIREBASE ----------------
# from dotenv import load_dotenv
# load_dotenv()

# from web3 import Web3
# import firebase_admin
# from firebase_admin import credentials, firestore

# # ======================= ENV CONFIG FOR INTEGRATIONS =======================

# FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")

# GANACHE_RPC_URL = os.getenv("GANACHE_RPC_URL", "http://127.0.0.1:7545")
# GANACHE_PRIVATE_KEY = os.getenv("GANACHE_PRIVATE_KEY")
# GANACHE_ACCOUNT_ADDRESS = os.getenv("GANACHE_ACCOUNT_ADDRESS")
# FORECAST_CONTRACT_ADDRESS = os.getenv("FORECAST_CONTRACT_ADDRESS")
# GANACHE_CHAIN_ID = int(os.getenv("GANACHE_CHAIN_ID", "1337"))

# API_SECRET_KEY = os.getenv("API_SECRET_KEY", "supersecret")

# # ===== RATE LIMIT CONFIG =====
# # Allow up to MAX_LOG_REQUESTS_PER_WINDOW logs every LOG_RATE_LIMIT_WINDOW_SECONDS seconds.
# # Default: 2 logs every 180 seconds (3 mins).
# MAX_LOG_REQUESTS_PER_WINDOW = int(os.getenv("LOG_MAX_REQUESTS_PER_WINDOW", "2"))
# LOG_RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("LOG_RATE_LIMIT_WINDOW_SECONDS", "180"))

# # Globals for integrations
# firebase_app = None
# firestore_client = None

# w3 = None
# forecast_contract = None
# blockchain_account_address = None
# blockchain_private_key = None

# # Globals for rate limiting state (fixed window)
# rate_limit_lock = Lock()
# window_start_ts = 0.0
# window_request_count = 0


# def check_rate_limit():
#   """
#   Fixed-window rate limit for *logging* to blockchain + Firebase.
#   """
#   global window_start_ts, window_request_count
#   now = time.time()
#   with rate_limit_lock:
#     # If window not started or expired -> reset window
#     if window_start_ts == 0.0 or (now - window_start_ts) >= LOG_RATE_LIMIT_WINDOW_SECONDS:
#       window_start_ts = now
#       window_request_count = 0

#     if window_request_count < MAX_LOG_REQUESTS_PER_WINDOW:
#       # Allow request inside current window
#       window_request_count += 1
#       return True, 0.0

#     # Window still active and max count reached -> rate limited
#     elapsed = now - window_start_ts
#     cooldown = max(0.0, LOG_RATE_LIMIT_WINDOW_SECONDS - elapsed)
#     return False, cooldown

# # ======================= INITIALIZE FIREBASE =======================

# def init_firebase():
#   """
#   Initialize Firebase Admin SDK (Firestore).
#   Uses FIREBASE_CREDENTIALS path from .env.
#   """
#   global firebase_app, firestore_client

#   if firebase_app is not None:
#     return

#   if not FIREBASE_CREDENTIALS:
#     print("⚠ FIREBASE_CREDENTIALS not set. Firebase logging disabled.")
#     return

#   try:
#     cred = credentials.Certificate(FIREBASE_CREDENTIALS)
#     firebase_app = firebase_admin.initialize_app(cred)
#     firestore_client = firestore.client()
#     print("✅ Firebase initialized successfully.")
#   except Exception as e:
#     print(f"⚠ Firebase initialization failed: {e}")
#     firebase_app = None
#     firestore_client = None

# # ======================= INITIALIZE BLOCKCHAIN (GANACHE) =======================

# def get_forecast_logger_abi():
#   """
#   Minimal ABI for the ForecastLogger contract.
#   """
#   return [
#     {
#       "inputs": [],
#       "stateMutability": "nonpayable",
#       "type": "constructor"
#     },
#     {
#       "anonymous": False,
#       "inputs": [
#         {
#           "indexed": False,
#           "internalType": "uint256",
#           "name": "value",
#           "type": "uint256"
#         },
#         {
#           "indexed": False,
#           "internalType": "string",
#           "name": "modelVersion",
#           "type": "string"
#         },
#         {
#           "indexed": False,
#           "internalType": "uint256",
#           "name": "timestamp",
#           "type": "uint256"
#         }
#       ],
#       "name": "ForecastSaved",
#       "type": "event"
#     },
#     {
#       "inputs": [],
#       "name": "latestForecast",
#       "outputs": [
#         {
#           "internalType": "uint256",
#           "name": "",
#           "type": "uint256"
#         }
#       ],
#       "stateMutability": "view",
#       "type": "function"
#     },
#     {
#       "inputs": [],
#       "name": "latestModelVersion",
#       "outputs": [
#         {
#           "internalType": "string",
#           "name": "",
#           "type": "string"
#         }
#       ],
#       "stateMutability": "view",
#       "type": "function"
#     },
#     {
#       "inputs": [],
#       "name": "lastUpdatedAt",
#       "outputs": [
#         {
#           "internalType": "uint256",
#           "name": "",
#           "type": "uint256"
#         }
#       ],
#       "stateMutability": "view",
#       "type": "function"
#     },
#     {
#       "inputs": [
#         {
#           "internalType": "uint256",
#           "name": "_value",
#           "type": "uint256"
#         },
#         {
#           "internalType": "string",
#           "name": "_modelVersion",
#           "type": "string"
#         }
#       ],
#       "name": "saveForecast",
#       "outputs": [],
#       "stateMutability": "nonpayable",
#       "type": "function"
#     }
#   ]

# def init_blockchain():
#   """
#   Initialize Web3 + ForecastLogger contract instance using Ganache.
#   """
#   global w3, forecast_contract, blockchain_account_address, blockchain_private_key

#   if w3 is not None and forecast_contract is not None:
#     return

#   if not GANACHE_RPC_URL or not GANACHE_PRIVATE_KEY or not FORECAST_CONTRACT_ADDRESS:
#     print("⚠ Blockchain env vars missing (GANACHE_RPC_URL / GANACHE_PRIVATE_KEY / FORECAST_CONTRACT_ADDRESS).")
#     return

#   try:
#     w3_local = Web3(Web3.HTTPProvider(GANACHE_RPC_URL))
#     if not w3_local.is_connected():
#       print("⚠ Could not connect to Ganache RPC. Blockchain logging disabled.")
#       return

#     blockchain_private_key = GANACHE_PRIVATE_KEY

#     if GANACHE_ACCOUNT_ADDRESS:
#       blockchain_account_address = Web3.to_checksum_address(GANACHE_ACCOUNT_ADDRESS)
#     else:
#       acct = w3_local.eth.account.from_key(blockchain_private_key)
#       blockchain_account_address = acct.address

#     contract_address = Web3.to_checksum_address(FORECAST_CONTRACT_ADDRESS)
#     contract_abi = get_forecast_logger_abi()
#     contract_instance = w3_local.eth.contract(address=contract_address, abi=contract_abi)

#     w3 = w3_local
#     forecast_contract = contract_instance

#     print(f"✅ Connected to Ganache at {GANACHE_RPC_URL}")
#     print(f"✅ ForecastLogger contract at {contract_address}")
#     print(f"✅ Using account {blockchain_account_address}")
#   except Exception as e:
#     print(f"⚠ Blockchain init failed: {e}")
#     w3 = None
#     forecast_contract = None
#     blockchain_account_address = None
#     blockchain_private_key = None

# # ======================= LOG TO BLOCKCHAIN + FIREBASE =======================

# def log_forecast_onchain_and_firebase(total_forecast, model_version="lstm_weekly_v1"):
#   """
#   Take the numeric 'total_forecast' (next 4 weeks total sales),
#   push it to:
#     1) ForecastLogger smart contract (Ganache)
#     2) Firebase Firestore 'forecast_logs' collection
#   """
#   result = {
#     "onchain": False,
#     "firebase": False,
#     "tx_hash": None,
#     "logged_value_int": None,
#     "model_version": model_version,
#   }

#   if total_forecast is None:
#     print("⚠ No forecast value to log on-chain / Firebase.")
#     return result

#   # Normalize to int for uint256 (we store INR with no decimals)
#   try:
#     value_int = int(round(float(total_forecast)))
#   except Exception:
#     print("⚠ Could not convert forecast to integer for blockchain.")
#     return result

#   result["logged_value_int"] = value_int

#   # --- Initialize integrations (lazy) ---
#   init_blockchain()
#   init_firebase()

#   # --- 1) Blockchain ---
#   if (
#     w3 is not None
#     and forecast_contract is not None
#     and blockchain_account_address is not None
#     and blockchain_private_key is not None
#   ):
#     try:
#       nonce = w3.eth.get_transaction_count(blockchain_account_address)

#       tx = forecast_contract.functions.saveForecast(
#         value_int,
#         model_version
#       ).build_transaction(
#         {
#           "from": blockchain_account_address,
#           "nonce": nonce,
#           "gas": 300000,
#           "gasPrice": w3.eth.gas_price,
#           "chainId": GANACHE_CHAIN_ID,
#         }
#       )

#       signed_tx = w3.eth.account.sign_transaction(tx, private_key=blockchain_private_key)

#       tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

#       receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

#       print(f"✅ Saved forecast on-chain. Tx hash: {tx_hash.hex()}")
#       print(f"   Block: {receipt.blockNumber}, Gas used: {receipt.gasUsed}")

#       result["onchain"] = True
#       result["tx_hash"] = tx_hash.hex()
#     except Exception as e:
#       print(f"⚠ Blockchain logging failed: {e}")
#   else:
#     print("⚠ Blockchain not initialized; skipping on-chain logging.")

#   # --- 2) Firebase ---
#   if firestore_client is not None:
#     try:
#       doc = {
#         "value_int": value_int,
#         "value_raw": float(total_forecast),
#         "currency": "INR",
#         "model_version": model_version,
#         "tx_hash": result["tx_hash"],
#         "source": "backend_forecast_summary",
#         "created_at": firestore.SERVER_TIMESTAMP,
#       }
#       firestore_client.collection("forecast_logs").add(doc)
#       print("✅ Saved forecast to Firebase Firestore (forecast_logs).")
#       result["firebase"] = True
#     except Exception as e:
#       print(f"⚠ Firebase logging failed: {e}")
#   else:
#     print("⚠ Firestore client not available; skipping Firebase logging.")

#   return result

# # =======================
# # TensorFlow / LSTM
# # =======================
# try:
#   import tensorflow as tf
#   TF_IMPORT_ERROR = None

#   # set seeds for reproducibility
#   random.seed(42)
#   np.random.seed(42)
#   tf.random.set_seed(42)
# except Exception as e:
#   tf = None
#   TF_IMPORT_ERROR = e
#   print("⚠ TensorFlow import failed. LSTM model will be skipped.")
#   print("   Reason:", e)

# # =========================================================
# # CONFIG – EDIT ONLY PATH IF NEEDED
# # =========================================================

# # ⚠ Default CSV path (used on startup / /api/run-pipeline)
# CSV_PATH = Path(r"online_retail.csv")  # default dataset
# # CSV_PATH = Path(r"Online_Retail_new.csv")  # you can still override this if you want

# DATE_COL = "InvoiceDate"
# QTY_COL = "Quantity"
# PRICE_COL = "Price"
# CUSTOMER_COL = "Customer ID"
# INVOICE_COL = "Invoice"
# COUNTRY_COL = "Country"
# DESC_COL = "Description"

# MODELS_DIR = Path("models")
# ARTIFACTS_DIR = Path("artifacts")
# MODELS_DIR.mkdir(exist_ok=True, parents=True)
# ARTIFACTS_DIR.mkdir(exist_ok=True, parents=True)

# DAILY_SALES_PATH = ARTIFACTS_DIR / "daily_sales.csv"
# WEEKLY_SALES_PATH = ARTIFACTS_DIR / "weekly_sales.csv"
# CATEGORY_SALES_PATH = ARTIFACTS_DIR / "category_sales.csv"
# COUNTRY_SALES_PATH = ARTIFACTS_DIR / "country_sales.csv"

# CLEANED_DATA_PATH = ARTIFACTS_DIR / "cleaned_online_retail.csv"

# LSTM_MODEL_PATH = MODELS_DIR / "lstm_model_weekly.h5"
# LSTM_SCALER_PATH = MODELS_DIR / "lstm_scaler_weekly.pkl"
# LSTM_METRICS_PATH = ARTIFACTS_DIR / "lstm_forecast_metrics_weekly.csv"

# # EDA outputs
# EDA_MISSING_PATH = ARTIFACTS_DIR / "eda_missing_values.csv"
# EDA_DESCRIBE_PATH = ARTIFACTS_DIR / "eda_describe_all.csv"
# EDA_MONTHLY_SALES_PATH = ARTIFACTS_DIR / "eda_monthly_sales.csv"
# EDA_TOP_PRODUCTS_PATH = ARTIFACTS_DIR / "eda_top_products.csv"
# EDA_TOP_COUNTRIES_PATH = ARTIFACTS_DIR / "eda_top_countries.csv"

# # 4-week LSTM forecast outputs
# NEXT4W_LSTM_PATH = ARTIFACTS_DIR / "next4weeks_lstm.csv"
# NEXT4W_LSTM_BY_COUNTRY_PATH = ARTIFACTS_DIR / "next4weeks_lstm_by_country.csv"
# NEXT4W_LSTM_BY_CATEGORY_PATH = ARTIFACTS_DIR / "next4weeks_lstm_by_category.csv"

# # Plots output directory
# PLOTS_DIR = ARTIFACTS_DIR / "plots"
# PLOTS_DIR.mkdir(exist_ok=True, parents=True)

# # =========================================================
# # UTILS
# # =========================================================

# def mape(y_true, y_pred, eps=1e-3):
#   """
#   MAPE ignoring very small true values, to avoid exploding percentages.
#   """
#   y_true = np.array(y_true, dtype=float)
#   y_pred = np.array(y_pred, dtype=float)

#   mask = np.abs(y_true) > eps
#   if not np.any(mask):
#     return np.nan

#   return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

# # ---------------- PLOTTING HELPERS ----------------

# def plot_time_series(df, date_col, value_col, title, y_label, file_path):
#   plt.figure(figsize=(10, 5))
#   plt.plot(df[date_col], df[value_col])
#   plt.title(title)
#   plt.xlabel("Date")
#   plt.ylabel(y_label)
#   plt.grid(True, linestyle="--", alpha=0.5)
#   plt.tight_layout()
#   plt.savefig(file_path)
#   plt.close()
#   print(f"Saved plot: {file_path}")

# def plot_bar(df, x_col, y_col, title, x_label, y_label, file_path, rotation=45):
#   plt.figure(figsize=(10, 5))
#   plt.bar(df[x_col].astype(str), df[y_col])
#   plt.title(title)
#   plt.xlabel(x_label)
#   plt.ylabel(y_label)
#   plt.xticks(rotation=rotation, ha="right")
#   plt.tight_layout()
#   plt.savefig(file_path)
#   plt.close()
#   print(f"Saved plot: {file_path}")

# def plot_lstm_forecast(weekly_df, forecast_df, file_path, last_weeks_history=20):
#   weekly_df = weekly_df.sort_values("ds").copy()
#   hist_tail = weekly_df.tail(last_weeks_history)

#   plt.figure(figsize=(10, 5))
#   plt.plot(hist_tail["ds"], hist_tail["y"], label="Historical Weekly Sales")

#   plt.plot(
#     forecast_df["ds"],
#     forecast_df["yhat_lstm"],
#     marker="o",
#     linestyle="--",
#     label="Next 4 Weeks Forecast",
#   )

#   plt.title("Weekly Sales with Next 4-Week LSTM Forecast")
#   plt.xlabel("Date")
#   plt.ylabel("SalesAmount")
#   plt.grid(True, linestyle="--", alpha=0.5)
#   plt.legend()
#   plt.tight_layout()
#   plt.savefig(file_path)
#   plt.close()
#   print(f"Saved LSTM forecast plot: {file_path}")

# # =========================================================
# # 1. LOAD + CLEAN DATA
# # =========================================================

# def load_raw_data(csv_path=None):
#   """
#   Load raw CSV. If csv_path is None, use default CSV_PATH.
#   """
#   path = Path(csv_path) if csv_path is not None else CSV_PATH
#   print(f"Loading data from {path}")
#   df = pd.read_csv(path, encoding="ISO-8859-1")
#   print("Raw shape:", df.shape)
#   print("Columns:", df.columns.tolist())
#   return df

# def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
#   print("\n=== CLEANING: start ===")
#   df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")

#   initial_rows = len(df)

#   # drop cancelled invoices (Invoice starting with 'C')
#   if INVOICE_COL in df.columns:
#     df[INVOICE_COL] = df[INVOICE_COL].astype(str)
#     df = df[~df[INVOICE_COL].str.startswith("C")]
#     print(f"Removed cancelled invoices. Rows now: {len(df)}")

#   # drop rows with missing critical info
#   df = df.dropna(subset=[DATE_COL, QTY_COL, PRICE_COL])
#   print(f"After dropping rows with NA in [{DATE_COL}, {QTY_COL}, {PRICE_COL}]: {len(df)} rows")

#   # convert quantity and price to numeric (in case of bad strings)
#   df[QTY_COL] = pd.to_numeric(df[QTY_COL], errors="coerce")
#   df[PRICE_COL] = pd.to_numeric(df[PRICE_COL], errors="coerce")

#   df = df.dropna(subset=[QTY_COL, PRICE_COL])
#   print(f"After enforcing numeric {QTY_COL}/{PRICE_COL}: {len(df)} rows")

#   df["SalesAmount"] = df[QTY_COL] * df[PRICE_COL]

#   df = df[df["SalesAmount"] > 0]
#   df = df[df[QTY_COL] > 0]

#   print(f"After removing negative/zero sales & qty: {len(df)} rows")

#   upper = df["SalesAmount"].quantile(0.999)
#   df = df[df["SalesAmount"] <= upper]
#   print(f"After removing top 0.1% extreme sales: {len(df)} rows (upper={upper:.2f})")

#   if CUSTOMER_COL in df.columns:
#     rows_before_cust = len(df)
#     df = df.dropna(subset=[CUSTOMER_COL])
#     print(f"Dropped rows without Customer ID for RFM: {rows_before_cust - len(df)} rows removed")

#   print(f"=== CLEANING: done. Final cleaned rows: {len(df)} (from {initial_rows}) ===")
#   return df

# # =========================================================
# # 1b. EDA
# # =========================================================

# def perform_eda(df: pd.DataFrame):
#   print("\n=== EDA: start ===")

#   missing = df.isna().sum().sort_values(ascending=False)
#   missing.to_csv(EDA_MISSING_PATH, header=["missing_count"])
#   print(f"Saved missing values report to {EDA_MISSING_PATH}")

#   try:
#     describe_all = df.describe(include="all", datetime_is_numeric=True)
#   except TypeError:
#     describe_all = df.describe(include="all")
#   describe_all.to_csv(EDA_DESCRIBE_PATH)
#   print(f"Saved full describe() summary to {EDA_DESCRIBE_PATH}")

#   df_month = df.copy()
#   df_month[DATE_COL] = pd.to_datetime(df_month[DATE_COL])
#   df_month["InvoiceMonth"] = df_month[DATE_COL].dt.to_period("M").dt.to_timestamp()
#   monthly_sales = (
#     df_month.groupby("InvoiceMonth")["SalesAmount"]
#     .sum()
#     .reset_index()
#     .sort_values("InvoiceMonth")
#   )
#   monthly_sales.to_csv(EDA_MONTHLY_SALES_PATH, index=False)
#   print(f"Saved monthly sales trend to {EDA_MONTHLY_SALES_PATH}")

#   top_products = (
#     df.groupby(DESC_COL)["SalesAmount"]
#     .sum()
#     .reset_index()
#     .sort_values("SalesAmount", ascending=False)
#     .head(20)
#   )
#   top_products.to_csv(EDA_TOP_PRODUCTS_PATH, index=False)
#   print(f"Saved top 20 products by sales to {EDA_TOP_PRODUCTS_PATH}")

#   top_countries = (
#     df.groupby(COUNTRY_COL)["SalesAmount"]
#     .sum()
#     .reset_index()
#     .sort_values("SalesAmount", ascending=False)
#     .head(20)
#   )
#   top_countries.to_csv(EDA_TOP_COUNTRIES_PATH, index=False)
#   print(f"Saved top 20 countries by sales to {EDA_TOP_COUNTRIES_PATH}")

#   print("=== EDA: done. Check artifacts/ folder for CSV summaries. ===")

#   return monthly_sales, top_products, top_countries

# # =========================================================
# # 2. AGGREGATION: DAILY/WEEKLY/CATEGORY/COUNTRY
# # =========================================================

# def build_daily_sales(df: pd.DataFrame) -> pd.DataFrame:
#   daily = (
#     df.set_index(DATE_COL)
#       .resample("D")
#       .agg({"SalesAmount": "sum"})
#       .rename(columns={"SalesAmount": "y"})
#   )
#   daily["y"] = daily["y"].fillna(0)
#   daily = daily.reset_index().rename(columns={DATE_COL: "ds"})
#   return daily

# def build_weekly_sales(df: pd.DataFrame) -> pd.DataFrame:
#   weekly = (
#     df.set_index(DATE_COL)
#       .resample("W")
#       .agg({"SalesAmount": "sum"})
#       .rename(columns={"SalesAmount": "y"})
#   )
#   weekly["y"] = weekly["y"].fillna(0)
#   weekly = weekly.reset_index().rename(columns={DATE_COL: "ds"})
#   return weekly

# def build_category_sales(df: pd.DataFrame) -> pd.DataFrame:
#   cat = (
#     df.groupby([DESC_COL])
#       .agg({"SalesAmount": "sum"})
#       .reset_index()
#       .sort_values("SalesAmount", ascending=False)
#   )
#   return cat

# def build_country_sales(df: pd.DataFrame) -> pd.DataFrame:
#   ctry = (
#     df.groupby([COUNTRY_COL])
#       .agg({"SalesAmount": "sum"})
#       .reset_index()
#       .sort_values("SalesAmount", ascending=False)
#   )
#   return ctry

# # =========================================================
# # 3. LSTM FORECAST MODEL
# # =========================================================

# def build_lstm_sequences(y_scaled: np.ndarray, lookback: int):
#   X, y = [], []
#   for i in range(len(y_scaled) - lookback):
#     X.append(y_scaled[i:i + lookback])
#     y.append(y_scaled[i + lookback])
#   X = np.array(X)
#   y = np.array(y)
#   X = X.reshape((X.shape[0], X.shape[1], 1))
#   return X, y

# def train_lstm_forecaster(
#   weekly: pd.DataFrame,
#   last_raw_date: pd.Timestamp,
#   lookback: int = 12,
#   test_points: int = 4
# ):
#   if tf is None:
#     print("⚠ TensorFlow is not available; skipping LSTM training.")
#     return None, None, None

#   df = weekly.copy().sort_values("ds")
#   y_series = df["y"].values.astype(float)

#   if len(y_series) <= lookback + test_points + 5:
#     raise ValueError("Time series too short for LSTM with given lookback and test_points.")

#   scaler = StandardScaler()
#   y_scaled = scaler.fit_transform(y_series.reshape(-1, 1)).flatten()

#   X_all, y_all = build_lstm_sequences(y_scaled, lookback=lookback)
#   num_sequences = X_all.shape[0]

#   if num_sequences <= test_points:
#     raise ValueError("Not enough sequences for the chosen test_points in LSTM.")

#   split_idx = num_sequences - test_points
#   X_train, X_test = X_all[:split_idx], X_all[split_idx:]
#   y_train, y_test = y_all[:split_idx], y_all[split_idx:]

#   print(f"\nLSTM: total sequences={num_sequences}, train={X_train.shape[0]}, test={X_test.shape[0]}")

#   model = tf.keras.Sequential([
#     tf.keras.layers.Input(shape=(lookback, 1)),
#     tf.keras.layers.LSTM(64, return_sequences=True, activation="tanh"),
#     tf.keras.layers.LSTM(32, activation="tanh"),
#     tf.keras.layers.Dense(16, activation="relu"),
#     tf.keras.layers.Dense(1)
#   ])

#   model.compile(
#     optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
#     loss="mse"
#   )

#   callbacks = [
#     tf.keras.callbacks.EarlyStopping(
#       monitor="val_loss",
#       patience=10,
#       restore_best_weights=True
#     )
#   ]

#   history = model.fit(
#     X_train, y_train,
#     epochs=100,
#     batch_size=16,
#     verbose=1,
#     validation_split=0.1,
#     shuffle=False,
#     callbacks=callbacks
#   )

#   y_pred_scaled = model.predict(X_test).flatten()

#   y_test_true = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()
#   y_test_pred = scaler.inverse_transform(y_pred_scaled.reshape(-1, 1)).flatten()

#   rmse = np.sqrt(mean_squared_error(y_test_true, y_test_pred))
#   test_mape = mape(y_test_true, y_test_pred)
#   r2 = r2_score(y_test_true, y_test_pred)

#   if np.isnan(test_mape):
#     accuracy_pct = np.nan
#   else:
#     accuracy_pct = max(0.0, 100.0 - test_mape)

#   print("\n=== LSTM Forecast Performance (weekly, last {} points) ===".format(test_points))
#   print(f"RMSE: {rmse:.3f}")
#   if np.isnan(test_mape):
#     print("MAPE: cannot be computed reliably (all true values are ~0).")
#     print("Accuracy: not defined.")
#   else:
#     print(f"MAPE: {test_mape:.3f}%")
#     print(f"Approx. Forecast Accuracy (100 - MAPE, clipped): {accuracy_pct:.2f}%")
#   print(f"R²:   {r2:.4f}")

#   metrics = {
#     "rmse": float(rmse),
#     "mape": float(test_mape) if not np.isnan(test_mape) else None,
#     "r2": float(r2),
#     "accuracy_pct": float(accuracy_pct) if not np.isnan(accuracy_pct) else None
#   }

#   last_lookback_scaled = y_scaled[-lookback:]
#   window = last_lookback_scaled.reshape(1, lookback, 1)

#   future_scaled = []
#   steps_ahead = 4
#   for _ in range(steps_ahead):
#     next_scaled = model.predict(window, verbose=0)[0, 0]
#     future_scaled.append(next_scaled)
#     window = np.roll(window, -1, axis=1)
#     window[0, -1, 0] = next_scaled

#   future_scaled = np.array(future_scaled)
#   future_pred = scaler.inverse_transform(future_scaled.reshape(-1, 1)).flatten()

#   future_dates = [last_raw_date + pd.Timedelta(weeks=i+1) for i in range(steps_ahead)]

#   next4_lstm_df = pd.DataFrame({
#     "ds": future_dates,
#     "yhat_lstm": future_pred
#   })
#   next4_lstm_df.to_csv(NEXT4W_LSTM_PATH, index=False)
#   print(f"Saved next 4-week LSTM forecast (total sales) to {NEXT4W_LSTM_PATH}")

#   model.save(LSTM_MODEL_PATH)
#   joblib.dump(scaler, LSTM_SCALER_PATH)
#   print(f"Saved LSTM weekly model to {LSTM_MODEL_PATH}")
#   print(f"Saved LSTM scaler to {LSTM_SCALER_PATH}")

#   metrics_df = pd.DataFrame([metrics])
#   metrics_df.to_csv(LSTM_METRICS_PATH, index=False)
#   print(f"Saved LSTM forecast metrics to {LSTM_METRICS_PATH}")

#   return model, metrics, next4_lstm_df

# # =========================================================
# # 4. SEASON PEAKS, SHOCKS, SIMPLE ANOMALIES
# # =========================================================

# def detect_peaks_and_shocks(daily: pd.DataFrame):
#   df = daily.copy().sort_values("ds")
#   df["rolling_mean_7"] = df["y"].rolling(window=7, min_periods=3).mean()
#   df["rolling_std_7"] = df["y"].rolling(window=7, min_periods=3).std()

#   df["z_score"] = (df["y"] - df["rolling_mean_7"]) / df["rolling_std_7"]
#   peaks = df[df["z_score"] > 2.5]

#   df["diff"] = df["y"].diff()
#   shock_threshold = df["diff"].abs().quantile(0.99)
#   shocks = df[df["diff"].abs() > shock_threshold]

#   print(f"\nDetected {len(peaks)} seasonal peaks (z_score > 2.5)")
#   print(f"Detected {len(shocks)} strong shocks (top 1% changes)")

#   peaks.to_csv(ARTIFACTS_DIR / "peaks.csv", index=False)
#   shocks.to_csv(ARTIFACTS_DIR / "shocks.csv", index=False)

#   return peaks, shocks

# def detect_anomalies(daily: pd.DataFrame):
#   df = daily.copy().sort_values("ds")
#   df["rolling_mean_7"] = df["y"].rolling(window=7, min_periods=5).mean()
#   df["rolling_std_7"] = df["y"].rolling(window=7, min_periods=5).std()

#   df["z_score"] = (df["y"] - df["rolling_mean_7"]) / df["rolling_std_7"]
#   anomalies = df[df["z_score"].abs() > 3]

#   anomalies.to_csv(ARTIFACTS_DIR / "anomalies_daily.csv", index=False)
#   print(f"Saved {len(anomalies)} anomalies (|z| > 3) to artifacts/anomalies_daily.csv")

#   return anomalies

# # =========================================================
# # 5. RFM SEGMENTATION
# # =========================================================

# def compute_rfm(df: pd.DataFrame) -> pd.DataFrame:
#   reference_date = df[DATE_COL].max()
#   print("\nRFM reference date:", reference_date)

#   rfm = (
#     df.groupby(CUSTOMER_COL)
#       .agg({
#         DATE_COL: lambda x: (reference_date - x.max()).days,
#         INVOICE_COL: "nunique",
#         "SalesAmount": "sum"
#       })
#       .rename(columns={
#         DATE_COL: "Recency",
#         INVOICE_COL: "Frequency",
#         "SalesAmount": "Monetary"
#       })
#       .reset_index()
#   )

#   rfm = rfm[rfm["Monetary"] > 0]
#   print("RFM customers:", len(rfm))
#   return rfm

# def rfm_rule_based(rfm: pd.DataFrame) -> pd.DataFrame:
#   rfm = rfm.copy()

#   r_quartiles = pd.qcut(rfm["Recency"], 4, labels=[4, 3, 2, 1])
#   f_quartiles = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4])
#   m_quartiles = pd.qcut(rfm["Monetary"], 4, labels=[1, 2, 3, 4])

#   rfm["R_score"] = r_quartiles.astype(int)
#   rfm["F_score"] = f_quartiles.astype(int)
#   rfm["M_score"] = m_quartiles.astype(int)

#   rfm["RFM_score"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]

#   def assign_segment(row):
#     if row["RFM_score"] >= 10:
#       return "Champions"
#     elif row["RFM_score"] >= 8:
#       return "Loyal Customers"
#     elif row["RFM_score"] >= 6:
#       return "Potential Loyalists"
#     elif row["RFM_score"] >= 4:
#       return "At Risk"
#     else:
#       return "Lost Customers"

#   rfm["Segment"] = rfm.apply(assign_segment, axis=1)

#   return rfm

# def rfm_kmeans(rfm: pd.DataFrame, n_clusters: int = 5):
#   rfm_log = rfm[["Recency", "Frequency", "Monetary"]].copy()
#   rfm_log["Recency"] = np.log1p(rfm_log["Recency"])
#   rfm_log["Frequency"] = np.log1p(rfm_log["Frequency"])
#   rfm_log["Monetary"] = np.log1p(rfm_log["Monetary"])

#   scaler = StandardScaler()
#   rfm_scaled = scaler.fit_transform(rfm_log)

#   kmeans = KMeans(n_clusters=n_clusters, random_state=42)
#   rfm["Cluster"] = kmeans.fit_predict(rfm_scaled)

#   rfm["Score"] = (-rfm_log["Recency"]) + rfm_log["Frequency"] + rfm_log["Monetary"]
#   cluster_scores = (
#     rfm.groupby("Cluster")["Score"]
#        .mean()
#        .sort_values(ascending=False)
#        .reset_index()
#   )
#   cluster_scores["Rank"] = cluster_scores["Score"].rank(ascending=False, method="dense").astype(int)

#   cluster_to_segment = {}
#   for _, row in cluster_scores.iterrows():
#     if row["Rank"] == 1:
#       label = "Champions"
#     elif row["Rank"] == 2:
#       label = "Loyal Customers"
#     elif row["Rank"] == 3:
#       label = "Potential Loyalists"
#     elif row["Rank"] == 4:
#       label = "At Risk"
#     else:
#       label = "Lost Customers"
#     cluster_to_segment[row["Cluster"]] = label

#   rfm["Segment"] = rfm["Cluster"].map(cluster_to_segment)

#   SEGMENT_OFFERS = {
#     "Champions": "Offer 15–20% VIP discount and early access.",
#     "Loyal Customers": "Offer 10% loyalty discount + referral bonus.",
#     "Potential Loyalists": "Send personalized recommendations + 5–10% coupon.",
#     "At Risk": "Re-engagement campaign with 10–12% win-back offer.",
#     "Lost Customers": "Strong limited-time reactivation coupon.",
#   }
#   rfm["Offer"] = rfm["Segment"].map(SEGMENT_OFFERS)

#   joblib.dump(
#     {"scaler": scaler, "kmeans": kmeans},
#     MODELS_DIR / "rfm_kmeans.pkl"
#   )
#   print(f"Saved RFM KMeans model to {MODELS_DIR / 'rfm_kmeans.pkl'}")

#   return rfm

# def plot_customer_segmentation_pie(rfm_df, file_path):
#   segment_counts = rfm_df["Segment"].value_counts()

#   plt.figure(figsize=(8, 8))
#   plt.pie(
#     segment_counts,
#     labels=segment_counts.index,
#     autopct="%1.1f%%",
#     startangle=140
#   )
#   plt.title("Customer Segmentation (RFM)")
#   plt.tight_layout()
#   plt.savefig(file_path)
#   plt.close()
#   print(f"Saved pie chart: {file_path}")

# # =========================================================
# # 6. MAIN DRIVER (REUSABLE)
# # =========================================================

# def run_full_pipeline(csv_path=None):
#   """
#   Run the full data pipeline (cleaning, EDA, aggregations, LSTM, RFM, plots)
#   for the CSV file at csv_path. If csv_path is None, use default CSV_PATH.
#   All artifacts are written to the standard ARTIFACTS_DIR files.
#   """
#   TEST_POINTS = 4  # 4-week evaluation horizon

#   # 1. Load raw data
#   df_raw = load_raw_data(csv_path)

#   # 2. Clean data
#   df = basic_cleaning(df_raw)

#   # 3. Save cleaned data
#   df.to_csv(CLEANED_DATA_PATH, index=False)
#   print(f"Saved cleaned data to {CLEANED_DATA_PATH}")

#   # 4. EDA on cleaned data (also get EDA dfs for plots)
#   monthly_sales, top_products, top_countries = perform_eda(df)

#   # Latest raw date for anchoring future weeks
#   last_raw_date = df[DATE_COL].max()
#   print(f"\nLatest date in dataset (raw): {last_raw_date}")

#   # 5. Aggregations
#   daily = build_daily_sales(df)
#   weekly = build_weekly_sales(df)
#   cat_sales = build_category_sales(df)
#   country_sales = build_country_sales(df)

#   daily.to_csv(DAILY_SALES_PATH, index=False)
#   weekly.to_csv(WEEKLY_SALES_PATH, index=False)
#   cat_sales.to_csv(CATEGORY_SALES_PATH, index=False)
#   country_sales.to_csv(COUNTRY_SALES_PATH, index=False)

#   print(f"\nSaved daily sales to    {DAILY_SALES_PATH}")
#   print(f"Saved weekly sales to   {WEEKLY_SALES_PATH}")
#   print(f"Saved category sales to {CATEGORY_SALES_PATH}")
#   print(f"Saved country sales to  {COUNTRY_SALES_PATH}")

#   # ------ PLOTS for artifacts ------

#   plot_time_series(
#     daily,
#     date_col="ds",
#     value_col="y",
#     title="Daily Sales",
#     y_label="SalesAmount",
#     file_path=PLOTS_DIR / "daily_sales.png"
#   )

#   plot_time_series(
#     weekly,
#     date_col="ds",
#     value_col="y",
#     title="Weekly Sales",
#     y_label="SalesAmount",
#     file_path=PLOTS_DIR / "weekly_sales.png"
#   )

#   plot_time_series(
#     monthly_sales,
#     date_col="InvoiceMonth",
#     value_col="SalesAmount",
#     title="Monthly Sales",
#     y_label="SalesAmount",
#     file_path=PLOTS_DIR / "monthly_sales.png"
#   )

#   plot_bar(
#     top_products,
#     x_col=DESC_COL,
#     y_col="SalesAmount",
#     title="Top 20 Products by Sales",
#     x_label="Product Description",
#     y_label="SalesAmount",
#     file_path=PLOTS_DIR / "top_products.png",
#     rotation=75
#   )

#   plot_bar(
#     top_countries,
#     x_col=COUNTRY_COL,
#     y_col="SalesAmount",
#     title="Top 20 Countries by Sales",
#     x_label="Country",
#     y_label="SalesAmount",
#     file_path=PLOTS_DIR / "top_countries.png",
#     rotation=45
#   )

#   # 6. LSTM model on WEEKLY data
#   lstm_metrics = None
#   next4_lstm_df = None
#   if tf is not None:
#     try:
#       lstm_model, lstm_metrics, next4_lstm_df = train_lstm_forecaster(
#         weekly,
#         last_raw_date=last_raw_date,
#         lookback=12,
#         test_points=TEST_POINTS
#       )
#     except Exception as e:
#       print("⚠ LSTM training failed due to:", e)
#   else:
#     print("⚠ Skipping LSTM: TensorFlow not available or import failed.")

#   if lstm_metrics and lstm_metrics.get("accuracy_pct") is not None:
#     print(f"➡ Final Weekly Forecast Accuracy (LSTM, 100 - MAPE): {lstm_metrics['accuracy_pct']:.2f}%")
#     print(f"➡ Next 4-week LSTM forecast (total) saved to: {NEXT4W_LSTM_PATH}")

#   if next4_lstm_df is not None:
#     plot_lstm_forecast(
#       weekly_df=weekly,
#       forecast_df=next4_lstm_df,
#       file_path=PLOTS_DIR / "lstm_forecast_next4weeks.png"
#     )

#   # 6b. Demographic breakdown of forecast
#   if next4_lstm_df is not None:
#     country_share = (
#       df.groupby(COUNTRY_COL)["SalesAmount"]
#         .sum()
#     )
#     country_share = country_share / country_share.sum()
#     country_share = country_share.sort_values(ascending=False)

#     category_share = (
#       df.groupby(DESC_COL)["SalesAmount"]
#         .sum()
#     )
#     category_share = category_share / category_share.sum()
#     category_share = category_share.sort_values(ascending=False)

#     TOP_N_COUNTRIES = 5
#     TOP_N_CATEGORIES = 5

#     top_country_share = country_share.head(TOP_N_COUNTRIES)
#     top_category_share = category_share.head(TOP_N_CATEGORIES)

#     rows_country = []
#     for _, row in next4_lstm_df.iterrows():
#       ds = row["ds"]
#       total_pred = row["yhat_lstm"]
#       for country, share in top_country_share.items():
#         rows_country.append({
#           "ds": ds,
#           "Country": country,
#           "share": float(share),
#           "yhat_lstm_country": float(total_pred * share)
#         })
#     next4_country_df = pd.DataFrame(rows_country)
#     next4_country_df.to_csv(NEXT4W_LSTM_BY_COUNTRY_PATH, index=False)
#     print(f"Saved next 4-week LSTM forecast by COUNTRY to {NEXT4W_LSTM_BY_COUNTRY_PATH}")

#     rows_category = []
#     for _, row in next4_lstm_df.iterrows():
#       ds = row["ds"]
#       total_pred = row["yhat_lstm"]
#       for desc, share in top_category_share.items():
#         rows_category.append({
#           "ds": ds,
#           "Description": desc,
#           "share": float(share),
#           "yhat_lstm_category": float(total_pred * share)
#         })
#     next4_category_df = pd.DataFrame(rows_category)
#     next4_category_df.to_csv(NEXT4W_LSTM_BY_CATEGORY_PATH, index=False)
#     print(f"Saved next 4-week LSTM forecast by CATEGORY to {NEXT4W_LSTM_BY_CATEGORY_PATH}")

#   # 7. Peaks, shocks, anomalies
#   peaks, shocks = detect_peaks_and_shocks(daily)
#   anomalies = detect_anomalies(daily)

#   # 8. RFM + segmentation
#   rfm = compute_rfm(df)
#   rfm_rule = rfm_rule_based(rfm)
#   rfm_rule.to_csv(ARTIFACTS_DIR / "rfm_segments_rule_based.csv", index=False)
#   print(f"Saved rule-based RFM segments to {ARTIFACTS_DIR / 'rfm_segments_rule_based.csv'}")

#   plot_customer_segmentation_pie(
#     rfm_rule,
#     PLOTS_DIR / "customer_segments_pie.png"
#   )

#   rfm_km = rfm_kmeans(rfm, n_clusters=5)
#   rfm_km.to_csv(ARTIFACTS_DIR / "rfm_segments_kmeans.csv", index=False)
#   print(f"Saved KMeans RFM segments to {ARTIFACTS_DIR / 'rfm_segments_kmeans.csv'}")

#   print("\n✅ ALL TASKS COMPLETED (CLEANING + EDA + LSTM 4-WEEK FORECAST + DEMOGRAPHICS + CRM + PLOTS):")
#   print("- Data cleaned and saved")
#   print("- EDA CSVs (missing, describe, monthly trend, top products, top countries) saved")
#   print(f"- Plots saved in: {PLOTS_DIR}")
#   if lstm_metrics and lstm_metrics.get("accuracy_pct") is not None:
#     print("- LSTM weekly forecast + metrics (4-week test)")
#     print(f"  ▸ LSTM Accuracy (100 - MAPE): {lstm_metrics['accuracy_pct']:.2f}%")
#     print(f"- Next 4-week LSTM TOTAL forecast CSV: {NEXT4W_LSTM_PATH}")
#     print(f"- Next 4-week LSTM forecast BY COUNTRY: {NEXT4W_LSTM_BY_COUNTRY_PATH}")
#     print(f"- Next 4-week LSTM forecast BY CATEGORY: {NEXT4W_LSTM_BY_CATEGORY_PATH}")
#     print(f"- LSTM forecast plot: {PLOTS_DIR / 'lstm_forecast_next4weeks.png'}")
#   else:
#     print("- LSTM metrics: not available (see earlier warnings).")
#   print("- Peaks + shocks + anomalies saved (daily)")
#   print("- RFM (rule-based + KMeans) saved")
#   print("- Aggregates for daily/weekly/country/category saved")
#   print(f"- LSTM metrics stored at:   {LSTM_METRICS_PATH}")

#   summary = {
#     "cleaned_data_path": str(CLEANED_DATA_PATH),
#     "daily_sales_path": str(DAILY_SALES_PATH),
#     "weekly_sales_path": str(WEEKLY_SALES_PATH),
#     "category_sales_path": str(CATEGORY_SALES_PATH),
#     "country_sales_path": str(COUNTRY_SALES_PATH),
#     "eda": {
#       "missing_path": str(EDA_MISSING_PATH),
#       "describe_path": str(EDA_DESCRIBE_PATH),
#       "monthly_sales_path": str(EDA_MONTHLY_SALES_PATH),
#       "top_products_path": str(EDA_TOP_PRODUCTS_PATH),
#       "top_countries_path": str(EDA_TOP_COUNTRIES_PATH),
#     },
#     "lstm": {
#       "metrics": lstm_metrics,
#       "metrics_path": str(LSTM_METRICS_PATH),
#       "total_forecast_path": str(NEXT4W_LSTM_PATH),
#       "by_country_path": str(NEXT4W_LSTM_BY_COUNTRY_PATH),
#       "by_category_path": str(NEXT4W_LSTM_BY_CATEGORY_PATH) if next4_lstm_df is not None else None,
#     } if lstm_metrics is not None else None,
#     "rfm": {
#       "rule_based_path": str(ARTIFACTS_DIR / "rfm_segments_rule_based.csv"),
#       "kmeans_path": str(ARTIFACTS_DIR / "rfm_segments_kmeans.csv"),
#     },
#     "plots": {
#       "daily_sales": str(PLOTS_DIR / "daily_sales.png"),
#       "weekly_sales": str(PLOTS_DIR / "weekly_sales.png"),
#       "monthly_sales": str(PLOTS_DIR / "monthly_sales.png"),
#       "top_products": str(PLOTS_DIR / "top_products.png"),
#       "top_countries": str(PLOTS_DIR / "top_countries.png"),
#       "lstm_forecast_next4weeks": str(PLOTS_DIR / "lstm_forecast_next4weeks.png") if next4_lstm_df is not None else None,
#       "customer_segments_pie": str(PLOTS_DIR / "customer_segments_pie.png"),
#     },
#     "peaks_path": str(ARTIFACTS_DIR / "peaks.csv"),
#     "shocks_path": str(ARTIFACTS_DIR / "shocks.csv"),
#     "anomalies_path": str(ARTIFACTS_DIR / "anomalies_daily.csv"),
#   }

#   return summary

# def main():
#   """
#   Backwards-compatible: run pipeline using default CSV_PATH.
#   """
#   return run_full_pipeline(csv_path=None)

# # =========================================================
# # FLASK APP FOR REACT INTEGRATION
# # =========================================================

# app = Flask(__name__)
# CORS(app)

# @app.route("/api/run-pipeline", methods=["POST", "GET"])
# def run_pipeline_endpoint():
#   """
#   Runs the full data pipeline on the DEFAULT CSV (CSV_PATH).
#   """
#   try:
#     summary = run_full_pipeline(csv_path=None)
#     return jsonify({
#       "status": "success",
#       "summary": summary
#     }), 200
#   except Exception as e:
#     return jsonify({
#       "status": "error",
#       "message": str(e)
#     }), 500

# # ========= NEW: UPLOAD CSV AND RE-RUN PIPELINE =========

# @app.route("/api/upload-csv", methods=["POST"])
# def upload_csv_endpoint():
#   """
#   Accept a CSV file upload, save it under artifacts/uploads,
#   run the full pipeline on that CSV, and regenerate all artifacts.
#   Frontend then just calls /api/forecast-summary and /api/segments-summary
#   to see the updated values.
#   """
#   try:
#     if "file" not in request.files:
#       return jsonify({
#         "status": "error",
#         "message": "No file part in request."
#       }), 400

#     file = request.files["file"]
#     if file.filename == "":
#       return jsonify({
#         "status": "error",
#         "message": "No selected file."
#       }), 400

#     upload_dir = ARTIFACTS_DIR / "uploads"
#     upload_dir.mkdir(exist_ok=True, parents=True)
#     upload_path = upload_dir / "latest_upload.csv"

#     file.save(upload_path)
#     print(f"✅ Uploaded CSV saved to {upload_path}")

#     summary = run_full_pipeline(csv_path=upload_path)

#     return jsonify({
#       "status": "success",
#       "message": "CSV uploaded and pipeline re-run successfully.",
#       "summary": summary
#     }), 200

#   except Exception as e:
#     print("⚠ Error in /api/upload-csv:", e)
#     return jsonify({
#       "status": "error",
#       "message": str(e)
#     }), 500

# @app.route("/api/forecast-summary", methods=["GET"])
# def forecast_summary():
#   """
#   Return forecast metrics + weekly sales data for charts.
#   """
#   try:
#     # Ensure pipeline artifacts exist; normally already done at startup or after upload
#     if (
#       not NEXT4W_LSTM_PATH.exists()
#       or not WEEKLY_SALES_PATH.exists()
#       or not LSTM_METRICS_PATH.exists()
#     ):
#       main()

#     # Load metrics
#     if LSTM_METRICS_PATH.exists():
#       metrics_df = pd.read_csv(LSTM_METRICS_PATH)
#       metrics = metrics_df.iloc[0].to_dict()
#     else:
#       metrics = {}

#     # Load forecast CSV
#     forecast_df = None
#     total_forecast = None
#     if NEXT4W_LSTM_PATH.exists():
#       forecast_df = pd.read_csv(NEXT4W_LSTM_PATH)
#       if "yhat_lstm" in forecast_df.columns:
#         total_forecast = float(forecast_df["yhat_lstm"].sum())

#     weeklySalesData = []

#     # Load weekly actuals (up to last 12 points)
#     if WEEKLY_SALES_PATH.exists():
#       weekly_df = pd.read_csv(WEEKLY_SALES_PATH)
#       if "ds" in weekly_df.columns and "y" in weekly_df.columns:
#         weekly_df = weekly_df.sort_values("ds")
#         n = len(weekly_df)
#         if n > 0:
#           last_n = min(12, n)
#           recent_df = weekly_df.tail(last_n).reset_index(drop=True)

#           forecast_values = None
#           if forecast_df is not None and "yhat_lstm" in forecast_df.columns:
#             forecast_values = forecast_df["yhat_lstm"].values
#           forecast_len = len(forecast_values) if forecast_values is not None else 0

#           for idx, row in recent_df.iterrows():
#             forecast_val = None
#             if forecast_values is not None and forecast_len > 0:
#               if idx >= last_n - forecast_len:
#                 f_index = idx - (last_n - forecast_len)
#                 if 0 <= f_index < forecast_len:
#                   forecast_val = float(forecast_values[f_index])

#             weeklySalesData.append({
#               "week": f"Week {idx+1}",
#               "actual": float(row["y"]),
#               "forecast": forecast_val,
#             })

#     # ===== CALCULATE KPI METRICS =====
#     kpi_metrics = {
#       "prev_4_weeks_total": None,
#       "last_4_weeks_total": None,
#       "next_4_weeks_forecast": total_forecast,
#       "sales_change_pct": None,
#       "forecast_change_pct": None,
#       "accuracy_pct": metrics.get("accuracy_pct"),
#     }

#     if WEEKLY_SALES_PATH.exists():
#       try:
#         weekly_df_full = pd.read_csv(WEEKLY_SALES_PATH)
#         if len(weekly_df_full) >= 8:
#           weekly_df_full = weekly_df_full.sort_values("ds")
#           prev_4_weeks = weekly_df_full.iloc[-8:-4]["y"].sum()
#           last_4_weeks = weekly_df_full.iloc[-4:]["y"].sum()

#           kpi_metrics["prev_4_weeks_total"] = float(prev_4_weeks)
#           kpi_metrics["last_4_weeks_total"] = float(last_4_weeks)

#           if prev_4_weeks > 0:
#             sales_change = ((last_4_weeks - prev_4_weeks) / prev_4_weeks) * 100
#             kpi_metrics["sales_change_pct"] = float(sales_change)

#           if last_4_weeks > 0 and total_forecast is not None:
#             forecast_change = ((total_forecast - last_4_weeks) / last_4_weeks) * 100
#             kpi_metrics["forecast_change_pct"] = float(forecast_change)
#       except Exception as e:
#         print(f"Error calculating KPI metrics: {e}")

#     metrics.update(kpi_metrics)

#     # ===== log to blockchain + firebase with rate limiting =====
#     blockchain_meta = None
#     rate_limit_info = {
#       "active": False,
#       "cooldownSeconds": 0
#     }
#     try:
#       if total_forecast is not None:
#         allowed, cooldown = check_rate_limit()
#         if allowed:
#           blockchain_meta = log_forecast_onchain_and_firebase(
#             total_forecast,
#             model_version="lstm_weekly_v1"
#           )
#         else:
#           rate_limit_info["active"] = True
#           rate_limit_info["cooldownSeconds"] = int(cooldown)
#           print(f"⏳ Skipping on-chain/Firebase log due to rate limit. Cooldown ~{cooldown:.1f}s left.")
#     except Exception as e:
#       print(f"⚠ Error logging forecast to blockchain/Firebase: {e}")
#       blockchain_meta = None

#     resp = {
#       "status": "success",
#       "total_forecast": total_forecast,
#       "total_forecast_formatted": (
#         f"₹{int(round(total_forecast)):,}" if total_forecast is not None else None
#       ),
#       "metrics": metrics,
#       "weeklySalesData": weeklySalesData,
#       "blockchain": blockchain_meta,
#       "rateLimit": rate_limit_info,
#     }
#     return jsonify(resp), 200
#   except Exception as e:
#     return jsonify({
#       "status": "error",
#       "message": str(e),
#     }), 500

# @app.route("/api/segments-summary", methods=["GET"])
# def segments_summary():
#   """
#   Return segment distribution + sample customers derived from RFM.
#   """
#   try:
#     rfm_path = ARTIFACTS_DIR / "rfm_segments_rule_based.csv"
#     if not rfm_path.exists():
#       main()

#     if not rfm_path.exists():
#       return jsonify({
#         "status": "error",
#         "message": "RFM segments file not found even after pipeline run.",
#       }), 500

#     rfm_df = pd.read_csv(rfm_path)

#     if "Segment" not in rfm_df.columns:
#       return jsonify({
#         "status": "error",
#         "message": "Segment column missing in RFM file.",
#       }), 500

#     seg_counts = rfm_df["Segment"].value_counts()
#     segments = [
#       {"name": str(seg), "value": int(cnt)}
#       for seg, cnt in seg_counts.items()
#     ]

#     customers = []
#     for _, row in rfm_df.iterrows():
#       cust_id = row.get(CUSTOMER_COL, None)
#       customers.append({
#         "id": str(cust_id) if cust_id is not None else "",
#         "name": f"Customer {cust_id}" if cust_id is not None else "Customer",
#         "segment": row.get("Segment", ""),
#         "recency": int(row.get("Recency", 0)),
#         "frequency": int(row.get("Frequency", 0)),
#         "monetary": float(row.get("Monetary", 0.0)),
#       })

#     return jsonify({
#       "status": "success",
#       "segments": segments,
#       "customers": customers,
#     }), 200
#   except Exception as e:
#     return jsonify({
#       "status": "error",
#       "message": str(e),
#     }), 500

# # =========================================================
# # NEW: EXPLICIT ENDPOINT TO LOG LATEST FORECAST ON-CHAIN
# # =========================================================

# @app.route("/api/log-forecast", methods=["POST"])
# def log_forecast_endpoint():
#   """
#   Explicit endpoint to force logging the latest 4-week forecast
#   to blockchain (Ganache) + Firebase.
#   """
#   try:
#     body = request.get_json(silent=True) or {}
#     model_version = body.get("modelVersion", "lstm_weekly_v1")
#     secret = body.get("secret")

#     if secret is not None and secret != API_SECRET_KEY:
#       return jsonify({
#         "status": "error",
#         "message": "Invalid API secret."
#       }), 403

#     allowed, cooldown = check_rate_limit()
#     if not allowed:
#       return jsonify({
#         "status": "error",
#         "message": f"Rate limit exceeded. Try again in {int(cooldown)} seconds.",
#         "rateLimit": {
#           "active": True,
#           "cooldownSeconds": int(cooldown)
#         }
#       }), 429

#     if not NEXT4W_LSTM_PATH.exists() or not LSTM_METRICS_PATH.exists():
#       main()

#     total_forecast = None
#     if NEXT4W_LSTM_PATH.exists():
#       forecast_df = pd.read_csv(NEXT4W_LSTM_PATH)
#       if "yhat_lstm" in forecast_df.columns:
#         total_forecast = float(forecast_df["yhat_lstm"].sum())

#     if total_forecast is None:
#       return jsonify({
#         "status": "error",
#         "message": "No forecast available to log."
#       }), 400

#     meta = log_forecast_onchain_and_firebase(total_forecast, model_version=model_version)

#     return jsonify({
#       "status": "success",
#       "total_forecast": total_forecast,
#       "total_forecast_formatted": f"₹{int(round(total_forecast)):,}",
#       "blockchain": meta,
#       "rateLimit": {
#         "active": False,
#         "cooldownSeconds": LOG_RATE_LIMIT_WINDOW_SECONDS
#       }
#     }), 200

#   except Exception as e:
#     return jsonify({
#       "status": "error",
#       "message": str(e),
#     }), 500

# # =========================================================
# # APP ENTRYPOINT
# # =========================================================

# if __name__ == "__main__":
#   init_firebase()
#   init_blockchain()

#   print("🚀 Running initial data pipeline & model training...")
#   try:
#     main()
#     print("✅ Pipeline ready. Starting Flask server...")
#   except Exception as e:
#     print("⚠ Initial pipeline failed:", e)

#   app.run(host="0.0.0.0", port=5000, debug=True)

