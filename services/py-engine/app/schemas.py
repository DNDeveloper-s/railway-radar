from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class TrainTelemetry(BaseModel):
    train_number: str
    status: Literal["ON_TIME", "DELAYED", "CANCELLED"]
    latitude: float
    longitude: float
    delay_minutes: int
    station_code: str


class StoredTelemetry(TrainTelemetry):
    fetched_at: datetime
