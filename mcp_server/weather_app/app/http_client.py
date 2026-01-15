from typing import Any, Optional
import httpx
import logging

# from app.config import USER_AGENT, REQUEST_TIMEOUT
from app.config import WEATHER_API_BASE, WEATHER_API_KEY, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

# async def make_nws_request(url: str) -> Optional[dict[str, Any]]:
#     headers = {
#         "User-Agent": USER_AGENT,
#         "Accept": "application/geo+json",
#     }

#     async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
#         try:
#             response = await client.get(url, headers=headers)
#             response.raise_for_status()
#             return response.json()

#         except httpx.TimeoutException:
#             logger.error(f"Timeout while calling NWS API: {url}")

#         except httpx.HTTPStatusError as exc:
#             logger.error(
#                 f"NWS API error {exc.response.status_code} for {url}"
#             )

#         except Exception as exc:
#             logger.exception(f"Unexpected error calling NWS API: {exc}")

#     return None

async def make_nws_request(
    endpoint: str,
    params: dict[str, Any]
) -> Optional[dict[str, Any]]:

    params["key"] = WEATHER_API_KEY
    url = f"{WEATHER_API_BASE}/{endpoint}"

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

        except httpx.TimeoutException:
            logger.error(f"Timeout calling WeatherAPI: {url}")

        except httpx.HTTPStatusError as exc:
            logger.error(
                f"WeatherAPI error {exc.response.status_code}: {exc.response.text}"
            )

        except Exception as exc:
            logger.exception("Unexpected WeatherAPI error")

    return None
