import httpx
from pydantic import TypeAdapter

from rocket_sdk_python.types.primitives import (
    AccountAddress,
    AssetId,
    BlockTimestamp,
    InstrumentId,
    Round,
)
from rocket_sdk_python.types.rest import (
    CandleTimeframe,
    GetAccountFees,
    GetAccountFeesResponse,
    GetAccountNonce,
    GetAccountNonceResponse,
    GetAccountOrderEvents,
    GetAccountPositionFundingEvents,
    GetAssetsResponse,
    GetBridgeEvents,
    GetBridgeEventsResponse,
    GetCandles,
    GetCandlesResponse,
    GetCollateral,
    GetCollateralsResponse,
    GetFaucetClaim,
    GetFaucetClaimResponse,
    GetFundingRateEvents,
    GetFundingRateEventsResponse,
    GetGlobalFeesResponse,
    GetInstrumentsResponse,
    GetMaxLeverage,
    GetMaxLeverageResponse,
    GetOpenOrders,
    GetOpenOrdersResponse,
    GetOrderEventsResponse,
    GetPosition,
    GetPositionFundingEventsResponse,
    GetPositionsResponse,
    GetVaultHistory,
    GetVaultHistoryResponse,
    GetVaultStats,
    GetVaultStatsResponse,
    GetVaults,
    GetVaultsResponse,
)
from rocket_sdk_python.types.transaction.response import TransactionResponse
from rocket_sdk_python.types.transaction.sign import Transaction

_tx_response_adapter = TypeAdapter(TransactionResponse)


class RestClient:
    def __init__(self, base_url: str, timeout: float = 30.0):
        self._base_url = base_url.rstrip("/")
        self._client = httpx.Client(timeout=timeout)

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def _get(self, path: str, params: dict | None = None) -> dict:
        response = self._client.get(f"{self._base_url}{path}", params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, path: str, body) -> dict | str:
        response = self._client.post(f"{self._base_url}{path}", json=body)
        response.raise_for_status()
        return response.json()

    def _transform_rust_enum(self, obj, parent_key=None):
        """Transform Rust-style enum serialization to discriminated union format.

        Converts {"VariantName": {...}} to {"type": "VariantName", ...}
        Only transforms single-key dicts where the key looks like a variant name (capitalized).
        """
        if isinstance(obj, dict):
            # Check if this is a single-key dict with a capitalized key (Rust enum variant)
            if len(obj) == 1:
                key = next(iter(obj.keys()))
                # Only transform if the key starts with uppercase (variant name pattern)
                # and is not a known field name like 'results', 'instruments', etc.
                if key[0].isupper() and key not in ['PlaceOrder', 'CreateVault', 'VaultDeposit', 'VaultWithdraw', 'SetLeverage', 'Withdraw']:
                    value = obj[key]
                    transformed_value = self._transform_rust_enum(value, parent_key=key)

                    # Special case: Success/Err variants should have their content under 'event'/'message'
                    if key == "Success":
                        return {"type": key, "event": transformed_value}
                    elif key == "Err":
                        # Err might have a message field or be a simple string
                        if isinstance(transformed_value, dict):
                            return {"type": key, **transformed_value}
                        else:
                            return {"type": key, "message": transformed_value}
                    # For event data variants (placed, canceled, etc.), merge the fields
                    elif key.lower() in ["placed", "canceled", "modified", "fill", "rejected"]:
                        if isinstance(transformed_value, dict):
                            return {"type": key.capitalize(), **transformed_value}
                        else:
                            return {"type": key.capitalize(), "value": transformed_value}
                    # Default: merge fields
                    elif isinstance(transformed_value, dict):
                        return {"type": key, **transformed_value}
                    else:
                        return {"type": key, "value": transformed_value}

            # Recursively transform nested objects
            return {k: self._transform_rust_enum(v, parent_key=k) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._transform_rust_enum(item, parent_key=parent_key) for item in obj]
        else:
            return obj

    def submit_transaction(self, tx: Transaction) -> TransactionResponse:
        body = tx.model_dump(by_alias=True, mode="json")
        data = self._post("/transaction", body)

        # Transform Rust-style enum serialization
        data = self._transform_rust_enum(data)

        # API doesn't return a 'type' field at the top level, infer it from the instruction
        instruction = tx.data.instruction
        if hasattr(instruction, 'PlaceOrder'):
            data['type'] = 'PlaceOrder'
        elif hasattr(instruction, 'Withdraw'):
            data['type'] = 'Ok'  # Withdraw returns Ok response
        elif hasattr(instruction, 'CreateVault'):
            data['type'] = 'CreateVault'
        elif hasattr(instruction, 'VaultDeposit'):
            data['type'] = 'VaultDeposit'
        elif hasattr(instruction, 'VaultWithdraw'):
            data['type'] = 'VaultWithdraw'
        elif hasattr(instruction, 'SetLeverage'):
            data['type'] = 'Ok'  # SetLeverage returns Ok response
        else:
            # Default to Ok if we can't determine the type
            data['type'] = 'Ok'

        return _tx_response_adapter.validate_python(data)

    def submit_transactions_batch(self, txs: list[Transaction]) -> str:
        body = [tx.model_dump(by_alias=True, mode="json") for tx in txs]
        return self._post("/batch_transactions", body)

    def get_account_nonce(self, account: AccountAddress) -> int:
        params = GetAccountNonce(account=account).model_dump(by_alias=True, exclude_none=True)
        data = self._get("/account-nonce", params)
        return GetAccountNonceResponse.model_validate(data).nonce

    def get_account_fees(self, account: AccountAddress) -> GetAccountFeesResponse:
        params = GetAccountFees(account=account).model_dump(by_alias=True, exclude_none=True)
        data = self._get("/account-fees", params)
        return GetAccountFeesResponse.model_validate(data)

    def get_instruments(
        self, page_number: int | None = None, page_size: int | None = None
    ) -> GetInstrumentsResponse:
        params: dict = {}
        if page_number is not None:
            params["pageNumber"] = page_number
        if page_size is not None:
            params["pageSize"] = page_size
        data = self._get("/instruments", params or None)
        return GetInstrumentsResponse.model_validate(data)

    def get_assets(
        self, page_number: int | None = None, page_size: int | None = None
    ) -> GetAssetsResponse:
        params: dict = {}
        if page_number is not None:
            params["pageNumber"] = page_number
        if page_size is not None:
            params["pageSize"] = page_size
        data = self._get("/assets", params or None)
        return GetAssetsResponse.model_validate(data)

    def get_candles(
        self,
        instrument_id: InstrumentId,
        interval: CandleTimeframe,
        start_time: BlockTimestamp | None = None,
        end_time: BlockTimestamp | None = None,
        limit: int | None = None,
    ) -> GetCandlesResponse:
        q = GetCandles(
            instrument_id=instrument_id,
            interval=interval,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )
        params = q.model_dump(by_alias=True, exclude_none=True)
        data = self._get("/candles", params)
        return GetCandlesResponse.model_validate(data)

    def get_global_fees(self) -> GetGlobalFeesResponse:
        data = self._get("/fees")
        return GetGlobalFeesResponse.model_validate(data)

    def get_max_leverage(
        self, account: AccountAddress, instrument_id: InstrumentId
    ) -> GetMaxLeverageResponse:
        params = GetMaxLeverage(account=account, instrument_id=instrument_id).model_dump(
            by_alias=True
        )
        data = self._get("/max-leverage", params)
        return GetMaxLeverageResponse.model_validate(data)

    def get_funding_rate_events(
        self,
        instrument_id: InstrumentId,
        start_round: Round | None = None,
        end_round: Round | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> GetFundingRateEventsResponse:
        q = GetFundingRateEvents(
            instrument_id=instrument_id,
            start_round=start_round,
            end_round=end_round,
            page_number=page_number,
            page_size=page_size,
        )
        params = q.model_dump(by_alias=True, exclude_none=True)
        data = self._get("/funding-rate-events", params)
        return GetFundingRateEventsResponse.model_validate(data)

    def get_positions(
        self, account: AccountAddress, instrument_id: InstrumentId | None = None
    ) -> GetPositionsResponse:
        params = GetPosition(account=account, instrument_id=instrument_id).model_dump(
            by_alias=True, exclude_none=True
        )
        data = self._get("/position", params)
        return GetPositionsResponse.model_validate(data)

    def get_collateral(
        self, account: AccountAddress, asset_id: AssetId | None = None
    ) -> GetCollateralsResponse:
        params = GetCollateral(account=account, asset_id=asset_id).model_dump(
            by_alias=True, exclude_none=True
        )
        data = self._get("/collateral", params)
        return GetCollateralsResponse.model_validate(data)

    def get_open_orders(
        self,
        account: AccountAddress,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> GetOpenOrdersResponse:
        params = GetOpenOrders(
            account=account, page_number=page_number, page_size=page_size
        ).model_dump(by_alias=True, exclude_none=True)
        data = self._get("/open-orders", params)
        return GetOpenOrdersResponse.model_validate(data)

    def get_order_events(
        self,
        account: AccountAddress,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> GetOrderEventsResponse:
        params = GetAccountOrderEvents(
            account=account, page_number=page_number, page_size=page_size
        ).model_dump(by_alias=True, exclude_none=True)
        data = self._get("/order-events", params)
        return GetOrderEventsResponse.model_validate(data)

    def get_vaults(
        self, page_number: int | None = None, page_size: int | None = None
    ) -> GetVaultsResponse:
        params = GetVaults(page_number=page_number, page_size=page_size).model_dump(
            by_alias=True, exclude_none=True
        )
        data = self._get("/vaults", params or None)
        return GetVaultsResponse.model_validate(data)

    def get_vault_stats(
        self,
        from_: BlockTimestamp,
        to: BlockTimestamp,
        vault_addresses: list[AccountAddress] | None = None,
    ) -> GetVaultStatsResponse:
        params = GetVaultStats(
            from_=from_, to=to, vault_addresses=vault_addresses
        ).model_dump(by_alias=True, exclude_none=True)
        data = self._get("/vault-stats", params)
        return GetVaultStatsResponse.model_validate(data)

    def get_vault_history(
        self,
        vault: AccountAddress,
        user: AccountAddress | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> GetVaultHistoryResponse:
        params = GetVaultHistory(
            vault=vault, user=user, page_number=page_number, page_size=page_size
        ).model_dump(by_alias=True, exclude_none=True)
        data = self._get("/vault-history", params)
        return GetVaultHistoryResponse.model_validate(data)

    def get_bridge_events(
        self,
        account: AccountAddress | None = None,
        round_from: str | None = None,
        round_to: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> GetBridgeEventsResponse:
        params = GetBridgeEvents(
            account=account,
            round_from=round_from,
            round_to=round_to,
            page_number=page_number,
            page_size=page_size,
        ).model_dump(by_alias=True, exclude_none=True)
        data = self._get("/bridge-events", params or None)
        return GetBridgeEventsResponse.model_validate(data)

    def get_position_funding_events(
        self,
        account: AccountAddress,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> GetPositionFundingEventsResponse:
        params = GetAccountPositionFundingEvents(
            account=account, page_number=page_number, page_size=page_size
        ).model_dump(by_alias=True, exclude_none=True)
        data = self._get("/position-funding-events", params)
        return GetPositionFundingEventsResponse.model_validate(data)

    def faucet_claim(self, account: AccountAddress) -> GetFaucetClaimResponse:
        params = GetFaucetClaim(account=account).model_dump(by_alias=True)
        data = self._get("/faucet-claim", params)
        return GetFaucetClaimResponse.model_validate(data)

