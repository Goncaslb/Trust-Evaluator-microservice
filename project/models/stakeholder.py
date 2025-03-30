import uuid
from typing import Optional
from abc import ABC, abstractmethod
from enum import IntEnum

from did import DID
from attributes import IdentityVerification, \
                       Reputation, \
                       DirectTrust, \
                       Compliance, \
                       HistoricalBehavior, \
                       Performance, \
                       Location, \
                       ContextualFit, \
                       ThirdPartyValidation


INITIAL_TRUST = 0


class Entities(IntEnum):
    """
    Used for index of AttributeWeights. 
    """
    RESOURCE_PROVIDER = 0
    RESOURCE_CAPACITY = 1
    APPLICATION_PROVIDER = 2


class Stakeholder(ABC):

    # Each time a new uuid is generated
    id: uuid.UUID = uuid.uuid4()

    # Level in trust as a floating point number
    trust: float = INITIAL_TRUST



    def __init__(self, name: str, entity_idx: Entities, did_raw: str, reputation: float, direct_trust: float):

        # Name of the stakeholder
        self.name: str = name

        # Type of entity converted to an integer (index)
        self.entity_idx: Entities = entity_idx

        # DID - Decentralized identifier
        self.did: DID = DID(did_raw)

        # 
        self.identity_verification = IdentityVerification(entity_idx)

        # 
        self.reputation = Reputation(entity_idx, reputation)

        # 
        self.direct_trust = DirectTrust(entity_idx, direct_trust)

    @abstractmethod
    def calculate_trust(self):
        pass


class ResourceProvider(Stakeholder): # or Resource Capacity provider

    def __init__(self, name: str, did_raw: str, reputation: float, direct_trust: float, compliance: float, historical_behavior: float):

        super().__init__(name, did_raw, reputation, direct_trust)

        self.compliance = Compliance(Entities.RESOURCE_PROVIDER)
        self.historical_behavior = HistoricalBehavior(Entities.RESOURCE_PROVIDER)


class ResourceCapacity(Stakeholder): # or Resources

    def __init__(self, name: str, did_raw: str, reputation: float, direct_trust: float, performance: float, location: float, historical_behavior: float, contextual_fit: float, third_party_validation: float, provider: ResourceProvider):

        super().__init__(name, did_raw, reputation, direct_trust)

        self.performance = Performance(Entities.RESOURCE_CAPACITY)
        self.location = Location(Entities.RESOURCE_CAPACITY)
        self.historical_behavior = HistoricalBehavior(Entities.RESOURCE_CAPACITY)
        self.contextual_fit = ContextualFit(Entities.RESOURCE_CAPACITY)
        self.third_party_validation = ThirdPartyValidation(Entities.RESOURCE_CAPACITY)

        self.provider: ResourceProvider = provider


class ApplicationProvider(Stakeholder):

    def __init__(self, name: str, did_raw: str, reputation: float, direct_trust: float, compliance: float, location: float):

        super().__init__(name, did_raw, reputation, direct_trust)

        self.compliance = Compliance(Entities.APPLICATION_PROVIDER)
        self.location = Location(Entities.APPLICATION_PROVIDER)

