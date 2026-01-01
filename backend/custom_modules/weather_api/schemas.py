from pydantic import BaseModel


class LocationWeatherSchema(BaseModel):
    name: str
    region: str
    country: str
    lat: float
    lon: float
    tz_id: str
    localtime_epoch: int
    localtime: str


class ConditionWeatherSchema(BaseModel):
    text: str
    icon: str
    code: int


class CurrentWeatherSchema(BaseModel):
    last_updated_epoch: int
    last_updated: str
    temp_c: float
    temp_f: float
    is_day: int
    condition: ConditionWeatherSchema
    wind_mph: float
    wind_kph: float
    wind_degree: int
    wind_dir: str
    pressure_mb: float
    pressure_in: float
    precip_mm: float
    precip_in: float
    humidity: int
    cloud: int
    feelslike_c: float
    feelslike_f: float
    windchill_c: float
    windchill_f: float
    heatindex_c: float
    heatindex_f: float
    dewpoint_c: float
    dewpoint_f: float
    vis_km: float
    vis_miles: float
    uv: float
    gust_mph: float
    gust_kph: float


class ResponseCurrentWeatherSchema(BaseModel):
    location: LocationWeatherSchema
    current: CurrentWeatherSchema
