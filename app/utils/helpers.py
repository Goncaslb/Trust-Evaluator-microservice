from typing import NamedTuple
from enum import IntEnum, StrEnum
import requests
from pathlib import Path
import re
import numpy as np

from app.models.did import DID

class StakeholderType(IntEnum):
    RESOURCE_PROVIDER = 0
    RESOURCE_CAPACITY = 1
    APPLICATION_PROVIDER = 2
    RESOURCE = 3
    CAPACITY_PROVIDER = 4

class MetricNames(StrEnum):
    AVAILABILITY = "availability"
    RELIABILITY = "reliability"
    ENERGY_EFFICIENCY = "energy_efficiency"
    LATENCY = "latency"
    THROUGHPUT = "throughput"
    BANDWIDTH = "bandwidth"
    JITTER = "jitter"
    PACKET_LOSS = "packet_loss"
    UTILIZATION_RATE = "utilization_rate"

class Coordinates(NamedTuple):
    lat: float
    lon: float


def get_graphql_query_json(graphql_server_url: str, query_fpath: Path, variables: dict) -> dict:

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

def camel_to_snake_case(camel_case_string: str) -> str:
    """
    Convert camelCase to snake_case for parsing GraphQL responses into class attributes.
    """
    snake_case_string = re.sub(r'(?<!^)(?=[A-Z])', '_', camel_case_string).lower()
    return snake_case_string

def verify_did(did: DID):
    if did.raw.startswith("did:"):
        return True
    else:
        print(f"Warning: {did} is not a valid DID")
        return False

def prob_transform(minimum: float, maximum: float, value: float) -> float:
    if value <= minimum:
        return 0.0
    elif value >= maximum:
        return 1.0
    else:
        # Scale the value to the range [0, 1] using a sigmoid-like function
        mid = (minimum + maximum) / 2  # Midpoint of the range
        scale = (maximum - minimum) / 6  # Scale factor for smooth transition
        return 1 / (1 + np.exp(-(value - mid) / scale))


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