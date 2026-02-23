# Rocket Chain Python SDK

Python SDK for interacting with Rocket Chain, a high-performance blockchain trading platform.

## Requirements

- Python 3.12 or higher
- Virtual environment (venv)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/rocketfoundation/rocket-sdk-python.git
cd rocket-sdk-python
```

### 2. Create and activate virtual environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -e .
```

### 4. For Development

```bash
pip install uv

uv add --dev ruff mypy pytest
```

## Quick Start

### Basic Usage

```python
from rocket_sdk_python import RocketSDK, OrderSide

rpc_url = "https://testnet.rocket-cluster-1.com"
private_key = "0x..."

sdk = RocketSDK(rpc_url=rpc_url, private_key=private_key)

instruments = sdk.list_instruments()
collateral = sdk.get_collateral()

sdk.place_limit_order(
    instrument_id=instrument_id,
    side=OrderSide.BUY,
    price="1850.50",
    quantity="1",
    reduce_only=False,
    take_profit=False,
)
```

### Environment Variables

Create a `.env` file in the `examples/` directory:

```
ROCKET_PRIVATE_KEY=0x...
ROCKET_RPC_URL=https://testnet.rocket-cluster-1.com
```

### Running Examples

```bash
cd examples
source ../.venv/bin/activate
python simple_bot.py
```

## API Overview

### SDK Initialization

```python
sdk = RocketSDK(rpc_url: str, private_key: str)
```

### Trading Operations

- `place_limit_order()` - Place a limit order
- `place_market_order()` - Place a market order
- `cancel_order()` - Cancel an existing order
- `modify_order()` - Modify an existing order

### Account Management

- `get_collateral()` - Get account collateral balances
- `get_open_positions()` - Get open positions
- `get_open_orders()` - Get open orders
- `set_leverage()` - Set leverage for an instrument

### Market Data

- `list_instruments()` - Get all available instruments
- `list_assets()` - Get all available assets
- `get_orderbook()` - Get orderbook for an instrument

### WebSocket Streaming

```python
from rocket_sdk_python.client.websocket import WebSocketClient

ws_client = WebSocketClient(ws_url="wss://testnet.rocket-cluster-1.com/ws")
await ws_client.connect()
await ws_client.subscribe_orderbook(instrument_id)
```

## Important Notes

### Price and Quantity Format

Always use decimal strings for price and quantity, not scaled integers:

```python
sdk.place_limit_order(
    instrument_id=instrument_id,
    side=OrderSide.BUY,
    price="1850.50",
    quantity="1",
)
```

### Signature Schemes

The SDK supports two signature schemes:
- EIP-191 (default) - Ethereum Signed Message format
- EIP-712 - Typed data signing

### Testnet

Default testnet endpoint: `https://testnet.rocket-cluster-1.com`

WebSocket endpoint: `wss://testnet.rocket-cluster-1.com/ws`

## Development

### Project Structure

```
rocket-sdk-python/
├── src/rocket_sdk_python/
│   ├── types/           # Type definitions
│   ├── client/          # HTTP and WebSocket clients
│   ├── transaction/     # Transaction builders
│   ├── signing/         # Signature implementations
│   └── sdk.py           # High-level SDK interface
├── examples/            # Example scripts
└── pyproject.toml       # Project configuration
```

### Running Tests

```bash
source .venv/bin/activate
pytest
```