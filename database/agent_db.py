from database import db_connection
from pydantic_classes import agent

a = agent.Agent

class AgentDB:
    @staticmethod
    def create_agent(data: a):
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO agents (name, specialty, is_active," \
        "completed_missions, failed_missions, agent_rank) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (data.name, data.specialty, data.is_active, data.completed_missions, data.failed_missions, data.agent_rank)
        cursor.execute(sql, values)
        conn.commit()
        new_agent = cursor.lastrowid
        cursor.close()
        conn.close()
        return new_agent
    
    @staticmethod
    def get_all_agents():
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT name FROM agents"
        cursor.execute(sql)
        all_agents = cursor.fetchall()
        cursor.close()
        conn.close()
        return all_agents
    
    @staticmethod
    def get_agent_by_id(id):
        try:
            conn = db_connection.get_connection()
            cursor = conn.cursor()
            sql = "SELECT * FROM agents WHERE ID = %s"
            value = id,
            cursor.execute(sql, value)
            agent_by_id = cursor.fetchone()
            cursor.close()
            conn.close()
            return agent_by_id
        except Exception:
            return None

    @staticmethod
    def update_agent(id, data: a):
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "UPDATE agents SET name = %s, specialty = %s, is_active = %s," \
        "completed_missions = %s,failed_missions = %s, agent_rank = %s WHERE ID = %s"
        values = (data.name, data.specialty, data.is_active, data.completed_missions, data.failed_missions, data.agent_rank, id)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return "agent updated successfully"

    @staticmethod
    def deactivate_agent(id):
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "UPDATE agents SET is_active = FALSE WHERE id = %s"
        value = id,
        cursor.execute(sql, value)
        conn.commit()
        cursor.close()
        conn.close()
        return "agent updated successfully"
    
    @staticmethod
    def increment_completed(id):
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT completed_missions FROM agents WHERE id = %s"
        value = id,
        cursor.execute(sql, value)
        tasks_completed = cursor.fetchone()
        sql1 = "UPDATE agents SET completed_missions = %s WHERE id = %s"
        value1 = (tasks_completed[0] + 1, id)
        cursor.execute(sql1, value1)
        conn.commit()
        cursor.close()
        conn.close()
        return "tasks completed updated successfully"
    
    @staticmethod
    def increment_failed(id):
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT failed_missions FROM agents WHERE id = %s"
        value = id,
        cursor.execute(sql, value)
        tasks_failed = cursor.fetchone()
        sql1 = "UPDATE agents SET failed_missions = %s WHERE id = %s"
        value1 = (tasks_failed[0] + 1, id)
        cursor.execute(sql1, value1)
        conn.commit()
        cursor.close()
        conn.close()
        return "tasks failed updated successfully"
    
    @staticmethod
    def get_agent_performance(id):
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT completed_missions FROM agents WHERE id = %s"
        value = id,
        cursor.execute(sql, value)
        tasks_completed = cursor.fetchone()
        sql1 = "SELECT failed_missions FROM agents WHERE id = %s"
        value1 = id,
        cursor.execute(sql1, value1)
        tasks_failed = cursor.fetchone()
        total_tasks = tasks_completed[0] + tasks_failed[0]
        return {"completed": tasks_completed[0], "failed": tasks_failed[0],
                "total": total_tasks, "success_rate": 100 / total_tasks * tasks_completed}
    
    @staticmethod
    def agents_active_count():
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT COUNT(is_active) FROM agents"
        cursor.execute(sql)
        sum_active_agents = cursor.fetchone()
        cursor.close()
        conn.close()
        return sum_active_agents