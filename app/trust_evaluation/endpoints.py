
from app.models.schemas import StakeholderResponse

from fastapi import FastAPI, Depends, Response, status, HTTPException

evaluator_app = FastAPI()

@evaluator_app.get("/stakeholder/{stakeholder_id}", response_model=StakeholderResponse)
def get_stakeholder():
    pass
