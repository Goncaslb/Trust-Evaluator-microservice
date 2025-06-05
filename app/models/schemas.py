
from typing import List
from datetime import datetime

from pydantic import BaseModel

class StakeholderResponse(BaseModel):
    did: str
    name: str
    created_at: datetime
    probabilistic_trust: float
    deterministic_trust: float

class AllStakeholdersResponse(BaseModel):
    stakeholders: List[StakeholderResponse]