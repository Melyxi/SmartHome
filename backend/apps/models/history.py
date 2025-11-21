from enum import Enum
from typing import TypeAlias

from pydantic import BaseModel

ScalarType: TypeAlias = int | str | float | bool | None


class ResultFormat(str, Enum):
    JSON = "JSON"


class QuerySchema(BaseModel):
    device_unique_name: str
    fields: list[str]
    row_limit: int


class HistoryDataQuerySchema(BaseModel):
    queries: list[QuerySchema]
    result_format: ResultFormat


class PresetsSchema(BaseModel):
    description: str
    name: str
    value: ScalarType = None


class ColumnPropertiesSchema(BaseModel):
    description: str | None = None
    label: str
    name: str
    property: str
    type: str
    value_off: str | bool | None = None
    value_on: str | bool | None = None
    values: list[str] | None = None
    category: str | None = None
    value_max: int | None = None
    value_min: int | None = None
    features: list["ColumnPropertiesSchema"] | None = None
    presets: list[PresetsSchema] | None = None


class HistoryDataResponseSchema(BaseModel):
    colnames: list[str]
    detailed_information: list[ColumnPropertiesSchema]
    data: list[dict]
    rowcount: int
    result_format: str
