import uuid
from typing import Optional, Any
from abc import ABC, abstractmethod
from enum import IntEnum

from .did import DID
from utils.helpers import Coordinates, Entities, GraphQLQueryFPath
from .attributes import IdentityVerification, \
                       Reputation, \
                       DirectTrust, \
                       Compliance, \
                       HistoricalBehavior, \
                       Performance, \
                       Location, \
                       ContextualFit, \
                       ThirdPartyValidation


INITIAL_TRUST = 0

class Stakeholder(ABC):

    # Each time a new uuid is generated
    id: uuid.UUID = uuid.uuid4()

    # Level in trust as a floating point number
    trust: float = INITIAL_TRUST

    def __init__(self, name: str, entity_idx: Entities, did_raw: str, graphql_query_fpath: str, reputation: float, direct_trust: float):

        # Name of the stakeholder
        self.name: str = name

        # Type of entity converted to an integer (index)
        self.entity_idx: Entities = entity_idx

        # Path to the GraphQL query for attributes
        self.graphql_query_fpath: str = graphql_query_fpath

        # DID - Decentralized identifier
        self.did: DID = DID(did_raw)

        # 
        self.identity_verification = IdentityVerification(entity_idx, self.did)

        # 
        self.reputation = Reputation(entity_idx, reputation)

        # 
        self.direct_trust = DirectTrust(entity_idx, direct_trust)


class ResourceProvider(Stakeholder): # or Resource Capacity provider

    def __init__(self, name: str, did_raw: str, reputation: float, direct_trust: float, compliance: float, historical_behavior: float):

        super().__init__(name, Entities.RESOURCE_PROVIDER, did_raw, GraphQLQueryFPath.RESOURCE_PROVIDER, reputation, direct_trust)

        self.compliance = Compliance(Entities.RESOURCE_PROVIDER, compliance)
        self.historical_behavior = HistoricalBehavior(Entities.RESOURCE_PROVIDER, historical_behavior)


class ResourceCapacity(Stakeholder): # or Resources

    def __init__(self, name: str, did_raw: str, reputation: float, direct_trust: float, performance: Any, location: Coordinates, historical_behavior: float, contextual_fit: float, third_party_validation: float, provider: ResourceProvider):

        super().__init__(name, Entities.RESOURCE_CAPACITY, did_raw, GraphQLQueryFPath.RESOURCE_CAPACITY, reputation, direct_trust)

        self.performance = Performance(Entities.RESOURCE_CAPACITY, performance)
        self.location = Location(Entities.RESOURCE_CAPACITY, location)
        self.historical_behavior = HistoricalBehavior(Entities.RESOURCE_CAPACITY, historical_behavior)
        self.contextual_fit = ContextualFit(Entities.RESOURCE_CAPACITY, contextual_fit)
        self.third_party_validation = ThirdPartyValidation(Entities.RESOURCE_CAPACITY, third_party_validation)

        self.provider: ResourceProvider = provider  # TODO add as attribute?


class ApplicationProvider(Stakeholder):

    def __init__(self, name: str, did_raw: str, reputation: float, direct_trust: float, compliance: float, location: Coordinates):

        super().__init__(name, Entities.APPLICATION_PROVIDER, did_raw, GraphQLQueryFPath.APPLICATION_PROVIDER, reputation, direct_trust)

        self.compliance = Compliance(Entities.APPLICATION_PROVIDER, compliance)
        self.location = Location(Entities.APPLICATION_PROVIDER, location)

