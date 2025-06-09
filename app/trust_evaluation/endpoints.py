from fastapi import FastAPI, Depends, Response, status, HTTPException
from sqlmodel import select
from datetime import datetime
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

from app.models.schemas import StakeholderResponse, AllStakeholdersResponse
from app.utils.helpers import StakeholderType
from app.utils.database import get_session, Session, SessionDep
from app.models.sql_models import Stakeholder
from app.models.stakeholder import ResourceProvider, ResourceCapacity, ApplicationProvider
from app.trust_evaluation.trust_evaluator import TrustEvaluator
from app.models.attributes import TrustCalcModel

evaluator_app = FastAPI()

evaluator_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # or use ["*"] to allow all origins (not recommended in production)
    allow_credentials=True,
    allow_methods=["*"],              # Allows all HTTP methods: GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],              # Allows all headers
)


@evaluator_app.get("/stakeholder/{stakeholder_did}", response_model=StakeholderResponse)
def get_stakeholder(stakeholder_did: str, session: SessionDep):
    stakeholder_model = session.get(Stakeholder, stakeholder_did)

    # Prepare a local TrustEvaluator instance
    evaluator_probabilistic = TrustEvaluator(model=TrustCalcModel.PROBABILISTIC)
    evaluator_deterministic = TrustEvaluator(model=TrustCalcModel.DETERMINISTIC)

    # If resource/resource capacity, evaluate provider first and add to trusted list
    if stakeholder_model.type == StakeholderType.RESOURCE_PROVIDER or stakeholder_model.type == StakeholderType.CAPACITY_PROVIDER:
        stakeholder = ResourceProvider(name=stakeholder_model.name, did_raw=stakeholder_did)
    elif stakeholder_model.type == StakeholderType.RESOURCE_CAPACITY or stakeholder_model.type == StakeholderType.RESOURCE:
        provider = session.get(Stakeholder, stakeholder_model.provider)
        provider_obj = ResourceProvider(name=provider.name, did_raw=provider.did)
        # Evaluate provider and add to trusted list if trusted
        evaluator_probabilistic.compute_trust(provider_obj)
        evaluator_probabilistic.trust_evaluation(provider_obj)
        evaluator_deterministic.compute_trust(provider_obj)
        evaluator_deterministic.trust_evaluation(provider_obj)
        stakeholder = ResourceCapacity(name=stakeholder_model.name, did_raw=stakeholder_did, provider=provider_obj)
    elif stakeholder_model.type == StakeholderType.APPLICATION_PROVIDER:
        stakeholder = ApplicationProvider(name=stakeholder_model.name, did_raw=stakeholder_did)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect stakeholder type."
        )

    evaluator_probabilistic.compute_trust(stakeholder)
    evaluator_probabilistic.trust_evaluation(stakeholder)
    probabilistic_trust = round(stakeholder.trust * 100)

    evaluator_deterministic.compute_trust(stakeholder)
    evaluator_deterministic.trust_evaluation(stakeholder)
    deterministic_trust = round(stakeholder.trust * 100)

    return StakeholderResponse(
        did=stakeholder.did.raw,
        name=stakeholder.name,
        created_at=stakeholder_model.created_at,
        probabilistic_trust=probabilistic_trust,
        deterministic_trust=deterministic_trust
    )


@evaluator_app.get("/stakeholders", response_model=AllStakeholdersResponse)
def get_all_stakeholders(session: SessionDep):
    all_stakeholders_model = session.exec(
        select(Stakeholder)
    ).all()

    # Sort: providers first, then resource capacities/resources, then others
    # def sort_key(stakeholder_model):
    #     if stakeholder_model.type in [StakeholderType.RESOURCE_PROVIDER, StakeholderType.CAPACITY_PROVIDER]:
    #         return 0
    #     elif stakeholder_model.type in [StakeholderType.RESOURCE_CAPACITY, StakeholderType.RESOURCE]:
    #         return 1
    #     else:
    #         return 2
    # all_stakeholders_model.sort(key=sort_key)

    print(all_stakeholders_model)

    return AllStakeholdersResponse(
        stakeholders=[
            get_stakeholder(stakeholder_model.did, session)
            for stakeholder_model in all_stakeholders_model
        ]
    )

@evaluator_app.post("/stakeholder/{stakeholder_did}", response_model=StakeholderResponse)
def insert_new_stakeholder(
        session: SessionDep,
        stakeholder_did: str,
        stakeholder_type: int,
        name: str,
        metrics_url: Optional[str] = None,
        provider: Optional[str] = None
):
    # Use valid Slovenian coordinates
    slovenia_lat = 46.0
    slovenia_lon = 15.0
    new_stakeholder = Stakeholder(
        did=stakeholder_did,
        type=stakeholder_type,
        name=name,
        provider=provider,
        metrics_url=metrics_url,
        identity="vc",
        reputation=0.5,
        direct_trust=0.6,
        compliance=0.7,
        historical_behavior=0.3,
        location_lat=slovenia_lat,
        location_lon=slovenia_lon,
        contextual_fit=0.2,
        third_party_validation=0.9,
        created_at=datetime.now()
    )
    session.add(new_stakeholder)
    session.commit()
    session.refresh(new_stakeholder)

    return get_stakeholder(stakeholder_did, session)


@evaluator_app.delete("/stakeholder/{stakeholder_did}")
def remove_stakeholder(session: SessionDep, stakeholder_did: str):
    target_stakeholder = session.exec(
        select(Stakeholder)
        .where(Stakeholder.did == stakeholder_did)
    ).one_or_none()

    if target_stakeholder is None:
        raise HTTPException(status_code=404, detail="No such stakeholder.")
    print(f"Removing stakeholder Did: {target_stakeholder.did}, Name: {target_stakeholder.name}")
    if target_stakeholder.type == StakeholderType.RESOURCE_PROVIDER or target_stakeholder.type == StakeholderType.CAPACITY_PROVIDER:
        # we need to remove the resources as well but remember some reources have null providers
        resources = session.exec(
            select(Stakeholder).where(Stakeholder.provider == target_stakeholder.did)
        ).all()
        for resource in resources:
            print(f"Removing resource Did: {resource.did}, Name: {resource.name}")
            session.delete(resource)
    session.delete(target_stakeholder)
    session.commit()

    return {"ok": True}
