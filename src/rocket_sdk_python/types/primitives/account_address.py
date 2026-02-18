from typing import Annotated

from pydantic import AfterValidator, BeforeValidator

AccountAddress = Annotated[
    str,
    BeforeValidator(lambda v: v if isinstance(v, str) else str(v)),
    AfterValidator(lambda v: v if v.startswith("0x") else f"0x{v}"),
]

