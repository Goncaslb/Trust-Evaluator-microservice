from typing import NamedTuple
from enum import IntEnum

from models.did import DID


class Coordinates(NamedTuple):
    lat: float
    lon: float


class Entities(IntEnum):
    """
    Used for index of AttributeWeights. 
    """
    RESOURCE_PROVIDER = 0
    RESOURCE_CAPACITY = 1
    APPLICATION_PROVIDER = 2


def verify_did(did: DID):
    if did.raw.startswith("did:"):
        return True
    else:
        print(f"Warning: {did} is not a valid DID")
        return False

def validate_location(location: Coordinates):    
    """
    Validates if the given coordinates are within Slovenian territory.

    Args:
        location (tuple): A tuple containing latitude and longitude (lat, lon).

    Returns:
        bool: True if the location is within Slovenia, False otherwise.
    """
    lat, lon = location

    min_lat, max_lat = 45.42, 46.88 
    min_lon, max_lon = 13.38, 16.60

    # Check if the coordinates are within the boundaries
    if min_lat <= lat <= max_lat:
        if min_lon <= lon <= max_lon:
            return True

    return False