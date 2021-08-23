from typing import List
from datetime import datetime, timedelta
from indra_network_search.util.curation_cache import CurationCache

now = datetime.fromisocalendar(year=2000, week=1, day=1)


class MockCurationCache(CurationCache):
    def __init__(self, hashes: List[int]):
        super().__init__()
        self.hdd = {h: now + timedelta(minutes=m) for m, h in enumerate(hashes)}

    def _update_cache(self):
        """Override the parent class method for test purposes"""
        self._curation_cache = self.hdd


def test_curation_cache():
    hashes = [1234567890, -9876543210]
    mcc = MockCurationCache(hashes)
    assert mcc.get_all_hashes() == set(hashes)

    assert {hashes[0]} == mcc.get_hashes(end=now + timedelta(seconds=30))
    assert {hashes[1]} == mcc.get_hashes(start=now + timedelta(seconds=30))
