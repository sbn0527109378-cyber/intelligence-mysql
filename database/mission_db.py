from database import db_connection
from pydantic_classes import mission
from logs.logs import get_logger

logger = get_logger(__name__)

m = mission.Mission

class MissionDB:
    @staticmethod
    def create_mission(data: m):
        logger.info("User create a new mission")
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        risk = data.difficulty * 2 + data.importance
        if 0 <= risk < 10:
            risk_l = "LOW"
        elif 10 <= risk < 18:
            risk_l = "MEDIUM"
        elif 18 <= risk < 25:
            risk_l = "HIGH"
        elif risk >= 25:
            risk_l = "CRITICAL"
        if 0 > data.difficulty or data.difficulty > 10 or 0 > data.importance or data.importance > 10:
            raise KeyError
        logger.info("User creates a new mission")
        sql = "INSERT INTO missions (title, description, location, difficulty, importance," \
        "status, risk_level, assigned_agent_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (data.title, data.description, data.location, data.difficulty,
                  data.importance, data.status ,risk_l, data.assigned_agent_id)
        cursor.execute(sql, values)
        conn.commit()
        lastrow = cursor.lastrowid
        sql1 = "SELECT * FROM missions WHERE id = %s"
        value1 = lastrow,
        cursor.execute(sql1, value1)
        new_mission = cursor.fetchall()
        cursor.close()
        conn.close()
        logger.info("Mission created successfully")
        return new_mission
    
    @staticmethod
    def get_all_missions():
        logger.info("all mission")
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM missions"
        cursor.execute(sql)
        all_missions = cursor.fetchall()
        cursor.close()
        conn.close()
        logger.info("Calling all missions was successful")
        return all_missions
    
    @staticmethod
    def get_mission_by_id(id):
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM missions WHERE id = %s"
        value = id,
        cursor.execute(sql, value)
        mission_by_id = cursor.fetchone()
        cursor.close()
        conn.close()
        logger.info("get mission by id")
        return mission_by_id
        
    @staticmethod
    def assign_mission(m_id, a_id):
        logger.info("assign mission")
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT * FROM missions WHERE id = %s"
        values = m_id,
        cursor.execute(sql, values)
        missions_by_id = cursor.fetchone()
        if not missions_by_id:
            raise KeyError("Mission not found")
        if missions_by_id["status"] is not "NEW":
            raise ValueError("Mission not available")
        if missions_by_id["risk_level"] is "CRITICAL":
            raise ValueError("Only Commander can handle critical missions")

        sql1 = "SELECT * FROM agents WHERE id = %s"
        values1 = a_id,
        cursor.execute(sql1, values1)
        agent_by_id = cursor.fetchone()
        if not agent_by_id:
            raise KeyError("Agent not found")
        if agent_by_id["is_active"] == 0:
            raise ValueError("Agent is not active")

        logger.info("Task assignment")
        sql3 = "UPDATE missions SET assigned_agent_id = %s WHERE id = %s"
        values3 = (m_id, a_id)
        
        cursor.execute(sql3, values3)
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("The task was successfully assigned")
        return "The task was successfully assigned"

    @staticmethod
    def update_mission_status(id, status):
        logger.info("updates mission status")
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        logger.info("updates mission status")
        sql = "UPDATE missions SET status = %s WHERE id = %s"
        values = (status, id)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("The status was updated successfully")
        return "The status was updated successfully"

    @staticmethod
    def get_open_missions_by_agent(id):
        logger.info("get open missions by agent")
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM missions WHERE assigned_agent_id = %s AND status = %s OR status = %s"
        value = (id, "ASSIGNED", "IN_PROGRESS")
        cursor.execute(sql, value)
        missions_by_id = cursor.fetchall()
        cursor.close()
        conn.close()
        if missions_by_id:
            logger.info("get open missions by agent succeeded")
            return missions_by_id
        logger.info("get open missions by agent is empty")
        return []
    
    @staticmethod
    def count_all_missions():
        logger.info("all missions")
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM missions"
        cursor.execute(sql)
        amount_all_missions = cursor.fetchone()
        cursor.close()
        conn.close()
        logger.info("count all missions succeeded")
        return amount_all_missions[0]
    
    @staticmethod
    def count_by_status(status):
        logger.info("count by status")
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM missions WHERE status = %s"
        value = status,
        cursor.execute(sql, value)
        amount_missions_by_status = cursor.fetchone()
        cursor.close()
        conn.close()
        logger.info("count by status succeeded")
        return amount_missions_by_status[0]
    
    @staticmethod
    def count_open_missions():
        logger.info("count open missions")
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM missions WHERE status = %s OR status = %s OR status = %s"
        value = ("NEW", "ASSIGNED", "IN_PROGRESS")
        cursor.execute(sql, value)
        open_missions = cursor.fetchone()
        cursor.close()
        conn.close()
        if open_missions:
            logger.info("count open missions succeeded")
            return open_missions[0]
        logger.info("count open missions succeeded")
        return 0
    
    @staticmethod
    def count_critical_missions():
        logger.info("count critical missions")
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM missions WHERE risk_level = %s"
        value = "CRITICAL",
        cursor.execute(sql, value)
        critical_missions = cursor.fetchone()
        cursor.close()
        conn.close()
        logger.info("count critical missions succeeded")
        return critical_missions[0]

    @staticmethod
    def get_top_agent():
        logger.info("get top agent")
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT completed_missions FROM agents"
        cursor.execute(sql)
        all_completed_missions = cursor.fetchall()
        top = [complete_mission["completed_missions"] for complete_mission in all_completed_missions]
        top = max(top)
        sql1 = "SELECT * FROM agents WHERE completed_missions = %s"
        value1 = top,
        cursor.execute(sql1, value1)
        top_agent = cursor.fetchall()
        cursor.close()
        conn.close()
        logger.info("get top agent succeeded")
        return top_agent