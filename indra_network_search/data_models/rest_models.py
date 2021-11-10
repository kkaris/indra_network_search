"""
Contains return models from the rest api
"""
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

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

    unsigned_nodes: Optional[int] = Field(None, description="Number of " "unsigned nodes " "in the graph")
    signed_nodes: Optional[int] = Field(None, description="Number of signed " "nodes in the graph")
    unsigned_edges: Optional[int] = Field(None, description="Number of " "unsigned edges " "in the graph")
    signed_edges: Optional[int] = Field(None, description="Number of signed " "edges in the graph")
    graph_date: Optional[date] = Field(None, description="Date of the " "graph creation from the database")
    status: STR_STATUS = Field(..., description="Status of the server")
