# config.py
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Settings:
    firebase_credentials: str
    ganache_rpc_url: str
    ganache_private_key: str
    ganache_account_address: str
    forecast_contract_address: str
    api_secret_key: str

    def __init__(self) -> None:
        self.firebase_credentials = os.getenv("FIREBASE_CREDENTIALS", "./firebase-key.json")
        self.ganache_rpc_url = os.getenv("GANACHE_RPC_URL", "http://127.0.0.1:7545")
        self.ganache_private_key = os.getenv("GANACHE_PRIVATE_KEY", "")
        self.ganache_account_address = os.getenv("GANACHE_ACCOUNT_ADDRESS", "")
        self.forecast_contract_address = os.getenv("FORECAST_CONTRACT_ADDRESS", "")
        self.api_secret_key = os.getenv("API_SECRET_KEY", "supersecret")


settings = Settings()
