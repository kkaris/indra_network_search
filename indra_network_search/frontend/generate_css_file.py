"""
This script generates a new CSS file and a new json resource file.
It should be run when new sources have been added to INDRA and the CSS file
and json resource file need to be updated to reflect the new sources.
"""

import logging
from copy import deepcopy
from pathlib import Path

logger = logging.getLogger(__name__)

ASSETS = Path(__file__).absolute().parent.joinpath("src/assets")
CSS_PATH = ASSETS.joinpath("sources.css").as_posix()
SOURCE_PATH = ASSETS.joinpath("source_list.json")


def update_sources_list_json():
    """Update the sources list JSON file read by SourceDisplay.vue."""
    import json

    from indra_db_service.api import sources_dict

    mod_sources = deepcopy(sources_dict)
    mod_sources["databases"] = ["fplx"] + sources_dict["databases"]

    with SOURCE_PATH.open("w") as fh:
        json.dump(mod_sources, fh, indent=2)


def main():
    from indra.assemblers.html.assembler import generate_source_css

    logger.info("Updating source lists")
    update_sources_list_json()
    logger.info(f"Regenerating source CSS at {CSS_PATH}")
    generate_source_css(fname=CSS_PATH)


if __name__ == "__main__":
    main()
