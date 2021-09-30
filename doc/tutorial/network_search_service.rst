Running the Service Locally
===========================

To run the service locally, two things are needed:

1. Fetch the latest update to the branch
   `'main' <https://github.com/indralab/indra_network_service/tree/main>`_
   of the indra_network_service repository from one of the maintainers.
2. Download the latest network representations of the indra network
   (might require AWS S3 login):

   * ``indranet_dir_graph_latest.pkl``
   * ``indranet_sign_edge_graph_latest.pkl`` (optional)
   * ``indranet_sign_node_graph_latest.pkl`` (optional)

   The signed representations of the graph are only needed for signed path
   search.

Dependecies are Python 3.6+, but otherwise the same as for INDRA and
INDRA_DB. Run ``service_api/api.py`` from the root of the repository with the
following arguments::

  python -m service_api.api [-h] [--host HOST] [--port PORT]
  [--cache DG_GRAPH MDG_GRAPH|None SIGN_EDGE_GRAPH|None SIGN_NODE_GRAPH|None]

where ``HOST`` is the address to use (default is ``127.0.0.1``), ``PORT``
is the port to use (default is ``5000``) and ``DG_GRAPH``, ``MDG_GRAPH``,
``SIGN_EDGE_GRAPH`` and ``SING_NODE_GRAPH`` are pickled graphs representing
the INDRA knowledge network in DiGraph, MultiDiGraph and SignedGraph
representations, respectively. The ``--cache`` flag overrides the defaults
in the file so that any file can be provided. If default settings are used
for ``HOST`` and ``PORT``, a web ui is hosted on http://localhost:5000/query
and query submissions are done to http://localhost:5000/query/submit.
