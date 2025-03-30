
from abc import ABC, abstractmethod

from stakeholder import Entities

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

    def __init__(self, entity: Entities):
        super().__init__(AttributeWeights.IDENTITY_VERIFICATION[entity])
        pass

    def calculate_trust(self, trust: float):
        self.trust = trust


class Reputation(Attribute):

    def __init__(self, entity: Entities):
        super().__init__(AttributeWeights.REPUTATION[entity])
        pass

    def calculate_trust(self, trust: float):
        self.trust = trust

        
class DirectTrust(Attribute):

    def __init__(self, entity: Entities):
        super().__init__(AttributeWeights.DIRECT_TRUST[entity])
        pass

    def calculate_trust(self, trust: float):
        self.trust = trust


class Compliance(Attribute):

    def __init__(self, entity: Entities):
        super().__init__(AttributeWeights.COMPLIANCE[entity])
        pass

    def calculate_trust(self, trust: float):
        self.trust = trust


class HistoricalBehavior(Attribute):

    def __init__(self, entity: Entities):
        super().__init__(AttributeWeights.HISTORICAL_BEHAVIOR[entity])
        pass

    def calculate_trust(self, trust: float):
        self.trust = trust


class Performance(Attribute):

    def __init__(self, entity: Entities):
        super().__init__(AttributeWeights.PERFORMANCE[entity])
        pass

    def calculate_trust(self, trust: float):
        self.trust = trust


class Location(Attribute):

    def __init__(self, entity: Entities):
        super().__init__(AttributeWeights.LOCATION[entity])
        pass

    def calculate_trust(self, trust: float):
        self.trust = trust


class ContextualFit(Attribute):

    def __init__(self, entity: Entities):
        super().__init__(AttributeWeights.CONTEXTUAL_FIT[entity])
        pass

    def calculate_trust(self, trust: float):
        self.trust = trust


class ThirdPartyValidation(Attribute):

    def __init__(self, entity: Entities):
        super().__init__(AttributeWeights.THIRD_PARTY_VALIDATION[entity])
        pass

    def calculate_trust(self, trust: float):
        self.trust = trust

