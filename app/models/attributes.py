
from abc import ABC, abstractmethod
from typing import Any, Optional
from app.trust_evaluation.probabilistic import SingleFeatureTrustModel
import numpy as np
from enum import Enum, auto

from app.utils.helpers import Coordinates, validate_location, verify_did, Entities, prob_transform
from app.models.did import DID

class AttributeWeights:
   # IDENTITY_VERIFICATION = (0.1, 0.2, 0.3)
    REPUTATION = (0.5, 0.6, 0.7)
    DIRECT_TRUST = (0.5, 0.6, 0.7)
    COMPLIANCE = (1.2, 0.6, 0.7)
    HISTORICAL_BEHAVIOR = (0.1, 0,2, 0.3)
    PERFORMANCE = (0.1, 1.6, 0.3)
    # LOCATION = (0.1, 0.2, 0.3)
    CONTEXTUAL_FIT = (0.1, 0.2, 0.3)
    THIRD_PARTY_VALIDATION = (0.1, 0.2, 0.3)


class TrustCalcModel(Enum):
    DETERMINISTIC = auto()
    PROBABILISTIC = auto()


class Attribute(ABC):
    trust: float
    weight: Optional[float]  # Weight is optional

    def __init__(self, weight: Optional[float] = None):
        self.weight = weight  
        self.trust = 0.5  # Default trust value(thinking of probabilities)

    @abstractmethod
    def calculate_trust(self):
        pass


class IdentityVerification(Attribute):

    def __init__(self, entity: Entities, did: DID):
        super().__init__()

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
        self.sftm = []
        for key in self.metrics.keys():
            self.sftm.append(SingleFeatureTrustModel(name=key))
        pass

    def compute_performance(self, model, ranges):

        if model == TrustCalcModel.DETERMINISTIC:
            normalized_metrics = []
            for metric in self.metrics:
                minimum, maximum = ranges[metric.name]
                v_prob = prob_transform(minimum, maximum, metric.value)
                normalized_metrics.append(v_prob)
            trust = np.mean(list(self.metrics.values()))
            for key in self.metrics.keys():
                self.metrics[key] = []
            return trust
            
        elif model == TrustCalcModel.PROBABILISTIC:
            for m in self.sftm:
                for v in self.metrics[m.name]:
                    if m.name in ranges:
                        minimum, maximum = ranges[m.name]
                        v_prob = prob_transform(minimum, maximum, v)
                    else: 
                        v_prob = v
                    m.observe(v_prob)

            for key in self.metrics.keys():
                self.metrics[key] = []
            return np.mean([m.adjusted_trust_score for m in self.sftm])

    def calculate_trust(self, model: Optional[TrustCalcModel] = None, ranges: Optional[list] = None):
        self.trust = float(self.compute_performance(model, ranges))


class Location(Attribute):

    def __init__(self, entity: Entities, coordinates: Coordinates):
        super().__init__()

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

