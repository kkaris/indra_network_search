from indra_network_search.query import _get_edge_filter_func
from indra_network_search.tests.util import _get_edge_hash, _get_graph

from indra_network_search.tests import hash_bl_edge1, hash_bl_edge2


def test_allowed_edges():
    large = False
    signed = False
    graph = _get_graph(large=large, signed=signed)
    hash_set1 = _get_edge_hash(
        edge=hash_bl_edge1, graph=graph, large=large, signed=signed
    )
    hash_set2 = _get_edge_hash(
        edge=hash_bl_edge2, graph=graph, large=large, signed=signed
    )
    hash_blacklist = list(hash_set1.union(hash_set2))
    _get_edge_hash(edge=hash_bl_edge1, graph=graph, large=large, signed=signed)
    edge_filter_func = _get_edge_filter_func(hash_blacklist=hash_blacklist)
    allowed_edges = [e for e in graph.edges if e not in (hash_bl_edge1, hash_bl_edge2)]
    disallowed_edges = [hash_bl_edge1, hash_bl_edge2]

    for edge in allowed_edges:
        assert edge_filter_func(graph, *edge)

    for edge in disallowed_edges:
        assert not edge_filter_func(graph, *edge)
