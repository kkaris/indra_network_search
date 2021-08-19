import logging
from typing import Dict, Set
from datetime import datetime
from indra_db.client.principal.curation import get_curations

logger = logging.getLogger(__name__)


class CurationCache:
    _correct_set = {"correct", "hypothesis", "act_vs_amt"}

    def __init__(self):
        self._curation_cache: Dict[int, datetime] = {}
        self.update_cache()

    def _get_new_curations(self) -> Dict[int, datetime]:
        try:
            curations = get_curations()
            incc = {
                cur["pa_hash"]: cur["date"]
                for cur in curations
                if cur["tag"] not in self._correct_set
            }
            return incc
        except Exception as exc:
            logger.error(f"Could not connect to the DB: {exc}")
            return {}

    def update_cache(self):
        """Update the hash: datetime dict"""
        curations = self._get_new_curations()
        added_curations = 0
        for hsh, dt in curations.items():
            if hsh not in self._curation_cache:
                self._curation_cache[hsh] = dt
                added_curations += 1

        if added_curations > 0:
            logger.info(f"Added {added_curations} curations")
        else:
            logger.info("No New curations")

    def get_all_hashes(self) -> Set[int]:
        """Get all hashes present in the cache as a set

        Returns
        -------
        :
            The set of all hashes stored in the cache
        """
        self.update_cache()
        return {h for h in self._curation_cache}
