from pydantic import BaseModel


class Mission(BaseModel):
    title: str
    description: str
    location: str
    difficulty: int
    importance: int
    status: str
    risk_level: str
    assigned_agent_id: int