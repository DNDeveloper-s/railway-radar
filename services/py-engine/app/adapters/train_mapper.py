from typing import Literal

from app.models import LiveTrainData
from app.schemas import TrainTelemetry


class MappingError(Exception):
    """Raised when RailKit data cannot be turned into a telemetry record."""


DELAYED_FROM_MINUTES = 5


def _status(live: LiveTrainData) -> Literal["ON_TIME", "DELAYED", "CANCELLED"]:
    if "cancel" in live.status.lower() or "cancel" in live.statusText.lower():
        return "CANCELLED"
    if live.delayMinutes >= DELAYED_FROM_MINUTES:
        return "DELAYED"
    return "ON_TIME"


def to_telemetry(live: LiveTrainData) -> TrainTelemetry:
    if not live.trainInfo:
        raise MappingError("RailKit data has no trainInfo, so there is no train number")
    here = live.currentLocation.stnCode
    stop = next((p for p in live.route if p.stnCode == here), None)
    if stop is None:
        raise MappingError(f"Current station {here} is not in the route")
    return TrainTelemetry(
        train_number=live.trainInfo[0].number,
        status=_status(live),
        latitude=stop.cord.lat,
        longitude=stop.cord.lon,
        delay_minutes=live.delayMinutes,
        station_code=here,
    )
