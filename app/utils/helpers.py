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


def get_graphql_query_json(graphql_server_url: str, query_fpath: Path, variables: dict) -> dict:
    with open(query_fpath, 'r') as query_file:
        query = query_file.read()
    try:
        response = requests.post(
            f"{graphql_server_url}/graphql",
            json={'query': query, 'variables': variables},
        )
        response.raise_for_status()
        graphql_data = response.json().get("data")
        if graphql_data is None:
            print(f"GraphQL response missing 'data': {response.text}")
        return graphql_data
    except Exception as e:
        print(f"Error in get_graphql_query_json: {e}")
        return None

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

import numpy as np

def prob_transform(minimum: float, maximum: float, behaviour: float, value: float) -> float:
    if behaviour == 1:
        if value <= minimum:
            return 0.0
        elif value >= maximum:
            return 1.0
        else:
            # Scale the value to the range [0, 1] using a sigmoid-like function
            mid = (minimum + maximum) / 2  # Midpoint of the range
            scale = (maximum - minimum) / 6  # Scale factor for smooth transition
            return 1 / (1 + np.exp(-(value - mid) / scale))
    elif behaviour == -1:
        if value <= minimum:
            return 1.0  # Minimum or below equals 1 (better)
        elif value >= maximum:
            return 0.0  # Maximum or above equals 0 (worse)
        else:
            # Scale the value to the range [0, 1] in reverse using a sigmoid-like function
            mid = (minimum + maximum) / 2
            scale = (maximum - minimum) / 6
            return 1 - (1 / (1 + np.exp(-(value - mid) / scale))) # Reverse the sigmoid output
    elif behaviour == 0:
        if value <= minimum or value >= maximum:
            return 0.0  # Outside the limits is 0
        else:
            # The closer to the middle point, the better (closer to 1)
            mid = (minimum + maximum) / 2
            # Max possible distance from midpoint is (maximum - minimum) / 2
            max_dist = (maximum - minimum) / 2
            normalized_value = (value - mid) / max_dist # Scales value to be in [-1, 1] relative to mid

            # Using a simple quadratic decay from the center
            return max(0.0, 1.0 - normalized_value**2) # Ensures it doesn't go below 0
    else:
        raise ValueError("Behaviour must be 1, -1, or 0")


def validate_location(lat: float, lon: float):
    """
    Validates if the given coordinates are within Slovenian territory.

    Returns:
        bool: True if the location is within Slovenia, False otherwise.
    """

    min_lat, max_lat = 45.42, 46.88 
    min_lon, max_lon = 13.38, 16.60
    print(f"Validating location: lat={lat}, lon={lon}")
    # Check if the coordinates are within the boundaries
    if min_lat <= lat <= max_lat:
        if min_lon <= lon <= max_lon:
            return True

    return False