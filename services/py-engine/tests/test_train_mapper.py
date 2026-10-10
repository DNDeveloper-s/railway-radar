import json
from pathlib import Path

import pytest

from app.adapters.train_mapper import MappingError, to_telemetry
from app.models import LiveTrainData

MOCK_FILE = Path(__file__).parent.parent / "app" / "mock_railkit_live_train.json"


@pytest.fixture
def payload():
    """The real RailKit data for train 12626, as a plain dict that a test may change."""
    with open(MOCK_FILE, encoding="utf-8") as file:
        return json.load(file)["data"]


def convert(payload):
    return to_telemetry(LiveTrainData.model_validate(payload))


def test_maps_the_mock_train(payload):
    result = convert(payload)
    assert result.train_number == "12626"
    assert result.station_code == "VBC"
    assert result.latitude == 16.533818
    assert result.longitude == 80.619927
    assert result.delay_minutes == 18
    assert result.status == "DELAYED"


def test_a_station_missing_from_the_route_gives_a_clear_error(payload):
    payload["currentLocation"]["stnCode"] = "ZZZ"
    with pytest.raises(MappingError, match="ZZZ"):
        convert(payload)


def test_a_train_without_train_info_gives_a_clear_error(payload):
    payload["trainInfo"] = []
    with pytest.raises(MappingError, match="trainInfo"):
        convert(payload)


def test_the_result_is_small_and_has_no_route(payload):
    raw = convert(payload).model_dump_json()
    assert len(raw.encode("utf-8")) < 300
    assert "route" not in json.loads(raw)


@pytest.mark.parametrize(
    "delay, expected",
    [(0, "ON_TIME"), (4, "ON_TIME"), (5, "DELAYED"), (18, "DELAYED")],
)
def test_status_follows_the_delay(payload, delay, expected):
    payload["delayMinutes"] = delay
    assert convert(payload).status == expected


def test_a_cancelled_train_is_cancelled_even_with_no_delay(payload):
    payload["status"] = "cancelled"
    payload["delayMinutes"] = 0
    assert convert(payload).status == "CANCELLED"
