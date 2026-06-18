from fastapi import APIRouter
from database.agent_db import AgentDB
from pydantic_classes import agent

ag = agent.Agent

a = AgentDB()
router = APIRouter()

@router.post("/")
def create_agent(data: ag):
    return a.create_agent(data)

@router.get("/")
def all_agents():
    return a.get_all_agents()

@router.get("/{id}")
def agent_by_id(id: int):
    return a.get_agent_by_id(id)

@router.put("/{id}")
def update_by_id(id: int, data: ag):
    return a.update_agent(id, data)

@router.put("/{id}/deactivate")
def deactivate_agent(id: int):
    return a.deactivate_agent(id)

@router.get("/{id}/performance")
def agent_performances(id: int):
    return a.get_agent_performance(id)