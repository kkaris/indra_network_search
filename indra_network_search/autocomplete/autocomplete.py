"""
An API wrapping SortedStringTrie from pytrie, see
https://github.com/gsakkis/pytrie, to provide some methods relevant for an
implementation
"""
import itertools
from typing import Union, List
from networkx import DiGraph, MultiDiGraph
from pytrie import SortedStringTrie


DirGraph = Union[DiGraph, MultiDiGraph]

__all__ = ['NodesTrie']


class NodesTrie(SortedStringTrie):

    @classmethod
    def from_graph_nodes(cls, graph: DirGraph) -> 'NodesTrie':
        """

        Parameters
        ----------
        graph:
            Graph from which nodes should be searchable. It is assumed the

        Returns
        -------
        :
            An instance of an NodesTrie containing the node names of the graph
        """
        node = list(itertools.islice( graph.nodes, 1))[0]
        if isinstance(node, str):
            return cls(**{n: ix for ix, n in enumerate(graph.nodes)})
        else:
            raise ValueError('Graph nodes are not str, cannot create '
                             'SortedStringTrie instance')

    def case_keys(self, prefix: str, case_sensitive: bool = True):
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
            The list of matched keys that
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
