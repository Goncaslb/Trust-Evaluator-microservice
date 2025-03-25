class Stakeholder:
    # I have added the name, the trust and the group
    def __init__(self, name, trust, did, group): # can the group attribute be incorporated in the did?
        self.name = name
        self.trust = trust
        self.did = did
        self.group = group

class ResourceProvider(Stakeholder): # or resource capacity provider
    # no extra attribute added
    def __init__(self, name, trust, did, group, compliance, historical_behavior, reputation, direct_trust):
        super().__init__(name, trust, did, group)
        self.compliance = compliance
        self.historical_behavior = historical_behavior
        self.reputation = reputation
        self.direct_trust = direct_trust
        self.weights = [0.3, 0.2, 0.2, 0.2, 0.1]

class ResourceCapacity(Stakeholder): # or resources
    # added the provider attribute which is the did of the provider
    def __init__(self, name, trust, did, group, performance_metrics, location, historical_behavior, contextual_fit, third_party_validation, reputation, direct_trust, provider):
        super().__init__(name, trust, did, group)
        self.performance_metrics = performance_metrics  # Dictionary of performance indicators that can be changed. At the end it will have to be of a specific format
        self.location = location
        self.historical_behavior = historical_behavior
        self.contextual_fit = contextual_fit
        self.third_party_validation = third_party_validation
        self.reputation = reputation
        self.direct_trust = direct_trust
        self.provider = provider
        self.weights = [0.2, 0.2, 0.15, 0.15, 0.1, 0.1, 0.05, 0.05]

class ApplicationProvider(Stakeholder):
    # no extra attribute added
    def __init__(self, name, trust, did, group, compliance, location, reputation, direct_trust):
        super().__init__(name, trust, did, group)
        self.compliance = compliance
        self.location = location
        self.reputation = reputation
        self.direct_trust = direct_trust
        self.weights = [0.4, 0.2, 0.2, 0.1, 0.1]

