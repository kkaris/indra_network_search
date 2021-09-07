"""
Contains return models from the rest api
"""
from pydantic import BaseModel
from typing import List, Optional

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

__all__ = ["Health", "ServerStatus"]


STR_STATUS = Literal["booting", "available"]


class Health(BaseModel):
    """Health status"""

    status: STR_STATUS


class ServerStatus(BaseModel):
    """Status with more detail than health"""

    graphs_available: Optional[List[Literal["signed", "unsigned"]]] = None
    unsigned_nodes: Optional[int] = None
    signed_nodes: Optional[int] = None
    unsigned_edges: Optional[int] = None
    signed_edges: Optional[int] = None
    status: STR_STATUS
