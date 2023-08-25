import typing

from ..db import database
from ..embed import embed
from .. import entities


class ResourceManager:
    """Manages the resources."""

    def __init__(self, **kwargs):
        pass
    
    def run(self) -> typing.Generator[entities.Document, None, None]:
        """Runs the resource manager.
        
        Generates documents(without embedding) from the resource.
        """
        pass
    