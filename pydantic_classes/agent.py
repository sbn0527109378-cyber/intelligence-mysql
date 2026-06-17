from pydantic import BaseModel


class Agent(BaseModel):
    name: str
    specialty: str
    is_active: bool
    completed_missions: int
    failed_missions: int
    agent_rank: str