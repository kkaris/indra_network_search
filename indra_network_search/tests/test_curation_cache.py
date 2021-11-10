from typing import List

from indra_network_search.util.curation_cache import CurationCache


class MockCurationCache(CurationCache):
    def __init__(self, hashes: List[int]):
        super().__init__()
        self.hdd = set(hashes)

    def _update_cache(self):
        """Override the parent class method for test purposes"""
        self._curation_cache = self.hdd


def test_curation_cache():
    hashes = [1234567890, -9876543210]
    mcc = MockCurationCache(hashes)
    assert mcc.get_all_hashes() == set(hashes)
