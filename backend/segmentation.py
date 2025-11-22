# segmentation.py
from typing import List, Dict


def calculate_segments(customers: List[Dict]) -> List[Dict]:
    high_value = []
    medium_value = []
    low_value = []

    for c in customers:
        recency = c.get("recency", 5)
        frequency = c.get("frequency", 1)
        monetary = c.get("monetary", 1)

        score = (5 - recency) * 0.4 + frequency * 0.3 + monetary * 0.3

        if score >= 4:
            high_value.append(c["customer_id"])
        elif score >= 2.5:
            medium_value.append(c["customer_id"])
        else:
            low_value.append(c["customer_id"])

    segments: List[Dict] = []

    if high_value:
        segments.append(
            {
                "segment_name": "High Value",
                "customer_ids": high_value,
                "suggested_offer": "Exclusive 20% loyalty discount + early access",
            }
        )

    if medium_value:
        segments.append(
            {
                "segment_name": "Medium Value",
                "customer_ids": medium_value,
                "suggested_offer": "10% discount on next purchase",
            }
        )

    if low_value:
        segments.append(
            {
                "segment_name": "Low Value",
                "customer_ids": low_value,
                "suggested_offer": "Free shipping on next order",
            }
        )

    return segments
