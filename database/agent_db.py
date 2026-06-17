from database import db_connection
from pydantic_classes import agent

a = agent.Agent

class AgentDB:
    def create_agent(data: a):
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO agents (name, specialty, is_active," \
        "completed_missions, failed_missions, agent_rank) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (data.name, data.specialty, data.is_active, data.completed_missions, data.failed_missions, data.agent_rank)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return "agent created successfully"
    
    def get_all_agents():
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT name FROM agents"
        cursor.execute(sql)
        all_agents = cursor.fetchall()
        cursor.close()
        conn.close()
        return all_agents
    
    def get_agent_by_id(id):
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM agents WHERE ID = %s"
        value = id,
        cursor.execute(sql, value)
        agent_by_id = cursor.fetchone()
        cursor.close()
        conn.close()
        return agent_by_id
    
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

    def deactivate_agent(id):
        pass