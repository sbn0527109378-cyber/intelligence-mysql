from database import db_connection
from logs.logs import get_logger

logger = get_logger(__name__)

class AgentDB:
    @staticmethod
    def create_agent(data):
        logger.info("User create a new agent")
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        logger.info("User creates a new agent")
        sql = "INSERT INTO agents (name, specialty, is_active," \
        "completed_missions, failed_missions, agent_rank) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (data.name, data.specialty, data.is_active, data.completed_missions, data.failed_missions, data.agent_rank)
        cursor.execute(sql, values)
        conn.commit()
        lastrow = cursor.lastrowid
        sql1 = "SELECT * FROM agents WHERE id = %s"
        value1 = lastrow,
        cursor.execute(sql1, value1)
        new_agent = cursor.fetchall()
        cursor.close()
        conn.close()
        logger.info("Agent created successfully")
        return new_agent
    
    @staticmethod
    def get_all_agents():
        logger.info("all agents")
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM agents"
        cursor.execute(sql)
        all_agents = cursor.fetchall()
        cursor.close()
        conn.close()
        logger.info("Calling all agents was successful")
        return all_agents
    
    @staticmethod
    def get_agent_by_id(id):
        logger.info("get agent by id")
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM agents WHERE id = %s"
        value = id,
        cursor.execute(sql, value)
        agent_by_id = cursor.fetchone()
        cursor.close()
        conn.close()
        logger.info("get agent by id was successful")
        return agent_by_id

    @staticmethod
    def update_agent(id, data):
        logger.info("User wants to update agent")
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        logger.info("User updates agent")
        sql = "UPDATE agents SET name = %s, specialty = %s, is_active = %s," \
        "completed_missions = %s,failed_missions = %s, agent_rank = %s WHERE ID = %s"
        values = (data.name, data.specialty, data.is_active, data.completed_missions, data.failed_missions, data.agent_rank, id)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("agent updated successfully")
        return "agent updated successfully"

    @staticmethod
    def deactivate_agent(id):
        logger.info("User wants to deactivate the agent.")
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        logger.info("Makes the agent deactivate")
        sql = "UPDATE agents SET is_active = FALSE WHERE id = %s"
        value = id,
        cursor.execute(sql, value)
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("deactivate updated successfully")
        return "deactivate updated successfully"
    
    @staticmethod
    def increment_completed(id):
        logger.info("The function performs increment completed")
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT completed_missions FROM agents WHERE id = %s"
        value = id,
        cursor.execute(sql, value)
        tasks_completed = cursor.fetchone()
        logger.info("increment completing")
        sql1 = "UPDATE agents SET completed_missions = %s WHERE id = %s"
        value1 = (tasks_completed[0] + 1, id)
        cursor.execute(sql1, value1)
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("tasks completed updated successfully")
        return "tasks completed updated successfully"
    
    @staticmethod
    def increment_failed(id):
        logger.info("The function performs increment failed")
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT failed_missions FROM agents WHERE id = %s"
        value = id,
        cursor.execute(sql, value)
        tasks_failed = cursor.fetchone()
        logger.info("increment faileding")
        sql1 = "UPDATE agents SET failed_missions = %s WHERE id = %s"
        value1 = (tasks_failed[0] + 1, id)
        cursor.execute(sql1, value1)
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("tasks failed updated successfully")
        return "tasks failed updated successfully"
    
    @staticmethod
    def get_agent_performance(id):
        logger.info("get agent performance")
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
        logger.info("agent_performance display succeeded")
        return {"completed": tasks_completed[0], "failed": tasks_failed[0],
                "total": total_tasks, "success_rate": 100 / total_tasks * tasks_completed}
    
    @staticmethod
    def count_active_agents():
        logger.info("count active agents")
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT COUNT(is_active) FROM agents"
        cursor.execute(sql)
        sum_active_agents = cursor.fetchone()
        cursor.close()
        conn.close()
        logger.info("count active agents display succeeded")
        return sum_active_agents[0]