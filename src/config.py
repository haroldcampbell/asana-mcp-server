import logging
import os
from pathlib import Path
from functools import lru_cache
from pydantic import BaseModel, ConfigDict, Field, ValidationError


class Settings(BaseModel):
    model_config = ConfigDict(extra="ignore")

    asana_access_token: str = Field(min_length=1)
    asana_api_base: str = "https://app.asana.com/api/1.0"
    asana_timeout_seconds: float = 30.0
    asana_max_retries: int = 3
    log_level: str = "INFO"
    log_file: str = "logs/asana-mcp.log"

    @staticmethod
    def from_env() -> "Settings":
        logger = logging.getLogger("asana_mcp")
        token_file = None
        if "ASANA_TOKEN_FILE" in os.environ:
            token_file = os.environ.get("ASANA_TOKEN_FILE", "")
            logger.info("ASANA_TOKEN_FILE set (redacted)")
            if not token_file.strip():
                raise RuntimeError("ASANA_TOKEN_FILE is set but empty.")
        token_from_file = ""
        if token_file:
            token_path = Path(token_file)
            if token_path.exists():
                token_from_file = token_path.read_text(encoding="utf-8").strip()
                if not token_from_file:
                    logger.warning("ASANA_TOKEN_FILE is empty after trimming: %s", token_path)
            else:
                logger.warning("ASANA_TOKEN_FILE does not exist: %s", token_path)
        data = {
            "asana_access_token": token_from_file or os.getenv("ASANA_ACCESS_TOKEN", ""),
            "asana_api_base": os.getenv("ASANA_API_BASE", "https://app.asana.com/api/1.0"),
            "asana_timeout_seconds": float(os.getenv("ASANA_TIMEOUT_SECONDS", "30")),
            "asana_max_retries": int(os.getenv("ASANA_MAX_RETRIES", "3")),
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "log_file": os.getenv("LOG_FILE", "logs/asana-mcp.log"),
        }
        try:
            return Settings(**data)
        except ValidationError as exc:
            msg = (
                "Invalid configuration. Set ASANA_ACCESS_TOKEN or provide a valid "
                "ASANA_TOKEN_FILE with a non-empty token."
            )
            raise RuntimeError(msg) from exc


@lru_cache
def get_settings() -> Settings:
    return Settings.from_env()
