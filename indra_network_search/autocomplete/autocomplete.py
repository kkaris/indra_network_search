"""
An API wrapping SortedStringTrie from pytrie (see
https://github.com/gsakkis/pytrie)
"""
import itertools
from typing import Union, List, Optional
from networkx import DiGraph, MultiDiGraph
from pytrie import SortedStringTrie


DirGraph = Union[DiGraph, MultiDiGraph]

__all__ = ["NodesTrie"]


class NodesTrie(SortedStringTrie):
    @classmethod
    def from_graph_nodes(cls, graph: DirGraph) -> "NodesTrie":
        """Produce a NodesTrie instance from a graph with str node names

        Parameters
        ----------
        graph:
            Graph from which nodes should be searchable. It is assumed the
            nodes are all keyed by strings

        Returns
        -------
        :
            An instance of a NodesTrie containing the node names of the
            graph as keys and the corresponding (name, ns, id) tuple as values
        """
        node = list(itertools.islice(graph.nodes, 1))[0]
        if isinstance(node, str):
            return cls(
                **{n.lower(): (n, graph.nodes[n]["ns"], graph.nodes[n]["id"])
                   for n in graph.nodes}
            )
        else:
            raise ValueError(
                "Graph nodes are not str, cannot create NodesTrie instance"
            )

    def case_keys(self, prefix: Optional[str] = None):
        """Case insensitive wrapper around NodeTrie.keys()

        Parameters
        ----------
        prefix :
            The prefix to search

        Returns
        -------
        List[str]
            Return a list of this trie's keys
        """
        return [w for _, (w, _, _) in self.items(prefix.lower())]

    def case_items(self, prefix: Optional[str] = None):
        """Case insensitive wrapper around NodeTrie.items()

        Parameters
        ----------
        prefix :
            The prefix to search

        Returns
        -------
        List[Tuple[str, Tuple[str, str]]]
            Return a list of key, value tuples, where the values are
            themselves (namespace, id) tuples
        """
        return [t for _, t in self.items(prefix.lower())]
