import logging
from urllib.parse import urljoin

from httpx import AsyncClient, RequestError
from settings import get_settings
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
async def request_get(endpoint: str, *args, **kwargs) -> dict:
    async with AsyncClient() as client:
        try:
            url = urljoin(get_settings().pokemon_api_base, endpoint)
            logger.info(
                f"Making GET request to {url} with args: {args} and kwargs: {kwargs}"
            )
            response = await client.get(url, *args, **kwargs)
            response.raise_for_status()
            logger.info(
                f"Received response from {url} with status code: {response.status_code}"
            )
            return response.json()
        except RequestError as e:
            logger.error(
                f"Error occurred while fetching data from {endpoint}: {e}",
                exc_info=True,
                extra={"endpoint": endpoint, "args": args, "kwargs": kwargs},
            )
