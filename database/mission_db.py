from database import db_connection
from pydantic_classes import mission

m = mission.Mission

class MissionDB:
    @staticmethod
    def create_mission(data: m):
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        risk = data.difficulty * 2 + data.importance
        if 0 <= risk < 10:
            risk_l = "LOW"
        elif 10 <= risk < 18:
            risk_l = "MEDIUM"
        elif 18 <= risk < 25:
            risk_l = "HIGH"
        elif risk >= 25:
            risk_l = "CRITICAL"
        sql = "INSERT INTO missions (title, description, location, difficulty, importance," \
        "status,risk_level assigned_agent_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (data.title, data.description, data.location, data.difficulty,
                  data.importance, data.status,risk_l, data.assigned_agent_id)
        cursor.execute(sql, values)
        conn.commit()
        new_mission = cursor.lastrowid
        cursor.close()
        conn.close()
        return new_mission
    
    @staticmethod
    def get_all_missions():
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT title FROM missions"
        cursor.execute(sql)
        all_missions = cursor.fetchall()
        cursor.close()
        conn.close()
        return all_missions
    
    @staticmethod
    def get_mission_by_id(id):
        try:
            conn = db_connection.get_connection()
            cursor = conn.cursor()
            sql = "SELECT * FROM missions WHERE id = %s"
            value = id,
            cursor.execute(sql, value)
            mission_by_id = cursor.fetchone()
            cursor.close()
            conn.close()
            return mission_by_id
        except Exception:
            return None
        
    @staticmethod
    def assign_mission(m_id, a_id):
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        
        sql1 = "SELECT * FROM missions WHERE assigned_agent_id = %s AND status = %s OR status = %s"
        values1 = (a_id, "ASSIGNED", "IN_PROGRESS")
        
        cursor.execute(sql1, values1)
        missions_by_id = cursor.fetchall()
        
        if len(missions_by_id) >= 3:
            return f"{a_id} has too many open tasks"
        
        sql2 = "SELECT is_active FROM agents WHERE id = %s"
        value2 = a_id,
        
        cursor.execute(sql2, value2)
        is_active = cursor.fetchone()
        
        if is_active == False:
            return f"{a_id} is not active"
        
        sql3 = "UPDATE missions SET assigned_agent_id = %s WHERE id = %s"
        values3 = (m_id, a_id)
        
        cursor.execute(sql3, values3)
        conn.commit()
        cursor.close()
        conn.close()
        return "The task was successfully assigned"

    @staticmethod
    def update_mission_status(id, status):
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "UPDATE missions SET status = %s WHERE id = %s"
        values = (status, id)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return "The status was updated successfully"

    @staticmethod
    def get_open_missions_by_agent(id):
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM missions WHERE assigned_agent_id = %s AND status = %s OR status = %s"
        value = (id, "ASSIGNED", "IN_PROGRESS")
        cursor.execute(sql, value)
        missions_by_id = cursor.fetchall()
        cursor.close()
        conn.close()
        if missions_by_id:
            return missions_by_id
        return []
    
    @staticmethod
    def count_all_missions():
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM missions"
        cursor.execute(sql)
        amount_all_missions = cursor.fetchone()
        cursor.close()
        conn.close()
        return amount_all_missions[0]
    
    @staticmethod
    def count_by_status(status):
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT COUNT(%s) FROM missions"
        value = status,
        cursor.execute(sql, value)
        amount_missions_by_status = cursor.fetchone()
        cursor.close()
        conn.close()
        return amount_missions_by_status[0]
    
    @staticmethod
    def count_open_missions():
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM missions WHERE status = %s OR status = %s OR status = %s"
        value = ("NEW", "ASSIGNED", "IN_PROGRESS")
        cursor.execute(sql, value)
        open_missions = cursor.fetchall()
        cursor.close()
        conn.close()
        if open_missions:
            return open_missions
        return []
    
    @staticmethod
    def count_critical_missions():
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM missions WHERE risk_level = %s"
        value = "CRITICAL",
        cursor.execute(sql, value)
        critical_missions = cursor.fetchone()
        cursor.close()
        conn.close()
        return critical_missions[0]

    @staticmethod
    def get_top_agent():
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT completed_missions FROM agents"
        cursor.execute(sql)
        all_completed_missions = cursor.fetchall()
        top = max(all_completed_missions)
        sql1 = "SELECT * FROM agents WHERE completed_missions = %s"
        value1 = top,
        cursor.execute(sql1, value1)
        top_agent = cursor.fetchall()
        cursor.close()
        conn.close()
        return top_agent