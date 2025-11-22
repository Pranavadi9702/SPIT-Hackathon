# firebase_service.py
import firebase_admin
from firebase_admin import credentials, firestore, auth
from pathlib import Path

from config import settings

# Initialize Firebase Admin SDK
cred_path = Path(settings.firebase_credentials)

if not firebase_admin._apps:
    cred = credentials.Certificate(str(cred_path))
    firebase_admin.initialize_app(cred)

db = firestore.client()


def verify_id_token(id_token: str):
    """
    Verify Firebase ID token sent from the frontend.
    Returns decoded token with fields like uid, email, etc.
    """
    decoded = auth.verify_id_token(id_token)
    return decoded


def save_forecast_to_firestore(
    user_id: str,
    forecast_value: float,
    model_version: str,
    segments: list,
):
    """
    Store forecast + segments in Firestore.
    """
    doc_ref = db.collection("forecasts").document()
    doc_ref.set(
        {
            "user_id": user_id,
            "forecast_value": forecast_value,
            "model_version": model_version,
            "segments": segments,
        }
    )
    return doc_ref.id


def save_segments_to_firestore(user_id: str, segments: list):
    """
    Optionally store segmentation separately by user.
    """
    doc_ref = db.collection("segments").document(user_id)
    doc_ref.set({"segments": segments})
    return doc_ref.id
