from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives.aliases import (
    AssetId,
    AssetTicker,
    HaircutTick,
    PriceTick,
    ScenarioChange,
)


class Scenario(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    price: ScenarioChange
    vol: ScenarioChange


ScenarioGrid = list[Scenario]


class AssetRow(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: AssetId
    ticker: AssetTicker
    haircut: HaircutTick
    mark_price: PriceTick = Field(alias="markPrice")
    scenario_grid: ScenarioGrid = Field(alias="scenarioGrid")
    initial_scenario_grid: ScenarioGrid = Field(alias="initialScenarioGrid")


class AssetRowData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ticker: AssetTicker
    haircut: HaircutTick
    mark_price: PriceTick = Field(alias="markPrice")
    scenario_grid: ScenarioGrid = Field(alias="scenarioGrid")
    initial_scenario_grid: ScenarioGrid = Field(alias="initialScenarioGrid")

