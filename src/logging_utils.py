import json
import logging
from logging.handlers import RotatingFileHandler
from typing import Any, Dict

SENSITIVE_KEYS = {
    "authorization",
    "access_token",
    "refresh_token",
    "token",
    "password",
    "secret",
    "notes",
    "email",
}


def _redact_value(value: Any) -> Any:
    if value is None:
        return value
    if isinstance(value, str):
        return "[REDACTED]"
    if isinstance(value, (bytes, bytearray)):
        return "[REDACTED]"
    return "[REDACTED]"


def redact_dict(payload: Any) -> Any:
    if isinstance(payload, dict):
        redacted: Dict[str, Any] = {}
        for key, value in payload.items():
            if key.lower() in SENSITIVE_KEYS:
                redacted[key] = _redact_value(value)
            else:
                redacted[key] = redact_dict(value)
        return redacted
    if isinstance(payload, list):
        return [redact_dict(item) for item in payload]
    return payload


def setup_logging(log_file: str, log_level: str) -> logging.Logger:
    logger = logging.getLogger("asana_mcp")
    if logger.handlers:
        return logger

    logger.setLevel(log_level.upper())

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )

    file_handler = RotatingFileHandler(
        log_file, maxBytes=5_000_000, backupCount=3
    )
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def audit(logger: logging.Logger, event: str, payload: Any) -> None:
    redacted = redact_dict(payload)
    message = json.dumps({"event": event, "payload": redacted}, sort_keys=True)
    logger.info(message)
