# schemas.py
from typing import List
from pydantic import BaseModel


class ForecastRequest(BaseModel):
    historical_sales: List[float]


class Segment(BaseModel):
    segment_name: str
    customer_ids: List[str]
    suggested_offer: str


class ForecastAndCRMResponse(BaseModel):
    forecast: List[float]
    total_forecast_4_weeks: float
    segments: List[Segment]
    firestore_doc_id: str
    blockchain_tx_hash: str
