import logging

import aiohttp
from bs4 import BeautifulSoup
from aiohttp_socks import ProxyConnector

from config import HTTP_TIMEOUT_SECONDS, PROXY_URL
from data.http_statuses import DESCRIPTIONS, KNOWN_CODES

logger = logging.getLogger(__name__)
BASE_URL = "https://http.cat/status/{code}"


def is_supported_code(code: int) -> bool:
    """Return whether HTTP Cats provides an image for this status code"""
    return code in KNOWN_CODES


def _extract_description(html: str) -> tuple[str | None, str | None]:
    """Extract the page title and description from an HTTP Cats page"""
    soup = BeautifulSoup(html, "html.parser")
    heading = soup.find("h1")
    description_heading = soup.find("h2", string="Description")

    if not heading:
        return None, None

    title = heading.get_text(" ", strip=True)
    paragraphs = []

    if description_heading:
        for element in description_heading.find_all_next():
            if element.name == "h2":
                break
            if element.name == "p":
                paragraphs.append(element.get_text(" ", strip=True))

    description = "\n\n".join(paragraphs)
    description = description.split("Developed by")[0].strip()
    description = description.split("Original Images by")[0].strip()

    return title, description or None


async def get_description(code: int) -> tuple[str, str]:
    """Fetch an HTTP status description, using local fallback data if needed"""
    timeout = aiohttp.ClientTimeout(total=HTTP_TIMEOUT_SECONDS)
    connector = ProxyConnector.from_url(PROXY_URL) if PROXY_URL else None

    try:
        async with aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
        ) as session:
            async with session.get(BASE_URL.format(code=code)) as response:
                if response.status == 200:
                    html = await response.text()
                    title, description = _extract_description(html)

                    if title and description:
                        return title, description[:2500]

                    if code in DESCRIPTIONS:
                        return DESCRIPTIONS[code]

                    if title:
                        return title, "A detailed description is not available."

                else:
                    logger.warning(
                        "HTTP Cats returned status %s for HTTP %s",
                        response.status,
                        code,
                    )
    except (aiohttp.ClientError, TimeoutError, ValueError):
        logger.exception("Failed to fetch the description for HTTP %s", code)

    if code in DESCRIPTIONS:
        return DESCRIPTIONS[code]

    return f"HTTP {code}", "The description is temporarily unavailable."
