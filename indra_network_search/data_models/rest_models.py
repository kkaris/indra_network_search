"""
Contains return models from the rest api
"""
from pydantic import BaseModel

__all__ = ['Health']


class Health(BaseModel):
    """Health status"""
    status: str
