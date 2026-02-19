from rocket_sdk_python.types.primitives import AccountAddress, AssetId, InstrumentId
from rocket_sdk_python.types.transaction.instruction import (
    CreateVaultData,
    CreateVaultInstruction,
    OrderRequestSet,
    PlaceOrderInstruction,
    SetLeverageData,
    SetLeverageInstruction,
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
            SetLeverage=SetLeverageData(to=to, instrument_id=instrument_id, leverage=leverage),
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

