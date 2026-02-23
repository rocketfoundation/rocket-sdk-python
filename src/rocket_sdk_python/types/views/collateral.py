from pydantic import RootModel

from rocket_sdk_python.types.primitives import AssetId

CollateralView = RootModel[dict[AssetId, str]]
