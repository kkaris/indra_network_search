from indra_network_search.data_models import StmtData


def test_stmt_data():
    stmt_dict = {
        "stmt_type": "fplx",
        "evidence_count": 1,
        "source_counts": {"fplx": 1},
        "stmt_hash": "https://identifiers.org/fplx:FANC",
        "belief": 1.0,
        "weight": 1e-15,
        "curated": True,
        "english": "FPLX:FANC is an ontological parent of HGNC:1100",
        "corr_weight": 1,
    }
    stmt_data = StmtData(db_url_hash=stmt_dict["stmt_hash"], **stmt_dict)
    assert stmt_data.source_counts == {"fplx": 1}
