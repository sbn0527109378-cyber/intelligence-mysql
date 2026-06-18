import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234",
        database="Intelligence_db"
    )

def create_database():
    conn = get_connection()
    cursor = conn.cursor()
    sql = "CREATE DATABASE IF NOT EXISTS Intelligence_db"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    sql = """CREATE TABLE IF NOT EXISTS agents(
    id                  INT AUTO_INCREMENT PRIMARY KEY          UNIQUE,
    name                VARCHAR(50),
    specialty           VARCHAR(100),
    is_active           BOOLEAN                                 DEFAULT TRUE, 
    completed_missions  INT                                     DEFAULT 0,
    failed_missions     INT                                     DEFAULT 0,
    agent_rank          ENUM("Junior", "Senior", "Commander")
    )"""
    cursor.execute(sql)
    
    sql2 = """CREATE TABLE IF NOT EXISTS missions(
    id                  INT AUTO_INCREMENT PRIMARY KEY          UNIQUE,
    title               VARCHAR(100),
    description         TEXT,
    location            VARCHAR(100),
    difficulty          INT,
    importance          INT,
    status              VARCHAR(100)                            DEFAULT "NEW",
    risk_level          VARCHAR(100),
    assigned_agent_id   INT                                     DEFAULT NULL
    )"""
    cursor.execute(sql2)
    conn.commit()
    cursor.close()
    conn.close()