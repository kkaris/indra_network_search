"""
The QueryHandler's job is to act as a middle layer between the network
search functionalities and the REST API that receives queries.
"""
from typing import List, Tuple, Union, Dict, Set

from depmap_analysis.network_functions.net_functions import SIGN_TO_STANDARD
from indra_network_search.query import (
    UIQuery,
    ShortestSimplePathsQuery,
    BreadthFirstSearchQuery,
    DijkstraQuery,
    SharedTargetsQuery,
    OntologyQuery,
    SharedRegulatorsQuery,
)
from indra_network_search.data_models import NetworkSearchQuery
from indra_network_search.pathfinding import shared_parents
from indra_network_search.util.curation_cache import CurationCache
from indra_network_search.rest_util import is_weighted

__all__ = ["QueryHandler"]


class QueryHandler:
    """Maps queries from the REST API to a method of the IndraNetworkSearchAPI

    The QueryHandler's job is to act as a middle layer between the methods
    of the IndraNetworkSearchAPI and the REST API. It figures out which
    queries are eligible from the input query.
    """

    def __init__(
        self,
        rest_query: NetworkSearchQuery,
        curation_cache: CurationCache = CurationCache(),
    ):
        self.rest_query: NetworkSearchQuery = rest_query
        self.rest_query_hash: int = rest_query.get_hash()
        self.signed: bool = SIGN_TO_STANDARD.get(rest_query.sign) in ("+", "-")
        self.open: bool = bool(rest_query.source) ^ bool(rest_query.target)
        self.weighted: bool = rest_query.is_overall_weighted()
        self.mesh: List[str] = rest_query.mesh_ids
        self.strict_mesh: bool = rest_query.strict_mesh_id_filtering
        self._query_dict: Dict[str, UIQuery] = {}
        cc = curation_cache
        self._hash_bl: Set[int] = (
            cc.get_all_hashes() if rest_query.filter_curated else set()
        )

    def _get_queries(self) -> Dict[str, UIQuery]:
        """This method maps the rest_query to different eligible queries"""
        query_dict: Dict[str, UIQuery] = {}
        # If not open: Add shortest_simple_paths and add other queries
        if not self.open:
            query_dict["path_query"] = ShortestSimplePathsQuery(
                self.rest_query, hash_blacklist=self._hash_bl
            )
            query_dict.update(self._aux_queries())
            if self.rest_query.two_way:
                query_dict["reverse_path_query"] = ShortestSimplePathsQuery(
                    self.rest_query.reverse_search(), hash_blacklist=self._hash_bl
                )
        # If open: check if weighted options
        else:
            if is_weighted(
                weighted=self.weighted,
                mesh_ids=self.mesh,
                strict_mesh_filtering=self.strict_mesh,
            ):
                query_dict["path_query"] = DijkstraQuery(
                    self.rest_query, hash_blacklist=self._hash_bl
                )
                if self.rest_query.two_way:
                    query_dict["reverse_path_query"] = DijkstraQuery(
                        self.rest_query.reverse_search(), hash_blacklist=self._hash_bl
                    )

            else:
                query_dict["path_query"] = BreadthFirstSearchQuery(
                    self.rest_query, hash_blacklist=self._hash_bl
                )
            if self.rest_query.two_way:
                query_dict["reverse_path_query"] = BreadthFirstSearchQuery(
                    self.rest_query.reverse_search(), hash_blacklist=self._hash_bl
                )

        return query_dict

    def _aux_queries(
        self,
    ) -> Dict[str, Union[SharedRegulatorsQuery, SharedTargetsQuery, OntologyQuery]]:
        """Get shared interactors and ontological query"""
        aux_queries = {
            "shared_targets": SharedTargetsQuery(self.rest_query, self._hash_bl),
            shared_parents.__name__: OntologyQuery(self.rest_query),
        }
        if self.rest_query.shared_regulators:
            aux_queries["shared_regulators"] = SharedRegulatorsQuery(
                self.rest_query, self._hash_bl
            )

        return aux_queries

    def get_queries(self) -> Dict[str, UIQuery]:
        """Returns a dict of all eligible queries

        Returns
        -------
        :
            A dict containing the instances of the eligible Query classes
            as {query name: Query instance}
        """
        if not self._query_dict:
            self._query_dict = self._get_queries()
        return self._query_dict
