from fastapi import FastAPI
import uvicorn
from database import db_connection
from routes import agent_routes, mission_routes, report_routes


app = FastAPI()
app.include_router(agent_routes.router, prefix="/agents")
app.include_router(mission_routes.router, prefix="/missions")
app.include_router(report_routes.router, prefix="/reports")




if __name__ == "__main__":
    db_connection.create_database()
    db_connection.create_tables()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)