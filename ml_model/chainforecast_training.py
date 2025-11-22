# import os

# # ---- Make TensorFlow as deterministic as possible (set BEFORE importing TF) ----
# os.environ["PYTHONHASHSEED"] = "42"
# os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # turn off oneDNN ops to avoid tiny non-deterministic diffs

# from pathlib import Path
# import random
# import numpy as np
# import pandas as pd
# import joblib

# from sklearn.metrics import mean_squared_error, r2_score
# from sklearn.preprocessing import StandardScaler
# from sklearn.cluster import KMeans

# import matplotlib.pyplot as plt  # <-- for plots

# # =======================
# # TensorFlow / LSTM
# # =======================
# try:
#     import tensorflow as tf # pyright: ignore[reportMissingImports]
#     TF_IMPORT_ERROR = None

#     # set seeds for reproducibility
#     random.seed(42)
#     np.random.seed(42)
#     tf.random.set_seed(42)
# except Exception as e:
#     tf = None
#     TF_IMPORT_ERROR = e
#     print("⚠️ TensorFlow import failed. LSTM model will be skipped.")
#     print("   Reason:", e)

# # =========================================================
# # CONFIG – EDIT ONLY PATH IF NEEDED
# # =========================================================

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
#     plt.plot(forecast_df["ds"], forecast_df["yhat_lstm"], marker="o", linestyle="--",
#              label="Next 4 Weeks Forecast")

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

#     Future weeks are anchored to the *latest date in the raw dataset* (last_raw_date),
#     so forecasts correspond to:
#         last_raw_date + 1 week
#         last_raw_date + 2 weeks
#         last_raw_date + 3 weeks
#         last_raw_date + 4 weeks
#     """
#     if tf is None:
#         print("⚠️ TensorFlow is not available; skipping LSTM training.")
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

#     r_quartiles = pd.qcut(rfm["Recency"], 4, labels=[4,3,2,1])
#     f_quartiles = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1,2,3,4])
#     m_quartiles = pd.qcut(rfm["Monetary"], 4, labels=[1,2,3,4])

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
#             print("⚠️ LSTM training failed due to:", e)
#     else:
#         print("⚠️ Skipping LSTM: TensorFlow not available or import failed.")

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
#                     "share": share,
#                     "yhat_lstm_country": total_pred * share
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
#                     "share": share,
#                     "yhat_lstm_category": total_pred * share
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


# if __name__ == "__main__":
#     main()







import os

# ---- Make TensorFlow as deterministic as possible (set BEFORE importing TF) ----
os.environ["PYTHONHASHSEED"] = "42"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # turn off oneDNN ops to avoid tiny non-deterministic diffs

from pathlib import Path
import random
import numpy as np
import pandas as pd
import joblib

from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt  # <-- for plots

# =======================
# TensorFlow / LSTM
# =======================
try:
    import tensorflow as tf  # pyright: ignore[reportMissingImports]
    TF_IMPORT_ERROR = None

    # set seeds for reproducibility
    random.seed(42)
    np.random.seed(42)
    tf.random.set_seed(42)
except Exception as e:
    tf = None
    TF_IMPORT_ERROR = e
    print("⚠️ TensorFlow import failed. LSTM model will be skipped.")
    print("   Reason:", e)

# =========================================================
# CONFIG – EDIT ONLY PATH IF NEEDED
# =========================================================

CSV_PATH = Path(r"Online_Retail_new.csv")  # your dataset

DATE_COL = "InvoiceDate"
QTY_COL = "Quantity"
PRICE_COL = "Price"
CUSTOMER_COL = "Customer ID"
INVOICE_COL = "Invoice"
COUNTRY_COL = "Country"
DESC_COL = "Description"

MODELS_DIR = Path("models")
ARTIFACTS_DIR = Path("artifacts")
MODELS_DIR.mkdir(exist_ok=True, parents=True)
ARTIFACTS_DIR.mkdir(exist_ok=True, parents=True)

DAILY_SALES_PATH = ARTIFACTS_DIR / "daily_sales.csv"
WEEKLY_SALES_PATH = ARTIFACTS_DIR / "weekly_sales.csv"
CATEGORY_SALES_PATH = ARTIFACTS_DIR / "category_sales.csv"
COUNTRY_SALES_PATH = ARTIFACTS_DIR / "country_sales.csv"

CLEANED_DATA_PATH = ARTIFACTS_DIR / "cleaned_online_retail.csv"

LSTM_MODEL_PATH = MODELS_DIR / "lstm_model_weekly.h5"
LSTM_SCALER_PATH = MODELS_DIR / "lstm_scaler_weekly.pkl"
LSTM_METRICS_PATH = ARTIFACTS_DIR / "lstm_forecast_metrics_weekly.csv"

# EDA outputs
EDA_MISSING_PATH = ARTIFACTS_DIR / "eda_missing_values.csv"
EDA_DESCRIBE_PATH = ARTIFACTS_DIR / "eda_describe_all.csv"
EDA_MONTHLY_SALES_PATH = ARTIFACTS_DIR / "eda_monthly_sales.csv"
EDA_TOP_PRODUCTS_PATH = ARTIFACTS_DIR / "eda_top_products.csv"
EDA_TOP_COUNTRIES_PATH = ARTIFACTS_DIR / "eda_top_countries.csv"

# 4-week LSTM forecast outputs
NEXT4W_LSTM_PATH = ARTIFACTS_DIR / "next4weeks_lstm.csv"
NEXT4W_LSTM_BY_COUNTRY_PATH = ARTIFACTS_DIR / "next4weeks_lstm_by_country.csv"
NEXT4W_LSTM_BY_CATEGORY_PATH = ARTIFACTS_DIR / "next4weeks_lstm_by_category.csv"

# Plots output directory
PLOTS_DIR = ARTIFACTS_DIR / "plots"
PLOTS_DIR.mkdir(exist_ok=True, parents=True)


# =========================================================
# UTILS
# =========================================================

def mape(y_true, y_pred, eps=1e-3):
    """
    MAPE ignoring very small true values, to avoid exploding percentages.
    """
    y_true = np.array(y_true, dtype=float)
    y_pred = np.array(y_pred, dtype=float)

    mask = np.abs(y_true) > eps
    if not np.any(mask):
        return np.nan

    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100


# ---------------- PLOTTING HELPERS ----------------

def plot_time_series(df, date_col, value_col, title, y_label, file_path):
    """
    Generic time series line plot.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(df[date_col], df[value_col])
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel(y_label)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()
    print(f"Saved plot: {file_path}")


def plot_bar(df, x_col, y_col, title, x_label, y_label, file_path, rotation=45):
    """
    Generic bar chart.
    """
    plt.figure(figsize=(10, 5))
    plt.bar(df[x_col].astype(str), df[y_col])
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=rotation, ha="right")
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()
    print(f"Saved plot: {file_path}")


def plot_lstm_forecast(weekly_df, forecast_df, file_path, last_weeks_history=20):
    """
    Plot the last few weeks of historical sales and next 4-week LSTM forecast.
    weekly_df: DataFrame with columns ['ds', 'y']
    forecast_df: DataFrame with columns ['ds', 'yhat_lstm']
    """
    weekly_df = weekly_df.sort_values("ds").copy()
    hist_tail = weekly_df.tail(last_weeks_history)

    plt.figure(figsize=(10, 5))
    # history
    plt.plot(hist_tail["ds"], hist_tail["y"], label="Historical Weekly Sales")

    # forecast
    plt.plot(
        forecast_df["ds"],
        forecast_df["yhat_lstm"],
        marker="o",
        linestyle="--",
        label="Next 4 Weeks Forecast",
    )

    plt.title("Weekly Sales with Next 4-Week LSTM Forecast")
    plt.xlabel("Date")
    plt.ylabel("SalesAmount")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()
    print(f"Saved LSTM forecast plot: {file_path}")


# =========================================================
# 1. LOAD + CLEAN DATA
# =========================================================

def load_raw_data():
    print(f"Loading data from {CSV_PATH}")
    df = pd.read_csv(CSV_PATH, encoding="ISO-8859-1")
    print("Raw shape:", df.shape)
    print("Columns:", df.columns.tolist())
    return df


def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    print("\n=== CLEANING: start ===")
    # ensure date parse
    df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")

    initial_rows = len(df)

    # drop cancelled invoices (Invoice starting with 'C')
    if INVOICE_COL in df.columns:
        df[INVOICE_COL] = df[INVOICE_COL].astype(str)
        df = df[~df[INVOICE_COL].str.startswith("C")]
        print(f"Removed cancelled invoices. Rows now: {len(df)}")

    # drop rows with missing critical info
    df = df.dropna(subset=[DATE_COL, QTY_COL, PRICE_COL])
    print(
        f"After dropping rows with NA in [{DATE_COL}, {QTY_COL}, {PRICE_COL}]: {len(df)} rows"
    )

    # convert quantity and price to numeric (in case of bad strings)
    df[QTY_COL] = pd.to_numeric(df[QTY_COL], errors="coerce")
    df[PRICE_COL] = pd.to_numeric(df[PRICE_COL], errors="coerce")

    df = df.dropna(subset=[QTY_COL, PRICE_COL])
    print(f"After enforcing numeric {QTY_COL}/{PRICE_COL}: {len(df)} rows")

    # sales amount
    df["SalesAmount"] = df[QTY_COL] * df[PRICE_COL]

    # remove negative/zero sales and quantities
    df = df[df["SalesAmount"] > 0]
    df = df[df[QTY_COL] > 0]

    print(f"After removing negative/zero sales & qty: {len(df)} rows")

    # remove extreme outliers
    upper = df["SalesAmount"].quantile(0.999)
    df = df[df["SalesAmount"] <= upper]
    print(
        f"After removing top 0.1% extreme sales: {len(df)} rows (upper={upper:.2f})"
    )

    # optionally drop rows without customer ID for RFM (not required for forecasting)
    if CUSTOMER_COL in df.columns:
        rows_before_cust = len(df)
        df = df.dropna(subset=[CUSTOMER_COL])
        print(
            f"Dropped rows without Customer ID for RFM: {rows_before_cust - len(df)} rows removed"
        )

    print(
        f"=== CLEANING: done. Final cleaned rows: {len(df)} (from {initial_rows}) ==="
    )
    return df


# =========================================================
# 1b. EDA
# =========================================================

def perform_eda(df: pd.DataFrame):
    """
    Perform basic EDA and save outputs as CSVs into artifacts/.
    Also return some EDA DataFrames for plotting.
    """
    print("\n=== EDA: start ===")

    # Missing values
    missing = df.isna().sum().sort_values(ascending=False)
    missing.to_csv(EDA_MISSING_PATH, header=["missing_count"])
    print(f"Saved missing values report to {EDA_MISSING_PATH}")

    # Describe (numeric + object); handle pandas versions without datetime_is_numeric
    try:
        describe_all = df.describe(include="all", datetime_is_numeric=True)
    except TypeError:
        describe_all = df.describe(include="all")
    describe_all.to_csv(EDA_DESCRIBE_PATH)
    print(f"Saved full describe() summary to {EDA_DESCRIBE_PATH}")

    # Monthly sales trend
    df_month = df.copy()
    df_month[DATE_COL] = pd.to_datetime(df_month[DATE_COL])
    df_month["InvoiceMonth"] = (
        df_month[DATE_COL].dt.to_period("M").dt.to_timestamp()
    )
    monthly_sales = (
        df_month.groupby("InvoiceMonth")["SalesAmount"]
        .sum()
        .reset_index()
        .sort_values("InvoiceMonth")
    )
    monthly_sales.to_csv(EDA_MONTHLY_SALES_PATH, index=False)
    print(f"Saved monthly sales trend to {EDA_MONTHLY_SALES_PATH}")

    # Top 20 products by total sales
    top_products = (
        df.groupby(DESC_COL)["SalesAmount"]
        .sum()
        .reset_index()
        .sort_values("SalesAmount", ascending=False)
        .head(20)
    )
    top_products.to_csv(EDA_TOP_PRODUCTS_PATH, index=False)
    print(f"Saved top 20 products by sales to {EDA_TOP_PRODUCTS_PATH}")

    # Top 20 countries by total sales
    top_countries = (
        df.groupby(COUNTRY_COL)["SalesAmount"]
        .sum()
        .reset_index()
        .sort_values("SalesAmount", ascending=False)
        .head(20)
    )
    top_countries.to_csv(EDA_TOP_COUNTRIES_PATH, index=False)
    print(f"Saved top 20 countries by sales to {EDA_TOP_COUNTRIES_PATH}")

    print("=== EDA: done. Check artifacts/ folder for CSV summaries. ===")

    # return for plotting
    return monthly_sales, top_products, top_countries


# =========================================================
# 2. AGGREGATION: DAILY/WEEKLY/CATEGORY/COUNTRY
# =========================================================

def build_daily_sales(df: pd.DataFrame) -> pd.DataFrame:
    daily = (
        df.set_index(DATE_COL)
        .resample("D")
        .agg({"SalesAmount": "sum"})
        .rename(columns={"SalesAmount": "y"})
    )
    daily["y"] = daily["y"].fillna(0)
    daily = daily.reset_index().rename(columns={DATE_COL: "ds"})
    return daily


def build_weekly_sales(df: pd.DataFrame) -> pd.DataFrame:
    weekly = (
        df.set_index(DATE_COL)
        .resample("W")
        .agg({"SalesAmount": "sum"})
        .rename(columns={"SalesAmount": "y"})
    )
    weekly["y"] = weekly["y"].fillna(0)
    weekly = weekly.reset_index().rename(columns={DATE_COL: "ds"})
    return weekly


def build_category_sales(df: pd.DataFrame) -> pd.DataFrame:
    cat = (
        df.groupby([DESC_COL])
        .agg({"SalesAmount": "sum"})
        .reset_index()
        .sort_values("SalesAmount", ascending=False)
    )
    return cat


def build_country_sales(df: pd.DataFrame) -> pd.DataFrame:
    ctry = (
        df.groupby([COUNTRY_COL])
        .agg({"SalesAmount": "sum"})
        .reset_index()
        .sort_values("SalesAmount", ascending=False)
    )
    return ctry


# =========================================================
# 3. LSTM FORECAST MODEL (WEEKLY, 4-WEEK TEST + 4-WEEK FUTURE)
# =========================================================

def build_lstm_sequences(y_scaled: np.ndarray, lookback: int):
    """
    Convert 1D scaled series to supervised sequences for LSTM.
    y_scaled: shape (T,)
    Returns: X (num_samples, lookback, 1), y (num_samples,)
    """
    X, y = [], []
    for i in range(len(y_scaled) - lookback):
        X.append(y_scaled[i : i + lookback])
        y.append(y_scaled[i + lookback])
    X = np.array(X)
    y = np.array(y)
    # reshape X to (samples, timesteps, features)
    X = X.reshape((X.shape[0], X.shape[1], 1))
    return X, y


def train_lstm_forecaster(
    weekly: pd.DataFrame,
    last_raw_date: pd.Timestamp,
    lookback: int = 12,
    test_points: int = 4,
):
    """
    Train an LSTM forecaster on weekly aggregated 'y' series.
    - lookback: number of past weeks to use as input window.
    - test_points: number of final target points used as test (here 4 weeks).
    Also creates a 4-week future forecast and saves it.

    Future weeks are anchored to the *latest date in the raw dataset* (last_raw_date),
    so forecasts correspond to:
        last_raw_date + 1 week
        last_raw_date + 2 weeks
        last_raw_date + 3 weeks
        last_raw_date + 4 weeks
    """
    if tf is None:
        print("⚠️ TensorFlow is not available; skipping LSTM training.")
        return None, None, None

    df = weekly.copy().sort_values("ds")
    y_series = df["y"].values.astype(float)

    if len(y_series) <= lookback + test_points + 5:
        raise ValueError(
            "Time series too short for LSTM with given lookback and test_points."
        )

    # Scale target series
    scaler = StandardScaler()
    y_scaled = scaler.fit_transform(y_series.reshape(-1, 1)).flatten()

    # Build sequences
    X_all, y_all = build_lstm_sequences(y_scaled, lookback=lookback)
    num_sequences = X_all.shape[0]

    if num_sequences <= test_points:
        raise ValueError(
            "Not enough sequences for the chosen test_points in LSTM."
        )

    # Split train/test on sequences: last test_points as test (time-ordered)
    split_idx = num_sequences - test_points
    X_train, X_test = X_all[:split_idx], X_all[split_idx:]
    y_train, y_test = y_all[:split_idx], y_all[split_idx:]

    print(
        f"\nLSTM: total sequences={num_sequences}, train={X_train.shape[0]}, test={X_test.shape[0]}"
    )

    # Build a slightly deeper LSTM model for better learning
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(lookback, 1)),
            tf.keras.layers.LSTM(64, return_sequences=True, activation="tanh"),
            tf.keras.layers.LSTM(32, activation="tanh"),
            tf.keras.layers.Dense(16, activation="relu"),
            tf.keras.layers.Dense(1),
        ]
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3), loss="mse"
    )

    # Early stopping to avoid overfitting (still deterministic with fixed seeds)
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss", patience=10, restore_best_weights=True
        )
    ]

    # Train – shuffle=False to keep sequences ordered deterministically
    history = model.fit(
        X_train,
        y_train,
        epochs=100,
        batch_size=16,
        verbose=1,
        validation_split=0.1,
        shuffle=False,
        callbacks=callbacks,
    )

    # Predict on test
    y_pred_scaled = model.predict(X_test).flatten()

    # Inverse scale (test)
    y_test_true = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()
    y_test_pred = scaler.inverse_transform(
        y_pred_scaled.reshape(-1, 1)
    ).flatten()

    # Metrics
    rmse = np.sqrt(mean_squared_error(y_test_true, y_test_pred))
    test_mape = mape(y_test_true, y_test_pred)
    r2 = r2_score(y_test_true, y_test_pred)

    if np.isnan(test_mape):
        accuracy_pct = np.nan
    else:
        accuracy_pct = max(0.0, 100.0 - test_mape)

    print(
        "\n=== LSTM Forecast Performance (weekly, last {} points) ===".format(
            test_points
        )
    )
    print(f"RMSE: {rmse:.3f}")
    if np.isnan(test_mape):
        print("MAPE: cannot be computed reliably (all true values are ~0).")
        print("Accuracy: not defined.")
    else:
        print(f"MAPE: {test_mape:.3f}%")
        print(
            f"Approx. Forecast Accuracy (100 - MAPE, clipped): {accuracy_pct:.2f}%"
        )
    print(f"R²:   {r2:.4f}")

    # ---- Base metrics dict ----
    metrics = {
        "rmse": float(rmse),
        "mape": float(test_mape) if not np.isnan(test_mape) else None,
        "r2": float(r2),
        "accuracy_pct": float(accuracy_pct)
        if not np.isnan(accuracy_pct)
        else None,
    }

    # ===== 4-WEEK FUTURE FORECAST (RECURSIVE) =====
    last_lookback_scaled = y_scaled[-lookback:]
    window = last_lookback_scaled.reshape(1, lookback, 1)

    future_scaled = []
    steps_ahead = 4
    for _ in range(steps_ahead):
        next_scaled = model.predict(window, verbose=0)[0, 0]
        future_scaled.append(next_scaled)
        # shift window and append new prediction
        window = np.roll(window, -1, axis=1)
        window[0, -1, 0] = next_scaled

    future_scaled = np.array(future_scaled)
    future_pred = scaler.inverse_transform(
        future_scaled.reshape(-1, 1)
    ).flatten()

    # ---- IMPORTANT: dates based on latest raw date, not weekly bucket ----
    future_dates = [
        last_raw_date + pd.Timedelta(weeks=i + 1) for i in range(steps_ahead)
    ]

    next4_lstm_df = pd.DataFrame(
        {
            "ds": future_dates,
            "yhat_lstm": future_pred,
        }
    )
    next4_lstm_df.to_csv(NEXT4W_LSTM_PATH, index=False)
    print(
        f"Saved next 4-week LSTM forecast (total sales) to {NEXT4W_LSTM_PATH}"
    )

    # ------ KPI CALCULATIONS from raw weekly series + LSTM forecast ------
    # last 4 actual weeks total (same horizon used for test_points)
    last4_total = float(y_series[-test_points:].sum())
    prev4_total = (
        float(y_series[-2 * test_points : -test_points].sum())
        if len(y_series) >= 2 * test_points
        else None
    )
    next4_total = float(future_pred.sum())

    pct_last_vs_prev = None
    if prev4_total is not None and prev4_total != 0:
        pct_last_vs_prev = (last4_total - prev4_total) / prev4_total * 100.0

    pct_next_vs_last = None
    if last4_total is not None and last4_total != 0:
        pct_next_vs_last = (next4_total - last4_total) / last4_total * 100.0

    print("\n=== KPI SUMMARY (from LSTM training) ===")
    if prev4_total is not None:
        print(f"Prev 4 weeks total:  {prev4_total:,.2f}")
    else:
        print("Prev 4 weeks total:  N/A (series too short)")
    print(f"Last 4 weeks total:  {last4_total:,.2f}")
    print(f"Next 4 weeks (LSTM): {next4_total:,.2f}")
    if pct_last_vs_prev is not None:
        print(f"Change (last vs prev): {pct_last_vs_prev:+.2f}%")
    if pct_next_vs_last is not None:
        print(f"Change (next vs last): {pct_next_vs_last:+.2f}%")

    # extend metrics dict with KPI info (so CSV shows "how value is coming")
    metrics.update(
        {
            "prev4_total": prev4_total,
            "last4_total": last4_total,
            "next4_total_lstm": next4_total,
            "pct_last_vs_prev": pct_last_vs_prev,
            "pct_next_vs_last": pct_next_vs_last,
        }
    )

    # Save model + scaler
    model.save(LSTM_MODEL_PATH)
    joblib.dump(scaler, LSTM_SCALER_PATH)
    print(f"Saved LSTM weekly model to {LSTM_MODEL_PATH}")
    print(f"Saved LSTM scaler to {LSTM_SCALER_PATH}")

    # Save metrics (now includes KPIs)
    metrics_df = pd.DataFrame([metrics])
    metrics_df.to_csv(LSTM_METRICS_PATH, index=False)
    print(f"Saved LSTM forecast metrics (with KPIs) to {LSTM_METRICS_PATH}")

    return model, metrics, next4_lstm_df


# =========================================================
# 4. SEASON PEAKS, SHOCKS, SIMPLE ANOMALIES (ON DAILY)
# =========================================================

def detect_peaks_and_shocks(daily: pd.DataFrame):
    df = daily.copy().sort_values("ds")
    df["rolling_mean_7"] = df["y"].rolling(window=7, min_periods=3).mean()
    df["rolling_std_7"] = df["y"].rolling(window=7, min_periods=3).std()

    df["z_score"] = (df["y"] - df["rolling_mean_7"]) / df["rolling_std_7"]
    peaks = df[df["z_score"] > 2.5]

    df["diff"] = df["y"].diff()
    shock_threshold = df["diff"].abs().quantile(0.99)
    shocks = df[df["diff"].abs() > shock_threshold]

    print(f"\nDetected {len(peaks)} seasonal peaks (z_score > 2.5)")
    print(f"Detected {len(shocks)} strong shocks (top 1% changes)")

    peaks.to_csv(ARTIFACTS_DIR / "peaks.csv", index=False)
    shocks.to_csv(ARTIFACTS_DIR / "shocks.csv", index=False)

    return peaks, shocks


def detect_anomalies(daily: pd.DataFrame):
    """
    Simple anomaly detection using deviation from 7-day rolling mean.
    """
    df = daily.copy().sort_values("ds")
    df["rolling_mean_7"] = df["y"].rolling(window=7, min_periods=5).mean()
    df["rolling_std_7"] = df["y"].rolling(window=7, min_periods=5).std()

    df["z_score"] = (df["y"] - df["rolling_mean_7"]) / df["rolling_std_7"]
    anomalies = df[df["z_score"].abs() > 3]

    anomalies.to_csv(ARTIFACTS_DIR / "anomalies_daily.csv", index=False)
    print(
        f"Saved {len(anomalies)} anomalies (|z| > 3) to artifacts/anomalies_daily.csv"
    )

    return anomalies


# =========================================================
# 5. RFM SEGMENTATION (RULE-BASED + KMEANS)
# =========================================================

def compute_rfm(df: pd.DataFrame) -> pd.DataFrame:
    reference_date = df[DATE_COL].max()
    print("\nRFM reference date:", reference_date)

    rfm = (
        df.groupby(CUSTOMER_COL)
        .agg(
            {
                DATE_COL: lambda x: (reference_date - x.max()).days,
                INVOICE_COL: "nunique",
                "SalesAmount": "sum",
            }
        )
        .rename(
            columns={
                DATE_COL: "Recency",
                INVOICE_COL: "Frequency",
                "SalesAmount": "Monetary",
            }
        )
        .reset_index()
    )

    rfm = rfm[rfm["Monetary"] > 0]
    print("RFM customers:", len(rfm))
    return rfm


def rfm_rule_based(rfm: pd.DataFrame) -> pd.DataFrame:
    rfm = rfm.copy()

    r_quartiles = pd.qcut(rfm["Recency"], 4, labels=[4, 3, 2, 1])
    f_quartiles = pd.qcut(
        rfm["Frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4]
    )
    m_quartiles = pd.qcut(rfm["Monetary"], 4, labels=[1, 2, 3, 4])

    rfm["R_score"] = r_quartiles.astype(int)
    rfm["F_score"] = f_quartiles.astype(int)
    rfm["M_score"] = m_quartiles.astype(int)

    rfm["RFM_score"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]

    def assign_segment(row):
        if row["RFM_score"] >= 10:
            return "Champions"
        elif row["RFM_score"] >= 8:
            return "Loyal Customers"
        elif row["RFM_score"] >= 6:
            return "Potential Loyalists"
        elif row["RFM_score"] >= 4:
            return "At Risk"
        else:
            return "Lost Customers"

    rfm["Segment"] = rfm.apply(assign_segment, axis=1)

    return rfm


def rfm_kmeans(rfm: pd.DataFrame, n_clusters: int = 5):
    rfm_log = rfm[["Recency", "Frequency", "Monetary"]].copy()
    rfm_log["Recency"] = np.log1p(rfm_log["Recency"])
    rfm_log["Frequency"] = np.log1p(rfm_log["Frequency"])
    rfm_log["Monetary"] = np.log1p(rfm_log["Monetary"])

    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm_log)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    rfm["Cluster"] = kmeans.fit_predict(rfm_scaled)

    rfm["Score"] = (
        -rfm_log["Recency"] + rfm_log["Frequency"] + rfm_log["Monetary"]
    )
    cluster_scores = (
        rfm.groupby("Cluster")["Score"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    cluster_scores["Rank"] = cluster_scores["Score"].rank(
        ascending=False, method="dense"
    ).astype(int)

    cluster_to_segment = {}
    for _, row in cluster_scores.iterrows():
        if row["Rank"] == 1:
            label = "Champions"
        elif row["Rank"] == 2:
            label = "Loyal Customers"
        elif row["Rank"] == 3:
            label = "Potential Loyalists"
        elif row["Rank"] == 4:
            label = "At Risk"
        else:
            label = "Lost Customers"
        cluster_to_segment[row["Cluster"]] = label

    rfm["Segment"] = rfm["Cluster"].map(cluster_to_segment)

    SEGMENT_OFFERS = {
        "Champions": "Offer 15–20% VIP discount and early access.",
        "Loyal Customers": "Offer 10% loyalty discount + referral bonus.",
        "Potential Loyalists": "Send personalized recommendations + 5–10% coupon.",
        "At Risk": "Re-engagement campaign with 10–12% win-back offer.",
        "Lost Customers": "Strong limited-time reactivation coupon.",
    }
    rfm["Offer"] = rfm["Segment"].map(SEGMENT_OFFERS)

    joblib.dump(
        {"scaler": scaler, "kmeans": kmeans}, MODELS_DIR / "rfm_kmeans.pkl"
    )
    print(f"Saved RFM KMeans model to {MODELS_DIR / 'rfm_kmeans.pkl'}")

    return rfm


def plot_customer_segmentation_pie(rfm_df, file_path):
    """
    Pie chart of RFM customer segments.
    """
    segment_counts = rfm_df["Segment"].value_counts()

    plt.figure(figsize=(8, 8))
    plt.pie(
        segment_counts,
        labels=segment_counts.index,
        autopct="%1.1f%%",
        startangle=140,
    )
    plt.title("Customer Segmentation (RFM)")
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()
    print(f"Saved pie chart: {file_path}")


# =========================================================
# 6. MAIN DRIVER
# =========================================================

def main():
    TEST_POINTS = 4  # 4-week evaluation horizon

    # 1. Load raw data
    df_raw = load_raw_data()

    # 2. Clean data
    df = basic_cleaning(df_raw)

    # 3. Save cleaned data
    df.to_csv(CLEANED_DATA_PATH, index=False)
    print(f"Saved cleaned data to {CLEANED_DATA_PATH}")

    # 4. EDA on cleaned data (also get EDA dfs for plots)
    monthly_sales, top_products, top_countries = perform_eda(df)

    # Latest raw date for anchoring future weeks
    last_raw_date = df[DATE_COL].max()
    print(f"\nLatest date in dataset (raw): {last_raw_date}")

    # 5. Aggregations
    daily = build_daily_sales(df)
    weekly = build_weekly_sales(df)
    cat_sales = build_category_sales(df)
    country_sales = build_country_sales(df)

    daily.to_csv(DAILY_SALES_PATH, index=False)
    weekly.to_csv(WEEKLY_SALES_PATH, index=False)
    cat_sales.to_csv(CATEGORY_SALES_PATH, index=False)
    country_sales.to_csv(COUNTRY_SALES_PATH, index=False)

    print(f"\nSaved daily sales to    {DAILY_SALES_PATH}")
    print(f"Saved weekly sales to   {WEEKLY_SALES_PATH}")
    print(f"Saved category sales to {CATEGORY_SALES_PATH}")
    print(f"Saved country sales to  {COUNTRY_SALES_PATH}")

    # ------ PLOTS for artifacts ------

    # Daily sales time series
    plot_time_series(
        daily,
        date_col="ds",
        value_col="y",
        title="Daily Sales",
        y_label="SalesAmount",
        file_path=PLOTS_DIR / "daily_sales.png",
    )

    # Weekly sales time series
    plot_time_series(
        weekly,
        date_col="ds",
        value_col="y",
        title="Weekly Sales",
        y_label="SalesAmount",
        file_path=PLOTS_DIR / "weekly_sales.png",
    )

    # Monthly sales time series (from EDA)
    plot_time_series(
        monthly_sales,
        date_col="InvoiceMonth",
        value_col="SalesAmount",
        title="Monthly Sales",
        y_label="SalesAmount",
        file_path=PLOTS_DIR / "monthly_sales.png",
    )

    # Top products bar plot
    plot_bar(
        top_products,
        x_col=DESC_COL,
        y_col="SalesAmount",
        title="Top 20 Products by Sales",
        x_label="Product Description",
        y_label="SalesAmount",
        file_path=PLOTS_DIR / "top_products.png",
        rotation=75,
    )

    # Top countries bar plot
    plot_bar(
        top_countries,
        x_col=COUNTRY_COL,
        y_col="SalesAmount",
        title="Top 20 Countries by Sales",
        x_label="Country",
        y_label="SalesAmount",
        file_path=PLOTS_DIR / "top_countries.png",
        rotation=45,
    )

    # 6. LSTM model on WEEKLY data (4-week evaluation + 4-week future forecast)
    lstm_metrics = None
    next4_lstm_df = None
    if tf is not None:
        try:
            lstm_model, lstm_metrics, next4_lstm_df = train_lstm_forecaster(
                weekly,
                last_raw_date=last_raw_date,
                lookback=12,
                test_points=TEST_POINTS,
            )
        except Exception as e:
            print("⚠️ LSTM training failed due to:", e)
    else:
        print(
            "⚠️ Skipping LSTM: TensorFlow not available or import failed."
        )

    if lstm_metrics and lstm_metrics.get("accuracy_pct") is not None:
        print(
            f"➡ Final Weekly Forecast Accuracy (LSTM, 100 - MAPE): {lstm_metrics['accuracy_pct']:.2f}%"
        )
        print(
            f"➡ Next 4-week LSTM forecast (total) saved to: {NEXT4W_LSTM_PATH}"
        )

    # LSTM forecast plot (history + next 4 weeks)
    if next4_lstm_df is not None:
        plot_lstm_forecast(
            weekly_df=weekly,
            forecast_df=next4_lstm_df,
            file_path=PLOTS_DIR / "lstm_forecast_next4weeks.png",
        )

    # 6b. Demographic breakdown of forecast (Country / Category)
    if next4_lstm_df is not None:
        # Country shares
        country_share = df.groupby(COUNTRY_COL)["SalesAmount"].sum()
        country_share = country_share / country_share.sum()
        country_share = country_share.sort_values(ascending=False)

        # Category (product description) shares
        category_share = df.groupby(DESC_COL)["SalesAmount"].sum()
        category_share = category_share / category_share.sum()
        category_share = category_share.sort_values(ascending=False)

        # For practicality, only use top N for each demographic
        TOP_N_COUNTRIES = 5
        TOP_N_CATEGORIES = 5

        top_country_share = country_share.head(TOP_N_COUNTRIES)
        top_category_share = category_share.head(TOP_N_CATEGORIES)

        # Expand next4_lstm_df for countries
        rows_country = []
        for _, row in next4_lstm_df.iterrows():
            ds = row["ds"]
            total_pred = row["yhat_lstm"]
            for country, share in top_country_share.items():
                rows_country.append(
                    {
                        "ds": ds,
                        "Country": country,
                        "share": share,
                        "yhat_lstm_country": total_pred * share,
                    }
                )
        next4_country_df = pd.DataFrame(rows_country)
        next4_country_df.to_csv(
            NEXT4W_LSTM_BY_COUNTRY_PATH, index=False
        )
        print(
            f"Saved next 4-week LSTM forecast by COUNTRY to {NEXT4W_LSTM_BY_COUNTRY_PATH}"
        )

        # Expand next4_lstm_df for categories (products)
        rows_category = []
        for _, row in next4_lstm_df.iterrows():
            ds = row["ds"]
            total_pred = row["yhat_lstm"]
            for desc, share in top_category_share.items():
                rows_category.append(
                    {
                        "ds": ds,
                        "Description": desc,
                        "share": share,
                        "yhat_lstm_category": total_pred * share,
                    }
                )
        next4_category_df = pd.DataFrame(rows_category)
        next4_category_df.to_csv(
            NEXT4W_LSTM_BY_CATEGORY_PATH, index=False
        )
        print(
            f"Saved next 4-week LSTM forecast by CATEGORY to {NEXT4W_LSTM_BY_CATEGORY_PATH}"
        )

    # --- KPI CALCULATIONS: last 4 weeks, prev 4 weeks, next 4 weeks (LSTM) ---
    # This block gives you the exact table for dashboard cards.
    if next4_lstm_df is not None:
        weekly_sorted = weekly.sort_values("ds")

        # Last 4 weeks actual
        last4 = weekly_sorted.tail(4)["y"]
        last4_total = float(last4.sum())

        # Previous 4 weeks
        prev4 = weekly_sorted.iloc[-8:-4]["y"]
        prev4_total = float(prev4.sum()) if len(prev4) == 4 else None

        # Next 4 weeks forecast total (LSTM)
        next4_total = float(next4_lstm_df["yhat_lstm"].sum())

        pct_change_last_vs_prev = (
            ((last4_total - prev4_total) / prev4_total * 100.0)
            if prev4_total is not None and prev4_total != 0
            else None
        )

        pct_change_next_vs_last = (
            ((next4_total - last4_total) / last4_total * 100.0)
            if last4_total != 0
            else None
        )

        print("\n=== KPI SUMMARY (Weekly, from main) ===")
        if prev4_total is not None:
            print(f"Prev 4 weeks total:   {prev4_total:,.2f}")
        else:
            print("Prev 4 weeks total:   N/A (series too short)")
        print(f"Last 4 weeks total:   {last4_total:,.2f}")
        print(f"Next 4 weeks (LSTM):  {next4_total:,.2f}")
        if pct_change_last_vs_prev is not None:
            print(f"Change (last vs prev): {pct_change_last_vs_prev:+.2f}%")
        if pct_change_next_vs_last is not None:
            print(f"Change (next vs last): {pct_change_next_vs_last:+.2f}%")

        kpi_df = pd.DataFrame(
            [
                {
                    "prev4_total": prev4_total,
                    "last4_total": last4_total,
                    "next4_total_lstm": next4_total,
                    "pct_last_vs_prev": pct_change_last_vs_prev,
                    "pct_next_vs_last": pct_change_next_vs_last,
                }
            ]
        )
        kpi_df.to_csv(
            ARTIFACTS_DIR / "kpi_summary_weekly.csv", index=False
        )
        print(
            f"Saved KPI summary table to {ARTIFACTS_DIR / 'kpi_summary_weekly.csv'}"
        )

    # 7. Peaks, shocks, anomalies (daily-level)
    peaks, shocks = detect_peaks_and_shocks(daily)
    anomalies = detect_anomalies(daily)

    # 8. RFM + segmentation
    rfm = compute_rfm(df)
    rfm_rule = rfm_rule_based(rfm)
    rfm_rule.to_csv(
        ARTIFACTS_DIR / "rfm_segments_rule_based.csv", index=False
    )
    print(
        f"Saved rule-based RFM segments to {ARTIFACTS_DIR / 'rfm_segments_rule_based.csv'}"
    )

    # Customer segmentation pie chart
    plot_customer_segmentation_pie(
        rfm_rule, PLOTS_DIR / "customer_segments_pie.png"
    )

    rfm_km = rfm_kmeans(rfm, n_clusters=5)
    rfm_km.to_csv(
        ARTIFACTS_DIR / "rfm_segments_kmeans.csv", index=False
    )
    print(
        f"Saved KMeans RFM segments to {ARTIFACTS_DIR / 'rfm_segments_kmeans.csv'}"
    )

    print(
        "\n✅ ALL TASKS COMPLETED (CLEANING + EDA + LSTM 4-WEEK FORECAST + DEMOGRAPHICS + CRM + PLOTS):"
    )
    print("- Data cleaned and saved")
    print(
        "- EDA CSVs (missing, describe, monthly trend, top products, top countries) saved"
    )
    print(f"- Plots saved in: {PLOTS_DIR}")
    if lstm_metrics and lstm_metrics.get("accuracy_pct") is not None:
        print("- LSTM weekly forecast + metrics (4-week test)")
        print(
            f"  ▸ LSTM Accuracy (100 - MAPE): {lstm_metrics['accuracy_pct']:.2f}%"
        )
        print(
            f"- Next 4-week LSTM TOTAL forecast CSV: {NEXT4W_LSTM_PATH}"
        )
        print(
            f"- Next 4-week LSTM forecast BY COUNTRY: {NEXT4W_LSTM_BY_COUNTRY_PATH}"
        )
        print(
            f"- Next 4-week LSTM forecast BY CATEGORY: {NEXT4W_LSTM_BY_CATEGORY_PATH}"
        )
        print(
            f"- LSTM forecast plot: {PLOTS_DIR / 'lstm_forecast_next4weeks.png'}"
        )
    else:
        print("- LSTM metrics: not available (see earlier warnings).")
    print("- Peaks + shocks + anomalies saved (daily)")
    print("- RFM (rule-based + KMeans) saved")
    print("- Aggregates for daily/weekly/country/category saved")
    print(f"- LSTM metrics stored at:   {LSTM_METRICS_PATH}")


if __name__ == "__main__":
    main()
