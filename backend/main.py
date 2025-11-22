# main.py
from typing import Optional, List, Dict

from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import ForecastRequest, ForecastAndCRMResponse, Segment # pyright: ignore[reportMissingImports]
from forecasting import generate_4_week_forecast, aggregate_forecast_value
from segmentation import calculate_segments # pyright: ignore[reportMissingImports]
from firebase_service import verify_id_token, save_forecast_to_firestore
from blockchain_service import save_forecast_on_chain

app = FastAPI(title="ChainForecast Backend")

# -------- CORS MIDDLEWARE --------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------- AUTH DEPENDENCY (Firebase ID Token) --------
def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    try:
        scheme, token = authorization.split()
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Authorization format")

    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Authorization scheme must be Bearer")

    try:
        decoded = verify_id_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

    return decoded  # contains fields like uid, email, etc.


@app.get("/health")
def health_check():
    return {"status": "ok"}


# -------- MAIN INTEGRATED ENDPOINT --------
@app.post("/api/forecast_and_crm", response_model=ForecastAndCRMResponse)
def forecast_and_crm(
    payload: ForecastRequest,
    # current_user: dict = Depends(get_current_user),
):
    current_user = {"uid": "demo-user"}

    # 1. Forecast
    forecast = generate_4_week_forecast(payload.historical_sales)
    total_forecast = aggregate_forecast_value(forecast)

    # 2. Dummy customers for segmentation (can replace with real RFM later)
    dummy_customers: List[Dict] = [
        {"customer_id": "C001", "recency": 1, "frequency": 10, "monetary": 5},
        {"customer_id": "C002", "recency": 3, "frequency": 5, "monetary": 3},
        {"customer_id": "C003", "recency": 5, "frequency": 2, "monetary": 1},
    ]
    segments_raw = calculate_segments(dummy_customers)

    segments: List[Segment] = [
        Segment(
            segment_name=s["segment_name"],
            customer_ids=s["customer_ids"],
            suggested_offer=s["suggested_offer"],
        )
        for s in segments_raw
    ]

    # 3. Save to Firestore
    doc_id = save_forecast_to_firestore(
        user_id=current_user["uid"],
        forecast_value=total_forecast,
        model_version="v1.0",
        segments=[s.dict() for s in segments],
    )

    # 4. Save to blockchain (use int for on-chain)
    tx_hash = save_forecast_on_chain(int(total_forecast), "v1.0")

    # 5. Return everything for dashboard UI
    return ForecastAndCRMResponse(
        forecast=forecast,
        total_forecast_4_weeks=total_forecast,
        segments=segments,
        firestore_doc_id=doc_id,
        blockchain_tx_hash=tx_hash,
    )
