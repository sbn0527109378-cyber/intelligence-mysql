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
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


@router.get("/")
def all_missions():
    return m.get_all_missions()

@router.get("/{id}")
def mission_by_id(id: int):
    try:
        return m.get_mission_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


@router.put("/{id}/assign/{agent_id}")
def assign_mission(id: int, agent_id: int):
    try:
        return m.assign_mission(id, agent_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


@router.put("/{id}/start")
def start_mission(id: int):
    try:
        return m.update_mission_status(id, "IN_PROGRESS")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


@router.put("/{id}/complete")
def complete_mission(id: int):
    try:
        return m.update_mission_status(id, "COMPLETED")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


@router.put("/{id}/fail")
def fail_mission(id: int):
    try:
        return m.update_mission_status(id, "FAILED")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


@router.put("/{id}/cancel")
def cancel_mission(id: int):
    try:
        return m.update_mission_status(id, "CANCELLED")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")