from fastapi import APIRouter, HTTPException
from database.mission_db import MissionDB
from pydantic_classes import mission

miss = mission.Mission

m = MissionDB()
router = APIRouter()

@router.post("/")
def create_missions(data: miss):
    try:
        return m.create_mission(data)
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"number must be between 0-10")

@router.get("/")
def all_missions():
    return m.get_all_missions()

@router.get("/{id}")
def mission_by_id(id: int):
    return m.get_mission_by_id(id)

@router.put("/{id}/assign/{agent_id}")
def assign_mission(id: int, agent_id: int):
    return m.assign_mission(id, agent_id)

@router.put("/{id}/start")
def start_mission(id: int):
    return m.update_mission_status(id, "IN_PROGRESS")

@router.put("/{id}/complete")
def complete_mission(id: int):
    return m.update_mission_status(id, "COMPLETED")

@router.put("/{id}/fail")
def fail_mission(id: int):
    return m.update_mission_status(id, "FAILED")

@router.put("/{id}/cancel")
def cancel_mission(id: int):
    return m.update_mission_status(id, "CANCELLED")