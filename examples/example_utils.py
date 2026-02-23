import os
import sys


def load_env_from_file(env_path: str = ".env"):
    if not os.path.exists(env_path):
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())


def get_credentials():
    load_env_from_file()

    private_key = os.environ.get("ROCKET_PRIVATE_KEY")
    rpc_url = os.environ.get("ROCKET_RPC_URL")

    if not private_key:
        print("Error: ROCKET_PRIVATE_KEY not set in environment or .env file")
        print("Copy .env.example to .env and set your private key")
        sys.exit(1)

    if not rpc_url:
        print("Error: ROCKET_RPC_URL not set in environment or .env file")
        print("Copy .env.example to .env and set your RPC URL")
        sys.exit(1)

    if not private_key.startswith("0x"):
        private_key = "0x" + private_key

    return private_key, rpc_url
