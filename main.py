
import requests
from pathlib import Path

from models.stakeholder import ResourceProvider, ResourceCapacity, ApplicationProvider
from trust_evaluation.trust_evaluator import TrustEvaluator
from utils.helpers import Coordinates, get_graphql_attributes_json
from utils.settings import settings


def main():
    
    # ProviderA is a simple example which will be trusted
    providerA = ResourceProvider(name="Provider_A", did_raw="did:example:123", compliance=1, historical_behavior=0.7, reputation=0.6, direct_trust=0.9)
    
    # CapacityA is a resource provided from  providerA which will also be trusted
    aggregator_url = f"http://{settings.trust_metric_aggregator_host}:{settings.trust_metric_aggregator_port}"
    query_fpath = Path(__file__).parent.absolute() / "models/query_resource_capacity.graphql"
    aggregator_data = get_graphql_attributes_json(aggregator_url, query_fpath)

    capacityA = ResourceCapacity(name="Capacity_A", 
                                 did_raw="did:example:456", 
                                 performance=aggregator_data["performanceMetrics"], 
                                 location=Coordinates(aggregator_data["location"]["lat"], aggregator_data["location"]["lon"]),
                                 historical_behavior=aggregator_data["historicalBehavior"]["trust"], 
                                 contextual_fit=aggregator_data["contextualFit"]["trust"], 
                                 third_party_validation=aggregator_data["thirdPartyValidation"]["trust"], 
                                 reputation=aggregator_data["reputation"]["trust"], 
                                 direct_trust=aggregator_data["directTrust"]["trust"], 
                                 provider=providerA)
    
    #capacityA = ResourceCapacity(name="Capacity_A", did_raw="did:example:456", performance={"throughput": [0.8,0.7], "bandwidth": [0.7,0.7]}, location=(46.05, 14.47), historical_behavior=0.8, contextual_fit=0.7, third_party_validation=0.6, reputation=0.65, direct_trust=0.8, provider=providerA)
    
    # AppProviderX is an application provider that will be trusted
    app_providerX = ApplicationProvider(name="AppProvider_X", did_raw="did:example:789", compliance=1, location=(46.05, 14.47), reputation=0.65, direct_trust=0.85)
    
    # App provider that will not be trusted
    bad_app_providerH = ApplicationProvider(name="AppProvider_H", did_raw="did:example:326", compliance=0.1, location=(46.05, 14.47), reputation=0.4, direct_trust=0.3)

    evaluator = TrustEvaluator(model='probabilistic') # 'deterministic' or 'probabilistic'
    stakeholders = [providerA, capacityA, app_providerX, bad_app_providerH]
    
    print("Initial Trust Scores and Evaluation:")
    for s in stakeholders:
        evaluator.compute_trust(s)
        print(f"{s.name}: {s.trust:.4f}")
        evaluator.trust_evaluation(s)
    
    trusted_stakeholders = evaluator.get_trusted_stakeholders()
    
    # Now we simmulate that there was registered a worst performance of CapacityA so we want to see a difference  in the trust value
    new_performance = {"throughput": [0.5,0.50], "bandwidth": [0.30,0.30]}
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
