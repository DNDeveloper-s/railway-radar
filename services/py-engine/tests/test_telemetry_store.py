import json
from datetime import UTC, datetime, timedelta

import pytest
import pytest_asyncio
from fakeredis import FakeAsyncRedis

from app import telemetry_store
from app.config import settings
from app.schemas import StoredTelemetry, TrainTelemetry
from app.telemetry_store import (
    age_seconds,
    get_telemetry,
    is_stale,
    set_telemetry,
    telemetry_key,
)

pytestmark = pytest.mark.asyncio

EXAMPLE = TrainTelemetry(
    train_number="12626",
    status="DELAYED",
    latitude=16.533818,
    longitude=80.619927,
    delay_minutes=18,
    station_code="VBC",
)


@pytest_asyncio.fixture
async def fake_redis(monkeypatch):
    """A pretend Redis that lives inside the test. No Docker needed."""
    client = FakeAsyncRedis(decode_responses=True)
    monkeypatch.setattr(telemetry_store, "_client", client)
    yield client
    await client.aclose()


def make_record(seconds_old: float, now: datetime) -> StoredTelemetry:
    return StoredTelemetry(
        **EXAMPLE.model_dump(), fetched_at=now - timedelta(seconds=seconds_old)
    )


async def test_save_then_read_returns_the_same_data(fake_redis):
    await set_telemetry(EXAMPLE)
    record = await get_telemetry("12626")
    assert record is not None
    assert record.model_dump(exclude={"fetched_at"}) == EXAMPLE.model_dump()


async def test_fetched_at_is_stamped_by_us_in_utc(fake_redis):
    before = datetime.now(UTC)
    await set_telemetry(EXAMPLE)
    record = await get_telemetry("12626")
    assert record is not None
    assert record.fetched_at.utcoffset() == timedelta(0)
    assert before <= record.fetched_at <= datetime.now(UTC)


async def test_a_missing_train_returns_none(fake_redis):
    assert await get_telemetry("99999") is None


async def test_a_record_59_seconds_old_is_not_stale():
    now = datetime.now(UTC)
    assert is_stale(make_record(59, now), now) is False


async def test_a_record_61_seconds_old_is_stale():
    now = datetime.now(UTC)
    assert is_stale(make_record(61, now), now) is True


async def test_a_record_exactly_at_the_limit_is_not_stale():
    now = datetime.now(UTC)
    assert (
        is_stale(make_record(settings.telemetry_stale_after_seconds, now), now) is False
    )


async def test_age_seconds_measures_from_fetched_at():
    now = datetime.now(UTC)
    assert age_seconds(make_record(42, now), now) == 42


async def test_the_key_is_exactly_train_number_telemetry(fake_redis):
    assert telemetry_key("12626") == "train:12626:telemetry"
    await set_telemetry(EXAMPLE)
    assert await fake_redis.exists("train:12626:telemetry") == 1


async def test_the_key_has_an_expiry(fake_redis):
    await set_telemetry(EXAMPLE)
    ttl = await fake_redis.ttl("train:12626:telemetry")
    assert 0 < ttl <= settings.telemetry_ttl_seconds


async def test_the_saved_json_is_small_and_has_no_route(fake_redis):
    await set_telemetry(EXAMPLE)
    raw = await fake_redis.get("train:12626:telemetry")
    assert len(raw.encode("utf-8")) < 300
    saved = json.loads(raw)
    assert "route" not in saved
    assert "stops" not in saved
