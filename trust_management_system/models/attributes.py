
from abc import ABC, abstractmethod
from typing import Any
import numpy as np
import os
import sys

from utils.helpers import Coordinates, Entities, validate_location, verify_did
from models.did import DID

class AttributeWeights:
    IDENTITY_VERIFICATION = (0.1, 0.2, 0.3)
    REPUTATION = (0.1, 0.2, 0.3)
    DIRECT_TRUST = (0.1, 0.2, 0.3)
    COMPLIANCE = (0.1, 0.2, 0.3)
    HISTORICAL_BEHAVIOR = (0.1, 0.2, 0.3)
    PERFORMANCE = (0.1, 0.2, 0.3)
    LOCATION = (0.1, 0.2, 0.3)
    CONTEXTUAL_FIT = (0.1, 0.2, 0.3)
    THIRD_PARTY_VALIDATION = (0.1, 0.2, 0.3)


class Attribute(ABC):

    trust: float
    
    def __init__(self, weight: int):
        self.weight: int = weight

    @abstractmethod
    def calculate_trust(self):
        pass


class IdentityVerification(Attribute):

    def __init__(self, entity: Entities, did: DID):
        super().__init__(AttributeWeights.IDENTITY_VERIFICATION[entity])

        self.did = did
        pass

    def calculate_trust(self):
        if verify_did(self.did):
            self.trust = 1
        else:
            self.trust = 0


class Reputation(Attribute):

    def __init__(self, entity: Entities, trust: Any):
        super().__init__(AttributeWeights.REPUTATION[entity])

        self.trust = trust
        pass

    def calculate_trust(self):
        self.trust = self.trust

        
class DirectTrust(Attribute):

    def __init__(self, entity: Entities, trust: Any):
        super().__init__(AttributeWeights.DIRECT_TRUST[entity])
        self.trust = trust
        pass

    def calculate_trust(self):
        self.trust = self.trust



class Compliance(Attribute):

    def __init__(self, entity: Entities, trust: Any):
        super().__init__(AttributeWeights.COMPLIANCE[entity])
        self.trust = trust
        pass

    def calculate_trust(self):
        self.trust = self.trust

class HistoricalBehavior(Attribute):

    def __init__(self, entity: Entities, trust: Any):
        super().__init__(AttributeWeights.HISTORICAL_BEHAVIOR[entity])
        self.trust = trust
        pass

    def calculate_trust(self):
        self.trust = self.trust


class Performance(Attribute):

    def __init__(self, entity: Entities, metrics: Any):
        super().__init__(AttributeWeights.PERFORMANCE[entity])

        self.metrics = metrics
        pass

    def compute_performance(self):
        return np.mean(list(self.metrics.values()))

    def calculate_trust(self):
        self.trust = self.compute_performance


class Location(Attribute):

    def __init__(self, entity: Entities, coordinates: Coordinates):
        super().__init__(AttributeWeights.LOCATION[entity])

        self.coordinates: Coordinates = coordinates
        pass

    def calculate_trust(self):
        if validate_location(self.coordinates):
            self.trust = 1
        else:
            self.trust = 0


class ContextualFit(Attribute):

    def __init__(self, entity: Entities, trust: Any):
        super().__init__(AttributeWeights.CONTEXTUAL_FIT[entity])
        self.trust = trust
        pass

    def calculate_trust(self):
        self.trust = self.trust


class ThirdPartyValidation(Attribute):

    def __init__(self, entity: Entities, trust: Any):
        super().__init__(AttributeWeights.THIRD_PARTY_VALIDATION[entity])
        self.trust = trust
        pass

    def calculate_trust(self):
        self.trust = self.trust

