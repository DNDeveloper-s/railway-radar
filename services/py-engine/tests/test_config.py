from app.config import Settings


def test_defaults_work_without_any_env_file(monkeypatch):
    monkeypatch.delenv("REDIS_URL", raising=False)
    monkeypatch.delenv("TELEMETRY_STALE_AFTER_SECONDS", raising=False)
    monkeypatch.delenv("USE_MOCK_RAILKIT", raising=False)
    s = Settings(_env_file=None)
    assert s.redis_url == "redis://localhost:6379/0"
    assert s.telemetry_stale_after_seconds == 60
    assert s.use_mock_railkit is True


def test_environment_variable_overrides_the_default(monkeypatch):
    monkeypatch.setenv("REDIS_URL", "redis://example:6380/1")
    assert Settings(_env_file=None).redis_url == "redis://example:6380/1"


def test_values_get_the_right_type(monkeypatch):
    monkeypatch.setenv("TELEMETRY_STALE_AFTER_SECONDS", "5")
    monkeypatch.setenv("USE_MOCK_RAILKIT", "false")
    s = Settings(_env_file=None)
    assert s.telemetry_stale_after_seconds == 5
    assert s.use_mock_railkit is False


def test_cors_origins_are_split_into_a_list(monkeypatch):
    monkeypatch.setenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:3000, https://railway-radar.vercel.app",
    )
    assert Settings(_env_file=None).cors_origins == [
        "http://localhost:3000",
        "https://railway-radar.vercel.app",
    ]


def test_the_api_key_is_not_printed(monkeypatch):
    monkeypatch.setenv("RAILKIT_API_KEY", "super-secret-value")
    s = Settings(_env_file=None)
    assert "super-secret-value" not in repr(s)
    assert s.railkit_api_key.get_secret_value() == "super-secret-value"


def test_values_are_read_from_an_env_local_file(tmp_path, monkeypatch):
    monkeypatch.delenv("TELEMETRY_STALE_AFTER_SECONDS", raising=False)
    env_file = tmp_path / ".env.local"
    env_file.write_text("TELEMETRY_STALE_AFTER_SECONDS=5\n", encoding="utf-8")
    assert Settings(_env_file=env_file).telemetry_stale_after_seconds == 5
