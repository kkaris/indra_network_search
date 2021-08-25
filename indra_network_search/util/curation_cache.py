import logging
from typing import Set, Optional
from collections import defaultdict
from indra_db.client.principal.curation import get_curations

logger = logging.getLogger(__name__)


class CurationCache:
    _correct_set = {'correct', 'hypothesis', 'activity_amount'}

    def __init__(self):
        self._curation_cache: Set[int] = set()

    def _update_cache(self):
        # todo: make a wrapper and wrap like the bio_ontology
        try:
            curations = get_curations()
            curs_by_hash = defaultdict(set)
            for cur in curations:
                curs_by_hash[cur["pa_hash"]].add(cur["tag"])

            self._curation_cache = {
                stmt_hash
                for stmt_hash, tags in curs_by_hash.items()
                if not tags & self._correct_set
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
        return self._curation_cache
