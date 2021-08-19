import logging
from typing import Dict, Set
from datetime import datetime, timedelta
from indra_db.client.principal.curation import get_curations

logger = logging.getLogger(__name__)


class CurationCache:
    _correct_set = {"correct", "hypothesis", "act_vs_amt"}
    _check_interval = timedelta(minutes=5)

    def __init__(self):
        self._curation_cache: Dict[int, datetime] = {}
        self.last_updated: datetime = datetime.utcnow()
        self.last_checked: datetime = datetime.utcnow() - self._check_interval
        self.update_cache(force=True)

    def _get_new_curations(self) -> Dict[int, datetime]:
        try:
            curations = get_curations()
            incc = {
                cur["pa_hash"]: cur["date"]
                for cur in curations
                if cur["tag"] not in self._correct_set
            }
            self.last_checked = datetime.utcnow()
            return incc
        except Exception as exc:
            logger.error(f"Could not connect to the DB: {exc}")
            return {}

    def update_cache(self, force: bool = False):
        """Update the hash: datetime dict

        To avoid re-running the update if multiple requests come in at high
        frequency, only check the database at regular intervals

        Parameters
        ----------
        force :
            If True, re-run the cache update, even if it's before the check
            interval
        """
        now = datetime.utcnow()
        if force or now - self.last_checked > self._check_interval:
            curations = self._get_new_curations()
            added_curations = 0
            for hsh, dt in curations.items():
                if hsh not in self._curation_cache:
                    self._curation_cache[hsh] = dt
                    added_curations += 1

            if added_curations > 0:
                self.last_updated = datetime.utcnow()
                logger.info(f"Added {added_curations} curations")

    def get_all_hashes(self) -> Set[int]:
        """Get all hashes present in the cache as a set

        Returns
        -------
        :
            The set of all hashes stored in the cache
        """
        return {h for h in self._curation_cache}
