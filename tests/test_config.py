from app.config import Settings


def test_default_settings():
    settings = Settings()

    assert settings.app_name == "Aegis"
    assert settings.environment == "development"
    assert settings.log_level == "INFO"
    assert settings.postgres_port == 5432


def test_environment_aliases(monkeypatch):
    monkeypatch.setenv("AEGIS_ENV", "test")
    monkeypatch.setenv("AEGIS_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("POSTGRES_PORT", "5433")

    settings = Settings()

    assert settings.environment == "test"
    assert settings.log_level == "DEBUG"
    assert settings.postgres_port == 5433