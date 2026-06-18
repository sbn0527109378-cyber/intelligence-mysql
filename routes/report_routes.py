from fastapi import APIRouter
from database.mission_db import MissionDB
from database.agent_db import AgentDB
from pydantic_classes import agent, mission

ag = agent.Agent
miss = mission.Mission

m = MissionDB()
a = AgentDB()

router = APIRouter()
@router.get("/summary")
def General_system_report():
    return {"active_agents_count": a.count_active_agents(),
            "total_missions": m.count_all_missions(),
            "open_missions": m.count_open_missions(),
            "completed_missions": m.count_by_status("COMPLETED"),
            "failed_missions": m.count_by_status("FAILED"),
            "critical_missions": m.count_critical_missions()
            }

@router.get("/missions-by-status")
def missions_by_status():
    return {
            "open": m.count_open_missions(),
            "in_progress": m.count_by_status("IN_PROGRESS"),
            "completed": m.count_by_status("COMPLETED"),
            "failed": m.count_by_status("FAILED"),
            "cancel": m.count_by_status("CANCELLED")
            }

@router.get("/top-agent")
def top_agent():
    return m.get_top_agent()