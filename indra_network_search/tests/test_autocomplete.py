import pandas as pd
from depmap_analysis.network_functions.net_functions import sif_dump_df_to_digraph
from indra_network_search.autocomplete import NodesTrie


def _get_dg():
    dfd = dict(
        agA_ns=["HGNC", "HGNC"],
        agA_id=["1100", "1101"],
        agA_name=["BRCA1", "Brca2"],
        agB_ns=["HGNC", "HGNC"],
        agB_id=["3467", "11998"],
        agB_name=["ESR1", "TP53"],
        stmt_type=["Complex", "Complex"],
        evidence_count=[13, 10],
        stmt_hash=["1234567890", "-9876543210"],
        residue=[None, None],
        position=[None, None],
        source_counts=[{"reach": 13}, {"sparser": 10}],
        belief=[0.8, 0.6],
    )
    sif = pd.DataFrame(dfd)
    dg = sif_dump_df_to_digraph(
        df=sif,
        date="2021-08-15",
        include_entity_hierarchies=False,
        graph_type="digraph",
    )
    return dg


def test_name_matching():
    dg = _get_dg()
    trie = NodesTrie.from_node_names(graph=dg)
    res = trie.case_items(prefix="brca")
    assert {("BRCA1", "HGNC", "1100"), ("Brca2", "HGNC", "1101")} == set(res)
    no_res = trie.case_items(prefix="not in graph")
    assert no_res == []


def test_nsid_matching():
    dg = _get_dg()
    trie = NodesTrie.from_node_ns_id(graph=dg)
    res = trie.case_items(prefix="HGNC:")
    assert {
        ("BRCA1", "HGNC", "1100"),
        ("Brca2", "HGNC", "1101"),
        ("ESR1", "HGNC", "3467"),
        ("TP53", "HGNC", "11998"),
    } == set(res)
    no_res = trie.case_items(prefix="UP:")
    assert no_res == []
