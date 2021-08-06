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
            graph as keys and the corresponding (ns, id) tuple as values
        """
        node = list(itertools.islice(graph.nodes, 1))[0]
        if isinstance(node, str):
            return cls(
                **{n: (graph.nodes[n]["ns"], graph.nodes[n]["id"])
                   for n in graph.nodes}
            )
        else:
            raise ValueError(
                "Graph nodes are not str, cannot create NodesTrie instance"
            )

    def case_keys(self, prefix: Optional[str] = None, case_sensitive: bool = True):
        """Case insensitive wrapper around NodeTrie.keys()

        Parameters
        ----------
        prefix :
            The prefix to search
        case_sensitive :
            If False, search for both prefix, prefix.upper() and
            prefix.lower(). Default: True, i.e. NodesTrie.keys() is called.

        Returns
        -------
        List[str]
            Return a list of this trie's keys
        """
        if case_sensitive:
            return self.keys(prefix)
        else:
            # Do both upper and lower
            lower_prefix = prefix.lower()
            upper_prefix = prefix.upper()
            lower_keys = self.keys(lower_prefix)
            keys = self.keys(prefix)
            upper_keys = self.keys(upper_prefix)
            merged = lower_keys + keys + upper_keys
            return sorted(merged)

    def case_items(self, prefix: Optional[str] = None, case_sensitive: bool = False):
        """Case insensitive wrapper around NodeTrie.items()

        Parameters
        ----------
        prefix :
            The prefix to search
        case_sensitive :
            If False, search for both prefix, prefix.upper() and
            prefix.lower(), otherwise route call to NodeTrie.items().
            Default: False

        Returns
        -------
        List[Tuple[str, Tuple[str, str]]]
            Return a list of key, value tuples, where the values are
            themselves (namespace, id) tuples
        """
        if case_sensitive:
            return self.items(prefix)
        else:
            # Do both upper and lower
            lower_prefix = prefix.lower()
            upper_prefix = prefix.upper()
            lower_keys = self.items(lower_prefix)
            keys = self.items(prefix)
            upper_keys = self.items(upper_prefix)
            merged = lower_keys + keys + upper_keys
            return sorted(merged)
