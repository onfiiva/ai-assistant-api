import httpx
from typing import Optional, Dict


class BaseHTTPClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json"
        }

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        return headers

    async def _get(self, endpoint: str, timeout: float):
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(
                f"{self.base_url}{endpoint}",
                headers=self._get_headers()
            )

            if response.status_code >= 400:
                raise RuntimeError(
                    f"HTTP {response.status_code}: {response.text}"
                )

            return response

    async def _post(self, endpoint: str, json_payload: dict, timeout: float):
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{self.base_url}{endpoint}",
                json=json_payload,
                headers=self._get_headers()
            )

            if response.status_code >= 400:
                raise RuntimeError(
                    f"HTTP {response.status_code}: {response.text}"
                )

            return response
