
import logging
from urllib.parse import urlparse

from ddgs import DDGS

logger = logging.getLogger(__name__)


class WebResearchError(Exception):
    """Raised when the external search provider fails."""


def search_web(query: str, max_results: int = 5) -> list[dict[str, str]]:
    """Search the web and return unique, structured source results."""
    try:
        raw_results = DDGS(timeout=10).text(
            query,
            region="in-en",
            safesearch="moderate",
            max_results=max_results,
        )

        results: list[dict[str, str]] = []
        seen_urls: set[str] = set()

        for item in raw_results or []:
            title = str(item.get("title") or "").strip()
            url = str(item.get("href") or item.get("url") or "").strip()
            snippet = str(item.get("body") or item.get("snippet") or "").strip()

            parsed_url = urlparse(url)

            # Keep only valid HTTP(S) source links.
            if (
                not title
                or parsed_url.scheme not in {"http", "https"}
                or not parsed_url.netloc
                or url in seen_urls
            ):
                continue

            seen_urls.add(url)
            results.append(
                {
                    "title": title,
                    "url": url,
                    "snippet": snippet,
                }
            )

            if len(results) >= max_results:
                break

        logger.info(
            "Web research completed: query_length=%d, results=%d",
            len(query),
            len(results),
        )
        return results

    except Exception as exc:
        logger.exception("External web research failed")
        raise WebResearchError(
            "External web search is temporarily unavailable."
        ) from exc
