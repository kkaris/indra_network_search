from itertools import zip_longest
from indra.explanation.pathfinding import bfs_search
from indra_network_search.data_models import Node, NetworkSearchQuery
from indra_network_search.query import _get_edge_filter_func, BreadthFirstSearchQuery
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
    edge_filter_func = _get_edge_filter_func(hash_blacklist=hash_blacklist)
    allowed_edges = [e for e in graph.edges if e not in (hash_bl_edge1, hash_bl_edge2)]
    disallowed_edges = [hash_bl_edge1, hash_bl_edge2]

    for edge in allowed_edges:
        assert edge_filter_func(graph, *edge)

    for edge in disallowed_edges:
        assert not edge_filter_func(graph, *edge)


def test_bfs_search_w_blacklist():
    large = False
    signed = False
    graph = _get_graph(large=large, signed=signed)
    brca1 = Node(name="BRCA1", namespace="HGNC", identifier="1100")
    hash_set1 = _get_edge_hash(
        edge=hash_bl_edge1, graph=graph, large=large, signed=signed
    )
    hash_set2 = _get_edge_hash(
        edge=hash_bl_edge2, graph=graph, large=large, signed=signed
    )
    hash_blacklist = list(hash_set1.union(hash_set2))
    edge_filter_func = _get_edge_filter_func(hash_blacklist=hash_blacklist)
    hash_bl_query = NetworkSearchQuery(source=brca1.name, filter_curated=True)
    str_paths2 = [("BRCA1", n) for n in ["testosterone", "NR2C2", "MBD2", "PATZ1"]]
    str_paths3 = [("BRCA1", "testosterone", "CHEK1")]
    combined_paths = str_paths2 + str_paths3

    bfsq = BreadthFirstSearchQuery(
        query=hash_bl_query, hash_blacklist=set(hash_blacklist)
    )
    bfs_gen_manual = bfs_search(
        g=graph, source_node=brca1.name, edge_filter=edge_filter_func
    )
    for p in bfs_gen_manual:
        assert "AR" not in p

    run_options = bfsq.run_options(graph=graph)
    bfs_gen_manual = bfs_search(
        g=graph, source_node=brca1.name, edge_filter=edge_filter_func
    )
    bfs_gen_query = bfs_search(g=graph, **run_options)

    for p1, p2, pe in zip_longest(bfs_gen_manual, bfs_gen_query,
                                  combined_paths, fillvalue=None):
        assert all(n1 is not None for n1 in p1)
        assert all(n2 is not None for n2 in p2)
        assert all((n1 == n2 and n2 == ne) for n1, n2, ne in zip(p1, p2, pe))
