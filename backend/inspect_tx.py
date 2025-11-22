import os
import sys
import json
from pathlib import Path

from web3 import Web3
from dotenv import load_dotenv

# Load .env (reuse same config as backend)
load_dotenv()

GANACHE_RPC_URL = os.getenv("GANACHE_RPC_URL", "http://127.0.0.1:7545")
CONTRACT_ADDRESS = os.getenv("FORECAST_CONTRACT_ADDRESS")

if CONTRACT_ADDRESS is None or CONTRACT_ADDRESS == "":
    raise RuntimeError("FORECAST_CONTRACT_ADDRESS not set in .env")

w3 = Web3(Web3.HTTPProvider(GANACHE_RPC_URL))

if not w3.is_connected():
    raise RuntimeError(f"Cannot connect to Ganache at {GANACHE_RPC_URL}")

# Load ABI from the same file you already use in backend
abi_path = Path(__file__).resolve().parent / "ForecastLogger_abi.json"
with open(abi_path, "r") as f:
    contract_json = json.load(f)

contract_abi = contract_json["abi"]
contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=contract_abi
)


def inspect_transaction(tx_hash_hex: str):
    print(f"\n🔎 Inspecting transaction: {tx_hash_hex}\n")

    # Get raw transaction + receipt
    tx = w3.eth.get_transaction(tx_hash_hex)
    receipt = w3.eth.get_transaction_receipt(tx_hash_hex)

    # Decode function + args from input data
    func_obj, func_args = contract.decode_function_input(tx["input"])

    print("➡ Function called on contract:")
    print(f"   {func_obj.fn_name}")
    print("\n➡ Arguments passed:")
    for key, value in func_args.items():
        print(f"   {key}: {value}")

    print("\n➡ Transaction metadata:")
    print(f"   From:        {tx['from']}")
    print(f"   To:          {tx['to']}")
    print(f"   Block:       {receipt['blockNumber']}")
    print(f"   Gas used:    {receipt['gasUsed']}")
    print(f"   Status:      {receipt['status']}  (1 = success)")

    # Also read current state from the contract
    latest_forecast = contract.functions.latestForecast().call()
    model_version = contract.functions.latestModelVersion().call()
    last_updated = contract.functions.lastUpdatedAt().call()

    print("\n📦 Current stored state in ForecastLogger:")
    print(f"   latestForecast:     {latest_forecast}")
    print(f"   latestModelVersion: {model_version}")
    print(f"   lastUpdatedAt:      {last_updated}  (unix timestamp)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inspect_tx.py <tx_hash>")
        print("Example:")
        print("  python inspect_tx.py 0x8c9478db5e42ea0ac174044579d3f0e1784689ec1cbc5f9e9239add60a6ff0ae")
        sys.exit(1)

    tx_hash = sys.argv[1].strip()
    inspect_transaction(tx_hash)
