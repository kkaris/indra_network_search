const DEPTH_LIMIT = 2;
const K_SHORTEST =50;
const MAX_PER_NODE = 5;
const CONST_C = 1;
const CONST_TK = 10;
const USER_TIMEOUT = 30;
const WEIGHTED = "unweighted";
const EMPTY_RESULTS = {
    // Follows indra_network_search.data_models::Results
    query_hash: "",
    time_limit: 30.0,
    timed_out: false,
    hashes: [],
    path_results: {},
    reverse_path_results: {},
    ontology_results: {},
    shared_target_results: {},
    shared_regulators_results: {},
}

export default {
    DEPTH_LIMIT,
    K_SHORTEST,
    MAX_PER_NODE,
    CONST_C,
    CONST_TK,
    USER_TIMEOUT,
    WEIGHTED,
    EMPTY_RESULTS,
}
