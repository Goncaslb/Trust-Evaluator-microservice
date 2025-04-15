from models.stakeholder import ResourceProvider, ResourceCapacity, ApplicationProvider
from trust_evaluation.trust_evaluator import TrustEvaluator

def main():
    
    # ProviderA is a simple example which will be trusted
    providerA = ResourceProvider(name="Provider_A", did_raw="did:example:123", compliance=1, historical_behavior=0.7, reputation=0.6, direct_trust=0.9)
    
    # CapacityA is a resource provided from  providerA which will also be trusted
    capacityA = ResourceCapacity(name="Capacity_A", did_raw="did:example:456", performance={"throughput": 0.8, "bandwidth": 0.7}, location=(46.05, 14.47), historical_behavior=0.8, contextual_fit=0.7, third_party_validation=0.6, reputation=0.65, direct_trust=0.8, provider=providerA)
    
    # AppProviderX is an application provider that will be trusted
    app_providerX = ApplicationProvider(name="AppProvider_X", did_raw="did:example:789", compliance=1, location=(46.05, 14.47), reputation=0.65, direct_trust=0.85)
    
    # App provider that will not be trusted
    bad_app_providerH = ApplicationProvider(name="AppProvider_H", did_raw="did:example:326", compliance=0.1, location=(46.05, 14.47), reputation=0.4, direct_trust=0.3)

    evaluator = TrustEvaluator()
    stakeholders = [providerA, capacityA, app_providerX, bad_app_providerH]
    
    print("Initial Trust Scores and Evaluation:")
    for s in stakeholders:
        evaluator.compute_trust(s)
        print(f"{s.name}: {s.trust:.4f}")
        evaluator.trust_evaluation(s)
    
    trusted_stakeholders = evaluator.get_trusted_stakeholders()
    
    # Now we simmulate that there was registered a worst performance of CapacityA so we want to see a difference  in the trust value
    new_performance = {"throughput": 0.5, "bandwidth": 0.30}
    capacityA.performance.metrics = new_performance

    print("\nTrust Scores After Performance Update:")
    for s in stakeholders:
        evaluator.compute_trust(s)
        print(f"{s.name}: {s.trust:.4f}")


    # now we will change the resource provider compliance and recalculate the trust scores showing that the resource is no longer trusted

    providerA.compliance.trust = 0
    print('\nTrust evaluation after seeting provider compliance to 0:')
    for s in stakeholders:
        evaluator.compute_trust(s)
        evaluator.trust_evaluation(s)
    
    a = evaluator.get_trusted_stakeholders()

    # now we will change the location of the app and verify that we will have zero trusted stakeholders
    app_providerX.location.coordinates = (0,0)

    print('\nTrust evaluation after setting app provider location out of Slovenia:')
    for s in stakeholders:
        evaluator.compute_trust(s)
        print(f"{s.name}: {s.trust:.4f}")
        evaluator.trust_evaluation(s)
    
    a = evaluator.get_trusted_stakeholders()

    
if __name__ == "__main__":
    main()



# onthologist? so reestructure the way trust works. dependencies between stakeholders. 

# add location fail example

# provider fail example

# maybe join both, we have a provider that is trusted then we change the location and it becomes not trusted making the resource not trusted.