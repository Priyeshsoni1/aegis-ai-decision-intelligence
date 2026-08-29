import logging

from app.config import get_settings
from app.logging import configure_logging


def main() -> None:
    settings = get_settings()

    configure_logging(settings.log_level)

    logger = logging.getLogger("aegis")

    logger.info(
        "Starting %s in %s environment",
        settings.app_name,
        settings.environment,
    )


if __name__ == "__main__":
    main()