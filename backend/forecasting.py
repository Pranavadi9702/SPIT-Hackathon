# forecasting.py
from typing import List


def generate_4_week_forecast(historical_sales: List[float]) -> List[float]:
    if not historical_sales:
        avg = 0.0
    elif len(historical_sales) < 7:
        avg = float(sum(historical_sales) / len(historical_sales))
    else:
        avg = float(sum(historical_sales[-7:]) / 7.0)

    forecast = [avg] * 28  # 4 weeks * 7 days
    return forecast


def aggregate_forecast_value(forecast: List[float]) -> float:
    return float(sum(forecast))
