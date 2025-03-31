import numpy as np

from utils.helpers import verify_did, validate_location
from models.stakeholder import ResourceProvider, ResourceCapacity, ApplicationProvider

# The ontology is defined here

class TrustEvaluator:
    
    def __init__(self):
        self.trusted_stakeholders = []

    def get_trusted_stakeholders(self):

        print('Trusted stakeholders:', [i[0] for i in self.trusted_stakeholders])
        return self.trusted_stakeholders
        
    def compute_trust(self, stakeholder):
        attributes_trust = []
        weights = []

        if isinstance(stakeholder, ResourceProvider):
            # provider trust estimation 
            
            # did verification
            stakeholder.identity_verification.calculate_trust()
            weights.append(stakeholder.identity_verification.weight)
            attributes_trust.append(stakeholder.identity_verification.trust)
            
            # compliance
            stakeholder.compliance.calculate_trust()
            weights.append(stakeholder.compliance.weight)
            attributes_trust.append(stakeholder.compliance.trust)
            
            # historical behaviour
            stakeholder.historical_behavior.calculate_trust()
            weights.append(stakeholder.historical_behavior.weight)
            attributes_trust.append(stakeholder.historical_behavior.trust)

            # reputation
            stakeholder.reputation.calculate_trust()
            weights.append(stakeholder.reputation.weight)
            attributes_trust.append(stakeholder.reputation.trust)

            # direct trust
            stakeholder.direct_trust.calculate_trust()
            weights.append(stakeholder.direct_trust.weight)
            attributes_trust.append(stakeholder.direct_trust.trust)


        elif isinstance(stakeholder, ResourceCapacity):
            # resource trust estimation

            # did verification
            stakeholder.identity_verification.calculate_trust()
            weights.append(stakeholder.identity_verification.weight)
            attributes_trust.append(stakeholder.identity_verification.trust)
            
            # provider trust
            if not any(stakeholder.provider.did == trusted[1] for trusted in self.trusted_stakeholders):
                stakeholder.trust = 0
                return
            
            # location
            stakeholder.location.calculate_trust()
            weights.append(stakeholder.location.weight)
            attributes_trust.append(stakeholder.location.trust)
            
            # performance metrics
            stakeholder.performance.calculate_trust()
            weights.append(stakeholder.performance.weight)
            attributes_trust.append(stakeholder.performance.trust)

            # historical behaviour
            stakeholder.historical_behavior.calculate_trust()
            weights.append(stakeholder.historical_behavior.weight)
            attributes_trust.append(stakeholder.historical_behavior.trust)

            # contextual fit
            stakeholder.contextual_fit.calculate_trust()
            weights.append(stakeholder.contextual_fit.weight)
            attributes_trust.append(stakeholder.contextual_fit.trust)

            # third party validation
            stakeholder.third_party_validation.calculate_trust()
            weights.append(stakeholder.third_party_validation.weight)
            attributes_trust.append(stakeholder.third_party_validation.trust)

            # reputation
            stakeholder.reputation.calculate_trust()
            weights.append(stakeholder.reputation.weight)
            attributes_trust.append(stakeholder.reputation.trust)

            # direct trust
            stakeholder.direct_trust.calculate_trust()
            weights.append(stakeholder.direct_trust.weight)
            attributes_trust.append(stakeholder.direct_trust.trust)


        elif isinstance(stakeholder, ApplicationProvider):
            # app trust estimation

            # did verification
            stakeholder.identity_verification.calculate_trust()
            weights.append(stakeholder.identity_verification.weight)
            attributes_trust.append(stakeholder.identity_verification.trust)
            
            # location
            stakeholder.location.calculate_trust()
            weights.append(stakeholder.location.weight)
            attributes_trust.append(stakeholder.location.trust)

            # compliance
            stakeholder.compliance.calculate_trust()
            weights.append(stakeholder.compliance.weight)
            attributes_trust.append(stakeholder.compliance.trust)

            # reputation
            stakeholder.reputation.calculate_trust()
            weights.append(stakeholder.reputation.weight)
            attributes_trust.append(stakeholder.reputation.trust)

            # direct trust
            stakeholder.direct_trust.calculate_trust()
            weights.append(stakeholder.direct_trust.weight)
            attributes_trust.append(stakeholder.direct_trust.trust)

        else:
            print(f"Warning: {stakeholder.name} does not belong to a valid group")
            return
        
        # final weighted trust
        stakeholder.trust = np.dot(weights, attributes_trust)
    
    '''def update_attribute(self, stakeholder, attribute, new_value):
        if hasattr(stakeholder, attribute):
            setattr(stakeholder, attribute, new_value)
        else:
            print(f"Warning: {stakeholder.name} does not have attribute {attribute}")'''

    def trust_evaluation(self, stakeholder):
        # Gets stakeholder trust if above a certain treshold add to trusted_stakeholders
        if stakeholder.trust > 0.5:
            if (stakeholder.name, stakeholder.did) not in self.trusted_stakeholders:
                self.trusted_stakeholders.append((stakeholder.name, stakeholder.did))
            print(f"{stakeholder.name} is trustworthy")
        else:
            if (stakeholder.name, stakeholder.did) in self.trusted_stakeholders:    
                self.trusted_stakeholders.remove((stakeholder.name, stakeholder.did))
            print(f"{stakeholder.name} is not trustworthy")