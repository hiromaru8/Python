import logging
from pathlib import Path


def setup_logger():
    # Create reports directory if it doesn't exist
    log_dir = Path("reports")
    log_dir.mkdir(exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "integration_test.log", encoding="utf-8"),
            logging.StreamHandler()
        ],
        force=True
    )
