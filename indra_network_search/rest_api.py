"""
The IndraNetworkSearch REST API
"""
import logging
from os import environ
from typing import List

from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse

from indra.databases import get_identifiers_url
from .data_models.rest_models import Health
from .util import load_indra_graph
from .data_models import Results, NetworkSearchQuery, SubgraphRestQuery, \
    SubgraphResults
from .autocomplete import NodesTrie, Prefixes
from .search_api import IndraNetworkSearchAPI
from depmap_analysis.network_functions.net_functions import bio_ontology


app = FastAPI()

logger = logging.getLogger(__name__)

DEBUG = environ.get('API_DEBUG') == "1"
USE_CACHE = environ.get('USE_CACHE') == "1"
HEALTH = Health(status='booting')


@app.get('/')
async def root_redirect():
    """Redirect to docs

    This is a temporary solution until the Vue frontend is in place
    """
    return RedirectResponse(app.root_path + '/redoc')


@app.get('/xrefs', response_model=List[List[str]])
def get_xrefs(ns: str, id: str) -> List[List[str]]:
    """Get all cross-refs given a namespace and ID

    Parameters
    ----------
    ns :
        The namespace of the entity to find cross-refs for
    id :
        The identifier of the entity to find cross-regs for

    Returns
    -------
    :
        A list of tuples containing namespace, identifier, lookup url to
        identifiers.org
    """
    # Todo: offload util features and capabilities, such as this one, to a new
    #  UtilApi class
    xrefs = bio_ontology.get_mappings(ns=ns, id=id)
    xrefs_w_lookup = [[n, i, get_identifiers_url(n, i)]
                      for n, i in xrefs]
    return xrefs_w_lookup


@app.get('/nodes_in_graph', response_model=Prefixes)
def get_nodes(prefix: str = Query(..., min_length=1)) -> Prefixes:
    """Get the case-insensitive node names with (ns, id) starting in prefix

    Parameters
    ----------
    prefix :
        The prefix of a node name to check

    Returns
    -------
    :
        A list of tuples of (node name, namespace, identifier)
    """
    # Catch very short entity names
    if 1 <= len(prefix) <= 2 and ':' not in prefix:
        logger.info('Got short node name lookup')
        # Loop all combinations of upper and lowercase
        if len(prefix) == 1:
            nodes = []
            upper_match = network_search_api.get_node(prefix.upper())
            lower_match = network_search_api.get_node(prefix.lower())
            if upper_match:
                nodes.append(
                    [upper_match.name, upper_match.namespace, upper_match.identifier]
                )
            if lower_match:
                nodes.append(
                    [lower_match.name, lower_match.namespace, lower_match.identifier]
                )
        else:
            nodes = []
            n1 = prefix.upper()
            n2 = prefix[0].lower() + prefix.upper()[1]
            n3 = prefix[0].upper() + prefix.lower()[1]
            n4 = prefix.lower()
            for p in [n1, n2, n3, n4]:
                m = network_search_api.get_node(p)
                if m:
                    nodes.append(
                        [m.name, m.namespace, m.identifier]
                    )
    # Look up ns:id searches
    elif ':' in prefix:
        logger.info('Got ns:id prefix check')
        nodes = nsid_trie.case_items(prefix=prefix)
    else:
        logger.info('Got name prefix check')
        nodes = nodes_trie.case_items(prefix=prefix)
    logger.info(f'Prefix query resolved with {len(nodes)} suggestions')
    return nodes


@app.get('/health', response_model=Health)
async def health():
    """Returns health status

    Returns
    -------
    Health
    """
    logger.info('Got health check')
    return HEALTH


@app.post('/query', response_model=Results)
def query(search_query: NetworkSearchQuery):
    """Interface with IndraNetworkSearchAPI.handle_query

    Parameters
    ----------
    search_query : NetworkSearchQuery
        Query to the NetworkSearchQuery

    Returns
    -------
    Results
    """
    logger.info(f'Got NetworkSearchQuery: {search_query.dict()}')
    results = network_search_api.handle_query(rest_query=search_query)
    return results


@app.post('/subgraph', response_model=SubgraphResults)
def sub_graph(search_query: SubgraphRestQuery):
    """Interface with IndraNetworkSearchAPI.handle_subgraph_query

    Parameters
    ----------
    search_query: SubgraphRestQuery
        Query to for IndraNetworkSearchAPI.handle_subgraph_query

    Returns
    -------
    SubgraphResults
    """
    logger.info(f'Got subgraph query with {len(search_query.nodes)} nodes')
    subgraph_results = network_search_api.handle_subgraph_query(
        subgraph_rest_query=search_query)
    logger.info('Subgraph query resolved')
    return subgraph_results


if DEBUG:
    from .tests.util import _setup_graph, _setup_signed_node_graph
    dir_graph = _setup_graph()
    sign_node_graph = _setup_signed_node_graph(False)
else:
    dir_graph, _, sign_node_graph, _ = \
        load_indra_graph(unsigned_graph=True, unsigned_multi_graph=False,
                         sign_node_graph=True, sign_edge_graph=False,
                         use_cache=USE_CACHE)

    bio_ontology.initialize()

# Get a Trie for autocomplete
logger.info('Loading Trie structure with unsigned graph nodes')
nodes_trie = NodesTrie.from_node_names(graph=dir_graph)
nsid_trie = NodesTrie.from_node_ns_id(graph=dir_graph)

# Setup search API
logger.info('Setting up IndraNetworkSearchAPI with signed and unsigned '
            'graphs')
network_search_api = IndraNetworkSearchAPI(
    unsigned_graph=dir_graph, signed_node_graph=sign_node_graph
)
logger.info('Service is available')
HEALTH.status = 'available'
