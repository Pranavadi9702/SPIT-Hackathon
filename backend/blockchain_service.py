from web3 import Web3
from config import settings
import json
from pathlib import Path

# existing setup stays as you have it...
w3 = Web3(Web3.HTTPProvider(settings.ganache_rpc_url))

if not w3.is_connected():
    raise RuntimeError("Cannot connect to Ganache RPC URL")

CONTRACT_ADDRESS = Web3.to_checksum_address(settings.forecast_contract_address)

abi_path = Path(__file__).resolve().parent / "ForecastLogger_abi.json"
with open(abi_path, "r") as f:
    contract_json = json.load(f)

contract_abi = contract_json["abi"]
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

ACCOUNT_ADDRESS = Web3.to_checksum_address(settings.ganache_account_address)
PRIVATE_KEY = settings.ganache_private_key


def save_forecast_on_chain(forecast_value: int, model_version: str) -> str:
    """
    Send transaction to ForecastLogger.saveForecast(_value, _modelVersion)
    using web3.py v6 (raw_transaction attr).
    """
    nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)

    tx = contract.functions.saveForecast(
        forecast_value,
        model_version,
    ).build_transaction(
        {
            "from": ACCOUNT_ADDRESS,
            "nonce": nonce,
            "gas": 300_000,
            "gasPrice": w3.to_wei("1", "gwei"),
        }
    )

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)

    # send tx
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    # wait for confirmation (optional but nice for demo)
    w3.eth.wait_for_transaction_receipt(tx_hash)

    # just return the hash from send_raw_transaction
    return tx_hash.hex()
 