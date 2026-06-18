from fastapi import APIRouter, HTTPException
from database.agent_db import AgentDB
from pydantic_classes import agent

ag = agent.Agent

a = AgentDB()
router = APIRouter()

@router.post("/")
def create_agent(data: ag):
    try:
        return a.create_agent(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")

@router.get("/")
def all_agents():
    return a.get_all_agents()

@router.get("/{id}")
def agent_by_id(id: int):
    try:
        return a.get_agent_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


@router.put("/{id}")
def update_by_id(id: int, data: ag):
    try:
        return a.update_agent(id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


@router.put("/{id}/deactivate")
def deactivate_agent(id: int):
    try:
        return a.deactivate_agent(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


@router.get("/{id}/performance")
def agent_performances(id: int):
    try:
        return a.get_agent_performance(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
