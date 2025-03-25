import numpy as np
from utils.helpers import verify_did, validate_location

# The ontology is defined here

class TrustEvaluator:
    def __init__(self, provider_weights, resource_weights, app_weights):
        self.provider_weights = provider_weights
        self.resource_weights = resource_weights
        self.app_weights = app_weights
        self.trusted_stakeholders = []


    def get_trusted_stakeholders(self):

        print('Trusted stakeholders:', [i[0] for i in self.trusted_stakeholders])
        return self.trusted_stakeholders
        
    def compute_trust(self, stakeholder):
        attributes = []
        if stakeholder.group == 'provider':
            # provider trust estimation 
            
            # did verification
            if not (verify_did(stakeholder.did)):
                setattr(stakeholder, 'trust', 0)
                return 
            
            # compliance
            # missing logic!!!!
            attributes.append(stakeholder.compliance)
            
            # historical behaviour
            # missing logic!!!!
            attributes.append(stakeholder.historical_behavior)

            # reputation
            # missing logic!!!!
            attributes.append(stakeholder.reputation)

            # direct trust
            # missing logic!!!!
            attributes.append(stakeholder.direct_trust)

            # final weighted trust
            setattr(stakeholder, 'trust', np.dot(self.provider_weights, attributes))

        elif stakeholder.group == 'resource':
            # resource trust estimation

            # did verification
            if not (verify_did(stakeholder.did)):
                setattr(stakeholder, 'trust', 0)
                return 
            
            # provider trust
            if not any(stakeholder.provider == trusted[1] for trusted in self.trusted_stakeholders):
                setattr(stakeholder, 'trust', 0)
                return
            
            # location
            if not validate_location(stakeholder.location):
                setattr(stakeholder, 'trust', 0)
                return
            
            # performance metrics
            attributes.append(self.compute_performance(stakeholder))

            # historical behaviour
            # missing logic!!!!
            attributes.append(stakeholder.historical_behavior)

            # contextual fit
            # missing logic!!!!
            attributes.append(stakeholder.contextual_fit)

            # third party validation
            # missing logic!!!!
            attributes.append(stakeholder.third_party_validation)

            # reputation
            # missing logic!!!!
            attributes.append(stakeholder.reputation)

            # direct trust
            # missing logic!!!!
            attributes.append(stakeholder.direct_trust)

            # final weighted trust
            setattr(stakeholder, 'trust', np.dot(self.resource_weights, attributes))
            

        elif stakeholder.group == 'app':
            # app trust estimation

            # did verification
            if not (verify_did(stakeholder.did)):
                setattr(stakeholder, 'trust', 0)
                return
            
            # location
            if not validate_location(stakeholder.location):
                setattr(stakeholder, 'trust', 0)
                return

            # compliance
            # missing logic!!!!
            attributes.append(stakeholder.compliance)

            # reputation
            # missing logic!!!!
            attributes.append(stakeholder.reputation)

            # direct trust
            # missing logic!!!!
            attributes.append(stakeholder.direct_trust)

            # final weighted trust
            setattr(stakeholder, 'trust', np.dot(self.app_weights, attributes))            


        
        else:
            print(f"Warning: {stakeholder.name} does not belong to a valid group")
            return
    
    def compute_performance(self, stakeholder):
        metrics = stakeholder.performance_metrics
        return np.mean(list(metrics.values()))
    
    def update_attribute(self, stakeholder, attribute, new_value):
        if hasattr(stakeholder, attribute):
            setattr(stakeholder, attribute, new_value)
        else:
            print(f"Warning: {stakeholder.name} does not have attribute {attribute}")

    def trust_evaluation(self, stakeholder):
        # Gets stakeholder trust if above a certain treshold add to trusted_stakeholders
        if getattr(stakeholder, 'trust') > 0.5:
            if (stakeholder.name, stakeholder.did) not in self.trusted_stakeholders:
                self.trusted_stakeholders.append((stakeholder.name, stakeholder.did))
            print(f"{stakeholder.name} is trustworthy")
        else:
            if (stakeholder.name, stakeholder.did) in self.trusted_stakeholders:    
                self.trusted_stakeholders.remove((stakeholder.name, stakeholder.did))
            print(f"{stakeholder.name} is not trustworthy")