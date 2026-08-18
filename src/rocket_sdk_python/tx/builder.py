from rocket_sdk_python.types.primitives import (
    AccountAddress,
    AssetId,
    InstrumentId,
    MMPTag,
    MarketMakerProtectionConfig,
)
from rocket_sdk_python.types.transaction.instruction import (
    CreateVaultData,
    CreateVaultInstruction,
    DeferredData,
    DeferredInstruction,
    ModifyTWAPInstruction,
    ModifyTWAPRequest,
    OrderRequestSet,
    PlaceOrderInstruction,
    PlaceTWAPInstruction,
    PlaceTWAPRequest,
    SetLeverageData,
    SetLeverageInstruction,
    SetMarketMakerProtectionData,
    SetMarketMakerProtectionInstruction,
    VaultDepositData,
    VaultDepositInstruction,
    VaultWithdrawData,
    VaultWithdrawInstruction,
    WithdrawData,
    WithdrawInstruction,
)
from rocket_sdk_python.types.transaction.sign import RawTransaction


def place_order(
    sender: AccountAddress,
    orders: OrderRequestSet,
    nonce: int,
) -> RawTransaction:
    return RawTransaction(
        sender=sender,
        instruction=PlaceOrderInstruction(PlaceOrder=orders),
        nonce=nonce,
    )


def place_twap(
    sender: AccountAddress,
    request: PlaceTWAPRequest,
    nonce: int,
) -> RawTransaction:
    return RawTransaction(
        sender=sender,
        instruction=PlaceTWAPInstruction(PlaceTWAP=request),
        nonce=nonce,
    )


def modify_twap(
    sender: AccountAddress,
    request: ModifyTWAPRequest,
    nonce: int,
) -> RawTransaction:
    return RawTransaction(
        sender=sender,
        instruction=ModifyTWAPInstruction(ModifyTWAP=request),
        nonce=nonce,
    )


def deferred_orders(
    sender: AccountAddress,
    orders: OrderRequestSet,
    expires_at_ms: int,
    deferred_nonce: int,
) -> RawTransaction:
    return RawTransaction(
        sender=sender,
        instruction=DeferredInstruction(
            Deferred=DeferredData(expires_at_ms=expires_at_ms, orders=orders),
        ),
        nonce=deferred_nonce,
    )


def set_market_maker_protection(
    sender: AccountAddress,
    to: AccountAddress,
    mmp_tag: MMPTag,
    config: MarketMakerProtectionConfig,
    nonce: int,
) -> RawTransaction:
    return RawTransaction(
        sender=sender,
        instruction=SetMarketMakerProtectionInstruction(
            SetMarketMakerProtection=SetMarketMakerProtectionData(
                to=to, mmp_tag=mmp_tag, config=config
            ),
        ),
        nonce=nonce,
    )


def withdraw(
    sender: AccountAddress,
    asset_id: AssetId,
    amount: str,
    to: AccountAddress,
    nonce: int,
) -> RawTransaction:
    return RawTransaction(
        sender=sender,
        instruction=WithdrawInstruction(
            Withdraw=WithdrawData(asset_id=asset_id, amount=amount, to=to),
        ),
        nonce=nonce,
    )


def set_leverage(
    sender: AccountAddress,
    to: AccountAddress,
    instrument_id: InstrumentId,
    leverage: int,
    nonce: int,
) -> RawTransaction:
    return RawTransaction(
        sender=sender,
        instruction=SetLeverageInstruction(
            SetLeverage=SetLeverageData(
                to=to, instrument_id=instrument_id, leverage=leverage
            ),
        ),
        nonce=nonce,
    )


def create_vault(
    sender: AccountAddress,
    deposit_asset: AssetId,
    initial_deposit: str,
    nonce: int,
) -> RawTransaction:
    return RawTransaction(
        sender=sender,
        instruction=CreateVaultInstruction(
            CreateVault=CreateVaultData(
                deposit_asset=deposit_asset, initial_deposit=initial_deposit
            ),
        ),
        nonce=nonce,
    )


def vault_deposit(
    sender: AccountAddress,
    vault: AccountAddress,
    amount: str,
    nonce: int,
) -> RawTransaction:
    return RawTransaction(
        sender=sender,
        instruction=VaultDepositInstruction(
            VaultDeposit=VaultDepositData(vault=vault, amount=amount),
        ),
        nonce=nonce,
    )


def vault_withdraw(
    sender: AccountAddress,
    vault: AccountAddress,
    shares: str,
    nonce: int,
) -> RawTransaction:
    return RawTransaction(
        sender=sender,
        instruction=VaultWithdrawInstruction(
            VaultWithdraw=VaultWithdrawData(vault=vault, shares=shares),
        ),
        nonce=nonce,
    )
