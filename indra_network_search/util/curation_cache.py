import logging
from typing import Dict, Set, Optional
from datetime import datetime
from indra_db.client.principal.curation import get_curations

logger = logging.getLogger(__name__)


class CurationCache:
    _correct_set = {'correct', 'hypothesis', 'activity_amount'}

    def __init__(self):
        self._curation_cache: Dict[int, datetime] = {}

    def _update_cache(self):
        # todo: make a wrapper and wrap like the bio_ontology
        try:
            curations = get_curations()
            self._curation_cache = {
                cur["pa_hash"]: cur["date"]
                for cur in curations
                if cur["tag"] not in self._correct_set
            }
            logger.info(f"Got {len(self._curation_cache)} curations")
        except Exception as exc:
            logger.error(f"Could not connect to the DB: {exc}")

    def get_hashes(
        self, start: Optional[datetime] = None, end: Optional[datetime] = None
    ) -> Set[int]:
        # Update cache
        self._update_cache()

        # Get cache
        hdd = self._curation_cache

        # Filter to range
        if start is not None:
            hdd = {h: dt for h, dt in hdd.items() if dt > start}
        if end is not None:
            hdd = {h: dt for h, dt in hdd.items() if dt < end}
        return {h for h in hdd}

    def get_all_hashes(self) -> Set[int]:
        """Get all hashes present in the cache as a set

        Returns
        -------
        :
            The set of all hashes stored in the cache
        """
        self._update_cache()
        return {h for h in self._curation_cache}
