import logging
from pathlib import Path


def setup_logger(filename="integration_test.log", output_dir="reports"):
    # Create reports directory if it doesn't exist
    log_dir = Path(output_dir)
    log_dir.mkdir(exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_dir / filename, encoding="utf-8"),
            logging.StreamHandler()
        ],
        force=True
    )
