import uuid
from typing import Any, Optional
from abc import ABC
from enum import StrEnum
from pathlib import Path

from .did import DID
from app.utils.helpers import StakeholderType, get_graphql_query_json, camel_to_snake_case
from app.utils.settings import settings
from app.utils.helpers import MetricNames
from .attributes import Identity, \
                       Reputation, \
                       DirectTrust, \
                       Compliance, \
                       HistoricalBehavior, \
                       Performance, \
                       Location, \
                       ContextualFit, \
                       ThirdPartyValidation


INITIAL_TRUST = 0
DEFAULT_ATTRIBUTE_VALUE = 1
DEFAULT_LONGITUDE = 15.0
DEFAULT_LATITUDE = 46.0

TRUST_METRIC_AGGREGATOR_HOST = settings.trust_metric_aggregator_host
TRUST_METRIC_AGGREGATOR_PORT = settings.trust_metric_aggregator_port

class GraphQLQueryFPath(StrEnum):
    RESOURCE_PROVIDER = "query_resource_provider.graphql"
    RESOURCE_CAPACITY = "query_resource_capacity.graphql"
    APPLICATION_PROVIDER = "query_application_provider.graphql"


class Stakeholder(ABC):

    # Level of trust as a floating point number
    trust: float = INITIAL_TRUST

    def __init__(self, name: str, entity_idx: StakeholderType, did_raw: str, graphql_query_fpath: str, reputation: float, direct_trust: float):

        # Name of the stakeholder
        self.name: str = name

        # Type of entity converted to an integer (index)
        self.entity_idx: StakeholderType = entity_idx

        # Path to the GraphQL query for attributes
        self.graphql_query_fpath: str = graphql_query_fpath

        # DID - Decentralized identifier
        self.did: DID = DID(did_raw)

        # 
        self.identity = Identity(entity_idx, self.did)

        # 
        self.reputation = Reputation(entity_idx, reputation)

        # 
        self.direct_trust = DirectTrust(entity_idx, direct_trust)

    def get_new_attributes(self) -> dict:
        aggregator_url = f"http://{TRUST_METRIC_AGGREGATOR_HOST}:{TRUST_METRIC_AGGREGATOR_PORT}"
        query_abs_fpath = Path(__file__).parent.absolute() / self.graphql_query_fpath
        query_variables = {"did": self.did.raw}
        aggregator_data = get_graphql_query_json(aggregator_url, query_abs_fpath, query_variables)
        return aggregator_data

    def update_attributes(self):
        """
        Used for updating attributes.
        """
        new_trust_attributes = self.get_new_attributes()
        if new_trust_attributes is None:
            print(f"No trust attributes returned for stakeholder {self.did.raw}. Skipping update.")
            return

        # Iterate and determine new values of attributes of trust attributes
        # Important: attributes (in snake case) must have the same name as GraphQL attributes (in camel case)
        for trust_attribute_key, trust_attribute_value in new_trust_attributes.items():
            for attr_key, attr_value in trust_attribute_value.items():
                trust_attribute = getattr(self, camel_to_snake_case(trust_attribute_key))

                # For performance metrics instead append the value
                if camel_to_snake_case(trust_attribute_key) == 'performance':
                    if (trust_attribute and
                            hasattr(trust_attribute, 'metrics') and
                            camel_to_snake_case(attr_key) in trust_attribute.metrics):
                        trust_attribute.metrics[camel_to_snake_case(attr_key)].append(attr_value)
                else:
                    if trust_attribute and hasattr(trust_attribute, camel_to_snake_case(attr_key)):
                        setattr(trust_attribute, camel_to_snake_case(attr_key), attr_value)


class ResourceProvider(Stakeholder): # or Resource Capacity provider

    def __init__(self, name: str, did_raw: str, reputation: float = DEFAULT_ATTRIBUTE_VALUE,
                 direct_trust: float = DEFAULT_ATTRIBUTE_VALUE, compliance: float = DEFAULT_ATTRIBUTE_VALUE,
                 historical_behavior: float = DEFAULT_ATTRIBUTE_VALUE):

        super().__init__(name, StakeholderType.RESOURCE_PROVIDER, did_raw, GraphQLQueryFPath.RESOURCE_PROVIDER, reputation, direct_trust)

        self.compliance = Compliance(StakeholderType.RESOURCE_PROVIDER, compliance)
        self.historical_behavior = HistoricalBehavior(StakeholderType.RESOURCE_PROVIDER, historical_behavior)

        # self.update_attributes()  # Initialize the trust attributes

class ResourceCapacity(Stakeholder): # or Resources

    def __init__(self, name: str, did_raw: str, provider: Optional[ResourceProvider] = None,
                 reputation: float = DEFAULT_ATTRIBUTE_VALUE, direct_trust: float = DEFAULT_ATTRIBUTE_VALUE,
                 performance: float = DEFAULT_ATTRIBUTE_VALUE, lat: float = DEFAULT_LATITUDE, lon: float = DEFAULT_LONGITUDE,
                 historical_behavior: float = DEFAULT_ATTRIBUTE_VALUE, contextual_fit: float = DEFAULT_ATTRIBUTE_VALUE,
                 third_party_validation: float = DEFAULT_ATTRIBUTE_VALUE):

        super().__init__(name, StakeholderType.RESOURCE_CAPACITY, did_raw, GraphQLQueryFPath.RESOURCE_CAPACITY, reputation, direct_trust)

        default_performance_metrics = {
            MetricNames.AVAILABILITY: [],
            MetricNames.RELIABILITY: [],
            MetricNames.ENERGY_EFFICIENCY: [],
            MetricNames.LATENCY: [],
            MetricNames.THROUGHPUT: [],
            MetricNames.BANDWIDTH: [],
            MetricNames.JITTER: [],
            MetricNames.PACKET_LOSS: [],
            MetricNames.UTILIZATION_RATE: []
        }
        self.performance = Performance(StakeholderType.RESOURCE_CAPACITY, default_performance_metrics)
        self.location = Location(StakeholderType.APPLICATION_PROVIDER, lat, lon)
        self.historical_behavior = HistoricalBehavior(StakeholderType.RESOURCE_CAPACITY, historical_behavior)
        self.contextual_fit = ContextualFit(StakeholderType.RESOURCE_CAPACITY, contextual_fit)
        self.third_party_validation = ThirdPartyValidation(StakeholderType.RESOURCE_CAPACITY, third_party_validation)

        self.provider: ResourceProvider = provider

        # self.update_attributes()  # Initialize the trust attributes


class ApplicationProvider(Stakeholder):

    def __init__(self, name: str, did_raw: str, reputation: float = DEFAULT_ATTRIBUTE_VALUE,
                 direct_trust: float = DEFAULT_ATTRIBUTE_VALUE, compliance: float = DEFAULT_ATTRIBUTE_VALUE,
                 lat: float = DEFAULT_LATITUDE, lon: float = DEFAULT_LONGITUDE):

        super().__init__(name, StakeholderType.APPLICATION_PROVIDER, did_raw, GraphQLQueryFPath.APPLICATION_PROVIDER, reputation, direct_trust)

        self.compliance = Compliance(StakeholderType.APPLICATION_PROVIDER, compliance)
        self.location = Location(StakeholderType.APPLICATION_PROVIDER, lat, lon)

        # self.update_attributes()  # Initialize the trust attributes

