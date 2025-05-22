
from typing import List

from pydantic import BaseModel

class StakeholderResponse(BaseModel):
    did: str
    name: str
    probabilistic_trust: float
    deterministic_trust: float

class AllStakeholdersResponse(BaseModel):
    stakeholders: List[StakeholderResponse]