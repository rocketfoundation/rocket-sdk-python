# Rocket SDK Python Examples

This directory contains example scripts demonstrating how to use the Rocket SDK.

## Setup

### 1. Install the SDK

From the repository root:

```bash
source .venv/bin/activate
```

### 2. Configure credentials

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and set your credentials:

```
ROCKET_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
ROCKET_RPC_URL=ROCKET_RPC_URL
```

**Important:** Never commit your `.env` file to git. It's already in `.gitignore`.

### 3. Run the example

```bash
cd examples
python simple_bot.py
```

## Examples

### `simple_bot.py`

A basic trading bot that demonstrates:

- Connecting to Rocket Chain testnet
- Fetching available instruments
- Checking account collateral and positions
- Placing a limit order
- Fetching open orders
- Canceling an order

This example uses the high-level `RocketSDK` interface for simplicity.

## Security Notes

- **Never share your private key** or commit it to version control
- The `.env` file is gitignored by default
- For production use, consider using encrypted keystore files (future feature)
- The testnet URL is safe to commit: `https://testnet.rocket-cluster-1.com`

## Getting Your Private Key

You can export your private key from MetaMask or any Ethereum wallet:

1. Open MetaMask
2. Click the three dots menu
3. Select "Account details"
4. Click "Show private key"
5. Enter your password
6. Copy the private key (starts with `0x`)

**Warning:** Anyone with your private key has full control of your account. Only use testnet keys for examples.

