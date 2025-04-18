from typing import NamedTuple, Optional
from enum import IntEnum, StrEnum
import requests
from pathlib import Path

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


class GraphQLQueryFPath(StrEnum):
    RESOURCE_PROVIDER = "models/query_resource_provider.graphql"
    RESOURCE_CAPACITY = "models/query_resource_capacity.graphql"
    APPLICATION_PROVIDER = "models/query_application_provider.graphql"


def get_graphql_attributes_json(graphql_server_url: str, query_fpath: Path, variables: Optional[dict] = None) -> dict:

    with open(query_fpath, 'r') as query_file:
        query = query_file.read()

    # headers = {
    #     'Content-Type': 'application/json',
    #     'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
    # }

    response = requests.post(
        f"{graphql_server_url}/graphql",
        json={'query': query, 'variables': variables},
        # headers=headers
    )
    response.raise_for_status()
    graphql_data = response.json()["data"]
    return graphql_data


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