"""
Contains return models from the rest api
"""
from pydantic import BaseModel

try:
    from typing import Literal, List
except ImportError:
    from typing_extensions import Literal

__all__ = ["Health"]


class Health(BaseModel):
    """Health status"""

    status: Literal["booting", "available"]


class ServerStatus(BaseModel):
    """Status with more detail than health"""

    graphs_available: List[Literal["signed", "unsigned"]]
    unsigned_nodes: int
    signed_nodes: int
    unsigned_edges: int
    signed_edges: int
    unique_entitity_count: int
