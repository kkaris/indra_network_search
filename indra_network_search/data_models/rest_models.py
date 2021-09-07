"""
Contains return models from the rest api
"""
from pydantic import BaseModel
from typing import Optional
from datetime import date

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

    unsigned_nodes: Optional[int] = None
    signed_nodes: Optional[int] = None
    unsigned_edges: Optional[int] = None
    signed_edges: Optional[int] = None
    graph_date: Optional[date] = None
    status: STR_STATUS
