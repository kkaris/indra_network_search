"""
An API wrapping SortedStringTrie from pytrie (see
https://github.com/gsakkis/pytrie)
"""
import itertools
from typing import Union, List, Optional, Tuple
from networkx import DiGraph, MultiDiGraph
from pytrie import SortedStringTrie


# Derived types
Prefixes = List[Tuple[str, str, str]]
DirGraph = Union[DiGraph, MultiDiGraph]

__all__ = ["NodesTrie", "Prefixes"]


class NodesTrie(SortedStringTrie):
    @classmethod
    def from_node_names(cls, graph: DirGraph) -> "NodesTrie":
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
        _is_str_nodes(graph)
        name_indexing = {}
        for node in graph.nodes:
            # Get node name in lowercase
            node_name = node.lower()
            if node_name in name_indexing:
                ix = 1
                node_name = node_name + f"_{ix}"
                # Increase index until no key is not present
                while node_name in name_indexing:
                    ix += 1
                    node_name = node.lower() + f"_{ix}"
            name_indexing[node_name] = (
                node,
                graph.nodes[node]["ns"],
                graph.nodes[node]["id"],
            )

        return cls(**name_indexing)

    @classmethod
    def from_node_ns_id(cls, graph: DirGraph) -> "NodesTrie":
        _is_str_nodes(graph)
        return cls(
            **{
                f'{graph.nodes[n]["ns"]}:{graph.nodes[n]["id"]}'.lower(): (
                    n,
                    graph.nodes[n]["ns"],
                    graph.nodes[n]["id"],
                )
                for n in graph.nodes
            }
        )

    def case_keys(self, prefix: Optional[str] = None) -> List[str]:
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

    def case_items(self, prefix: Optional[str] = None) -> Prefixes:
        """Case insensitive wrapper around NodeTrie.items()

        Parameters
        ----------
        prefix :
            The prefix to search

        Returns
        -------
        :
            Return a list of (name, namespace, id) tuples
        """
        return [t for _, t in self.items(prefix.lower())]


def _is_str_nodes(g: DirGraph):
    node = list(itertools.islice(g.nodes, 1))[0]
    if not isinstance(node, str):
        raise ValueError("Graph nodes are not str, cannot create NodesTrie instance")
