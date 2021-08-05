"""
An API wrapping SortedStringTrie from pytrie, see
https://github.com/gsakkis/pytrie, to provide some methods relevant for an
implementation
"""
import itertools
from typing import Union
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
