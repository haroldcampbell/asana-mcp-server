import time
from typing import Any, Dict, Optional

import httpx

from src.config import get_settings


class AsanaError(RuntimeError):
    def __init__(self, status_code: int, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details or {}


def _is_retryable(status_code: int) -> bool:
    return status_code in {429, 500, 502, 503, 504}


class AsanaClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.asana_api_base.rstrip("/")
        self.timeout = settings.asana_timeout_seconds
        self.max_retries = settings.asana_max_retries
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {settings.asana_access_token}"},
            timeout=self.timeout,
        )

    def close(self) -> None:
        self._client.close()

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        for attempt in range(self.max_retries + 1):
            response = self._client.request(
                method,
                path,
                params=params,
                json=payload,
            )
            if response.status_code < 400:
                return response.json()

            if _is_retryable(response.status_code) and attempt < self.max_retries:
                retry_after = response.headers.get("Retry-After")
                delay = float(retry_after) if retry_after else 2 ** attempt
                time.sleep(delay)
                continue

            try:
                data = response.json()
            except ValueError:
                data = {"message": response.text}
            raise AsanaError(response.status_code, "Asana API error", data)

        raise AsanaError(500, "Asana API retry exhaustion")
