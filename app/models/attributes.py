
from abc import ABC, abstractmethod
from typing import Any, Optional
import numpy as np
from enum import Enum, auto

from app.utils.helpers import Coordinates, validate_location, verify_did, StakeholderType, prob_transform, MetricNames
from app.models.did import DID
from app.trust_evaluation.probabilistic import SingleFeatureTrustModel

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

RANGES = {
        MetricNames.AVAILABILITY: (0, 1, 1),
        MetricNames.RELIABILITY: (0, 1, 1),
        MetricNames.ENERGY_EFFICIENCY: (0, 1, 1),
        MetricNames.LATENCY: (0, 1, -1),
        MetricNames.THROUGHPUT: (0, 1, 1),
        MetricNames.BANDWIDTH: (0, 1, 1),
        MetricNames.JITTER: (0, 1, -1),
        MetricNames.PACKET_LOSS: (0, 1, -1),
        MetricNames.UTILIZATION_RATE: (0, 1, 1)
}

class TrustCalcModel(Enum):
    DETERMINISTIC = auto()
    PROBABILISTIC = auto()

DEFAULT_TRUST_ATTRIBUTE = 0.5

class Attribute(ABC):
    trust: float
    weight: Optional[float]  # Weight is optional

    def __init__(self, weight: Optional[float] = None):
        self.weight = weight  
        self.trust = DEFAULT_TRUST_ATTRIBUTE  # Default trust value(thinking of probabilities)

    @abstractmethod
    def calculate_trust(self):
        pass


class Identity(Attribute):

    def __init__(self, entity: StakeholderType, did: DID):
        super().__init__()

        self.did = did
        pass

    def calculate_trust(self):
        if verify_did(self.did):
            self.trust = 1
        else:
            self.trust = 0


class Reputation(Attribute):

    def __init__(self, entity: StakeholderType, trust: Optional[Any] = None):
        super().__init__(AttributeWeights.REPUTATION[entity])

        self.trust = trust
        pass

    def calculate_trust(self):
        if self.trust is None:
            self.trust = DEFAULT_TRUST_ATTRIBUTE

        
class DirectTrust(Attribute):

    def __init__(self, entity: StakeholderType, trust: Optional[Any] = None):
        super().__init__(AttributeWeights.DIRECT_TRUST[entity])
        self.trust = trust
        pass

    def calculate_trust(self):
        if self.trust is None:
            self.trust = DEFAULT_TRUST_ATTRIBUTE




class Compliance(Attribute):

    def __init__(self, entity: StakeholderType, trust: Optional[Any] = None):
        super().__init__(AttributeWeights.COMPLIANCE[entity])
        self.trust = trust
        pass

    def calculate_trust(self):
        if self.trust is None:
            self.trust = DEFAULT_TRUST_ATTRIBUTE


class HistoricalBehavior(Attribute):

    def __init__(self, entity: StakeholderType, trust: Optional[Any] = None):
        super().__init__(AttributeWeights.HISTORICAL_BEHAVIOR[entity])
        self.trust = trust
        pass

    def calculate_trust(self):
        if self.trust is None:
            self.trust = DEFAULT_TRUST_ATTRIBUTE



class Performance(Attribute):

    def __init__(self, entity: StakeholderType, metrics: Any):
        super().__init__(AttributeWeights.PERFORMANCE[entity])

        self.metrics = metrics
        self.sftm = []
        for key in self.metrics.keys():
            self.sftm.append(SingleFeatureTrustModel(name=key))
        pass

    def compute_performance(self, model):

        if model == TrustCalcModel.DETERMINISTIC:
            normalized_metrics = []
            for metric_key in self.metrics.keys():
                for metric_value in self.metrics[metric_key]:
                    minimum, maximum, behavior = RANGES[metric_key]
                    v_prob = prob_transform(minimum, maximum, behavior, metric_value)
                    normalized_metrics.append(v_prob)
            trust = np.mean(normalized_metrics)
            for key in self.metrics.keys():
                self.metrics[key] = []
            return trust
            
        elif model == TrustCalcModel.PROBABILISTIC:
            for m in self.sftm:
                for v in self.metrics[m.name]:
                    if m.name in RANGES:
                        minimum, maximum, behavior = RANGES[m.name]
                        v_prob = prob_transform(minimum, maximum, behavior, v)
                    else: 
                        v_prob = v
                    m.observe(v_prob)

            for key in self.metrics.keys():
                self.metrics[key] = []
            return np.mean([m.adjusted_trust_score for m in self.sftm])
        else:
            raise

    def calculate_trust(self, model: Optional[TrustCalcModel] = None):
        self.trust = float(self.compute_performance(model))


class Location(Attribute):

    def __init__(self, entity: StakeholderType, coordinates: Coordinates):
        super().__init__()

        self.coordinates: Coordinates = coordinates
        pass

    def calculate_trust(self):
        if validate_location(self.coordinates):
            self.trust = 1
        else:
            self.trust = 0


class ContextualFit(Attribute):

    def __init__(self, entity: StakeholderType, trust: Optional[Any] = None):
        super().__init__(AttributeWeights.CONTEXTUAL_FIT[entity])
        self.trust = trust
        pass

    def calculate_trust(self):
        if self.trust is None:
            self.trust = DEFAULT_TRUST_ATTRIBUTE



class ThirdPartyValidation(Attribute):

    def __init__(self, entity: StakeholderType, trust: Optional[Any] = None):
        super().__init__(AttributeWeights.THIRD_PARTY_VALIDATION[entity])
        self.trust = trust
        pass

    def calculate_trust(self):
        if self.trust is None:
            self.trust = DEFAULT_TRUST_ATTRIBUTE


