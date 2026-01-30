import os
import pytest

from src import config


def test_missing_token_raises(monkeypatch):
    monkeypatch.setenv("ASANA_ACCESS_TOKEN", "")
    config.get_settings.cache_clear()
    with pytest.raises(RuntimeError):
        config.get_settings()


def test_valid_token_loads(monkeypatch):
    monkeypatch.setenv("ASANA_ACCESS_TOKEN", "token")
    config.get_settings.cache_clear()
    settings = config.get_settings()
    assert settings.asana_access_token == "token"


def test_token_file_preferred(monkeypatch, tmp_path):
    token_file = tmp_path / "asana.token"
    token_file.write_text("file-token", encoding="utf-8")
    monkeypatch.setenv("ASANA_TOKEN_FILE", str(token_file))
    monkeypatch.setenv("ASANA_ACCESS_TOKEN", "env-token")
    config.get_settings.cache_clear()
    settings = config.get_settings()
    assert settings.asana_access_token == "file-token"
