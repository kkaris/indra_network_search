import logging
from pathlib import Path

from indra.assemblers.html.assembler import generate_source_css

logger = logging.getLogger(__name__)

CSS_PATH = Path(__file__).absolute().parent.joinpath("src/assets/sources.css").as_posix()

if __name__ == "__main__":
    logger.info(f"Regenerating source CSS at {CSS_PATH}")
    generate_source_css(fname=CSS_PATH)
