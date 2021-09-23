=====================
Network Search Web UI
=====================
This document introduces the web interface of the INDRA Network Search Service

.. figure:: ../_static/images/indra_network_search_screenshot.png
  :align: center
  :figwidth: 100 %

  *The network search interface with no input or results.*

Source and Target
-----------------
The source and target are the nodes between which to find a path and at least
one of source and target is needed to do a search. If only one of source or
target is provided, an open ended breadth first search is done instead of a
path search. Note that the source and target are not affected by the choice of
*allowed namespaces* (see below) <-- provide internal link.

Autocompleting source/target inputs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Autocompletion of source/target based on prefix and entity identifier are
made automatically as an input is typed or pasted into the text boxes. The
suggestions are picked from the nodes in the graph and the text box will
mark the entered text as correct if it matches an existing node in the graph.
ADD IMAGE WITH CORRECT NODE AND SUGGESTIONS


Detailed Search Options - General Options
-----------------------------------------

Path Length
~~~~~~~~~~~
Only paths of this many edges will be returned. Must be a positive integer.

Node Blacklist
~~~~~~~~~~~~~~
Node names entered here are skipped in the path search. This is a good way
to avoid nodes of extremely high degree that overwhelms the results and
effectively blocks out results that include nodes of lower degree. *See also
Cull Highest Degree Node below.* <-- provide internal link

Max Paths
~~~~~~~~~
The maximum number of results to return per category in the results. The
default and the maximum allowed is 50 results. For unweighted searches this
number rarely makes a perceivable difference in response time but for
weighted searches keep this number low for a faster response time.

Signed Search
~~~~~~~~~~~~~
To perform a signed search, click on the drop down menu that says "No sign"
and chose a sign. "+" means that the returned paths are upregulations,
and "-" means that the returned paths are downregulations. For the
purpose of signed search, only statements that imply a clear up- or
downregulation are considered. Currently this mean `IncreaseAmount` and
`Activation` for upregulation, and `DecreaseAmount` and `Inhibition` for
downregulation.

Highest Degree Node Culling Frequency
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Entering a positive integer here allows the path search to include the highest
degree node for the first N returned paths, after which that node is added to
the *Node Blacklist*. <-- internal link This is repeated for the second highest degree node for
the following N paths, then for the third highest degree node and so forth.
*Limitations:* This option is only applied to unweighted open search and
source-target searches.

Belief Cutoff
~~~~~~~~~~~~~
Any statement with a belief score below this number will be excluded from the
edge support. If all statements are excluded from the edge, all paths
containing that edge become invalid and are skipped. It is set to zero by
default to include all edges. Read more about belief scores in the `belief
module <https://indra.readthedocs.io/en/latest/modules/belief/index.html>`_ of
INDRA.

Allowed Statement Types
~~~~~~~~~~~~~~~~~~~~~~~
This is a multiselect dropdown which contains multiple statement types to
allow in the results. If an edge of a path does not contain any of the
selected statement types, the whole path will be skipped from the result.
Read more about statement types in the
`statements module <https://indra.readthedocs.io/en/latest/modules/statements.html>`_
of INDRA.

Allowed Node Namespaces
~~~~~~~~~~~~~~~~~~~~~~~
The namespaces included here are the ones that are allowed on any node
visited in the path search. The namespace of the source and target are
excluded from this restriction. A namespace in INDRA is the prefix or name of
the *type* of identifier used to uniquely identify an entity from a specific
knowledge source. For example, a chemical can be identified using a `CHEBI`
identifier and would then be identified in the `CHEBI` namespace.

Checkboxes
~~~~~~~~~~
The following options are available as checkboxes:

- **Only Database Supported Sources**: Check this box to enforce that all
  edges must be supported by at least one statement sourced from curated
  databases like PathwayCommons and Signor
- **Allow Ontological Edges**: Check this box to allow directed edges that go
  from an entity to its ontological parent, e.g. from the NFKB1 sub-unit to
  the NFkappaB complex.
- **Include Reverse Search**: Check this box to also search for paths with
  source and target swapped. With this option, the reverse search *from*
  target *to* source is done as well as the original search from source to
  target. If the timeout is reached (see below) before the reverse search can
  start, the reverse search will not return any paths. If the timeout is
  reached during the reverse search, fewer paths than for the original search
  will be returned.
- **Include Search for Shared Regulators of Source/Target**: Check this box
  to include a search for common upstream nodes one edge away from both
  source and target. This option is only available when both source and
  target specified.

Detailed Search Options - Context and Weighted Search Options
-------------------------------------------------------------
This section of the search options allows control over how to prioritize or
*weight* edges in paths differently. During weighted search, the cost along
every path encountered is calculated as the sum of the edge weights along the
path. The paths are returned in ascending order of cost.

The different ways of weighting the search are available in the dropdown menu
"Weighted Search". *Note:* A weighted search is costly and usually takes
longer than an unweighted search. It is common that a very heavy weighted
search times out, especially for a *signed weighted* search, even with the
highest allowed timeout of 120 seconds.

The weighted search uses a slightly modified version of the Djikstra weighted
search employed in Networkx.

The code implemented for the weighted search is available on `github
<https://github.com/sorgerlab/indra/blob/master/indra/explanation/pathfinding/pathfinding.py>`_
in the functions `shortest_simple_paths()` and `open_dijkstra_search()` for
closed and open paths, respectively.

Open Search Options
~~~~~~~~~~~~~~~~~~~
Options under the Open Search Options are only applied during open ended
searches. In order to perform an open ended search, only a source or a
target must be given.

- **Terminal Namespaces:** Namespaces selected here restrict the search to
  only return paths that end (open search from source) or start (open
  search from target) on the given namespaces.
- **Max per node:** The integer provided here gives a maximum for the number
  of children to continue to open search from. This option is only applied
  during *unweighted* searches.

Context Options
~~~~~~~~~~~~~~~
The context based search allows a search to prioritize or only include
connections that are relevant to the provided context. The context is
given as MeSH terms.

- **MeSH IDs:** Enter a comma separated list of MeSH IDs that should be
  prioritized in the search.
- **Strict Filtering on MeSH IDs:** Tick this box to *only* allow edges with
  associated with the provided MeSH IDs. If left unticked, the search is
  weighted.
- **Constants** :math:`C` **and** :math:`T_k`: These two constant allow for
  changing the importance of the context in a weighted context based search.
  For any edge :math:`e`, the weight :math:`w_e` for context based search is
  calculated in the following way:

.. math::
    w_e = -C \cdot \log\left(\frac{\text{refcount}}{\text{total} + T_k}\right)

Here, `refcount` is the number of references with the associated MeSH
ID(s) that are supporting edge :math:`e` and `total` is the total number of
references supporting edge :math:`e`.


Include Reverse Search
~~~~~~~~~~~~~~~~~~~~~~
With this option, the reverse search *from* target *to* source is done as
well as the original search from source to target. If the timeout is reached
(see below) before the reverse seach can start, the reverse search will
not return any paths. If the timeout is reached during the reverse search,
fewer paths than for the original search will be retured.

Weighted Search
~~~~~~~~~~~~~~~
When performing a weighted search, the cost along every path encountered is
calculated as the sum of the weights along the path. The paths are then
returned in ascending order of cost. The weighted search uses a slightly
modified version of the Djikstra weighted search employed in Networkx.
*Note:* A weighted search is costly and usually takes longer than
a normal search. It is common that a very heavy weighted search times out,
especially for a *signed* weighted search.

The code implemented for the weighted search is available on `github
<https://github.com/sorgerlab/indra/blob/master/indra/explanation/pathfinding/pathfinding.py>`_
in the function `shortest_simple_paths()`.

Databases Only
~~~~~~~~~~~~~~
With this option, only statements that contain sources from curated
databases like PathwayCommons and Signor are allowed to support edges in the
returned paths.

Include Famplex Families and Complexes in Path Search
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This option allows for edges to be between a gene and its family or
betewen a gene and a complex formed by its encoded protein. For example: an
edge between `BRCA1` and its family `BRCA` would be allowed.

Expand search to FamPlex
~~~~~~~~~~~~~~~~~~~~~~~~
If a path search returns empty, this option will allow the path search to be
retried with parents if the source and/or target entities. For example, if a
search with `BRCA1` as source returns empty, the search would be retried
with the `BRCA` family as source instead.

Timeout
~~~~~~~
Setting a timeout allows to set a larger (or smaller) timeout than the
default 30 seconds timeout. The time since the path search was started is
checked after each path has been checked during the search. If the time
passed is larger than the allowed timeout, the search is interrupted and
returns as fast as possible. The timeout provided has to be a decimal number
smaller than or equal to 120 seconds.

Result Categories
-----------------
If there are no results for the specific section, that section's card won't
show up. By default, the result cards are collapsed and only the card header
is shown with a summary count of the number of results. To expand the card
body, click on the card header.

Complexes and Families
~~~~~~~~~~~~~~~~~~~~~~
This card shows the results of a search for common complexes and families
between source and target. For example with `BRCA1` and `BRCA2` as source
and target, respectively, the BRCA family would show up alongside the FANC
family.

.. figure:: ../_static/images/famplex_search.png
  :align: center
  :figwidth: 100 %

  *The result of a search with `BRCA1` and `BRCA2` as source and target,
  respectively for Complexes and Families.*


Common Targets
~~~~~~~~~~~~~~
This card shows the direct downstream targets that are common to both the
chosen `source` and `target`.

Shared Regulators
~~~~~~~~~~~~~~~~~
Shared regulators are only searched for if the corresponding tick-box is
checked. The results shown are the direct upstream regulators that are
common to both `source` and `target`.

N Edge Paths
~~~~~~~~~~~~
These card are shown per path length so that all paths with one edge are
assembled under one card, all paths with two edges in another card and so
forth.

Detailed Results
----------------
For each result card, the edges displayed link out to an INDRA DataBase query
in order to further inspect the results. As the network search results are
filtered in more detail than what is possible using the INDRA DataBase web
interface, the statements shown can sometimes be slightly different than the
edge data returned by the network search result.

Download Results
----------------
You can download the search result json and the statement jsons from the *path
search* by clicking the link provided after the search has resolved.

The Graphs Used
---------------
The two graphs used for the network search are assembled from a full
snapshot of the `INDRA DataBase <https://github.com/indralab/indra_db>`_ that
is updated regularly. Any statement that includes two or three agents are
assembled into the support for the edges for the graphs, with one edge
containing one or more statements. The two types of graphs used are:

1. Unsigned directed graph
2. Signed node directed graph

The edges in the signed graph only contain statements that have clear
up- or downreguations associated with them, which currently are
`IncreaseAmount` and `Activation` for upregulation, and `DecreaseAmount` and
`Inhibition` for downregulation.

The code assembling the graphs can be found in `net_functions.py
<https://github.com/indralab/depmap_analysis/blob/master/depmap_analysis
/network_functions/net_functions.py>`_ in the function
`sif_dump_df_to_digraph()`.
