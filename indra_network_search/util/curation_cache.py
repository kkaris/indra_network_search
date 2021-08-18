import logging
from typing import Dict, Set
from datetime import datetime
from indra_db.client.principal.curation import get_curations

logger = logging.getLogger(__name__)


class CurationCache:
    def __init__(self):
        logger.info("Loading incorrect curations")
        curations = self._get_new_curations()
        incc = {
            cur["pa_hash"]: cur["date"]
            for cur in curations
            if cur["tag"] not in {"correct", "hypothesis", "act_vs_amt"}
        }
        self._curation_cache: Dict[int, datetime] = incc
        logger.info(f"Loaded {len(incc)} curations")

    @staticmethod
    def _get_new_curations():
        try:
            return get_curations()
        except Exception as exc:
            logger.error(f"Could not connect to the DB: {exc}")
            return []

    def update_cache(self):
        before = len(self._curation_cache)
        curations = self._get_new_curations()
        for cur in curations:
            if cur["pa_hash"] not in self._curation_cache:
                self._curation_cache[cur["pa_hash"]] = cur["date"]
        logger.info(f"Added {len(self._curation_cache) - before} curations")

    def get_all_hashes(self) -> Set[int]:
        return {h for h in self._curation_cache}
