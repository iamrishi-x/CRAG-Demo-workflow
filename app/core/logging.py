"""Centralized logging setup."""

import logging
import logging.config
from pathlib import Path

import yaml


def setup_logging(config_path: str = "configs/logging.yaml") -> None:
    """Initialize logging from YAML config."""
    path = Path(config_path)
    if not path.exists():
        logging.basicConfig(level=logging.INFO)
        logging.getLogger(__name__).warning("Logging config not found: %s", config_path)
        return

    with path.open("r", encoding="utf-8") as stream:
        config = yaml.safe_load(stream)

    Path("logs").mkdir(parents=True, exist_ok=True)
    logging.config.dictConfig(config)
