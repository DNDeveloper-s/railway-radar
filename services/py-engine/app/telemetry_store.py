from datetime import UTC, datetime

from redis.asyncio import Redis

from app.config import settings
from app.schemas import StoredTelemetry, TrainTelemetry

_client: Redis | None = None


def get_redis() -> Redis:
    global _client
    if _client is None:
        _client = Redis.from_url(settings.redis_url, decode_responses=True)
    return _client


def telemetry_key(train_id: str) -> str:
    return f"train:{train_id}:telemetry"


async def set_telemetry(telemetry: TrainTelemetry) -> None:
    record = StoredTelemetry(**telemetry.model_dump(), fetched_at=datetime.now(UTC))
    await get_redis().set(
        telemetry_key(telemetry.train_number),
        record.model_dump_json(),
        ex=settings.telemetry_ttl_seconds,
    )


async def get_telemetry(train_id: str) -> StoredTelemetry | None:
    raw = await get_redis().get(telemetry_key(train_id))
    if raw is None:
        return None
    return StoredTelemetry.model_validate_json(raw)


def age_seconds(record: StoredTelemetry, now: datetime | None = None) -> float:
    now = now or datetime.now(UTC)
    return (now - record.fetched_at).total_seconds()


def is_stale(record: StoredTelemetry, now: datetime | None = None) -> bool:
    return age_seconds(record, now) > settings.telemetry_stale_after_seconds
