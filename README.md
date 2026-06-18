# Intelligence Task Manager

## Shlomo Baruch Noyfeld


## `Description of the center`

### A task management system for an intelligence unit called ShadowNet that links tasks to the agents who will carry them out, and reports whether the task has been assigned to an agent, is in progress, has been completed successfully, failed, or has been canceled.

## `Folder structure`

#### intelligence-task-manager/
#### ├── database/
#### │ ├── db_connection.py
#### │ ├── agent_db.py
#### │ └── mission_db.py
#### ├── README.md
#### ├── requirements.txt
#### └── .gitignore

## `Table structure`

### `agents table`

|  `field`  | `type`  |  `Notes`  |
|---------|-------|---------|
|id|INT AUTO_INCREMENT PRIMARY KEY|UNIQUE|
|name|VARCHAR|Agent name|
|specialty|VARCHAR|Field of specialization|
|is_active|BOOLEAN|DEFAULT: TRUE|
|completed_missions|INT|DEFAULT: 0|
|failed_missions|INT|DEFAULT: 0|
|agent_rank|ENUM / VARCHAR|Only Junior/Senior/Commander|


### `missions table`

|  `field`  | `type`  |  `Notes`  |
|---------|-------|---------|
|id|INT AUTO_INCREMENT PRIMARY KEY|UNIQUE|
|title|VARCHAR|Mission title|
|description|TEXT|Detailed description|
|location|VARCHAR|Location|
|difficulty|INT|Only 1-10|
|importance|INT|Only 1-10|
|status|VARCHAR|DEFAULT: NEW|
|level_risk|VARCHAR|Automatically calculated—not coming from the user|
|assigned_agent_id|INT|NULL, until associated|


## Explanation of the methods

### class DB_connection 

|  `role`  | `method`  |
|----------|-----------|
|Returns an active connection to MySQL|get_connection()|
|Creates db_Intelligence if it does not exist|create_database()|
|Creates both tables if they do not exist|create_tables()|

### class AgentDB

|  `role`  | `method`  |
|----------|-----------|
|Creates a new agent and returns the agent object|create_agent(data)|
|Returns a list of all agents|get_all_agents()|
|Returns one agent by ID or NONE|get_agent_by_id(id)|
|Cannot change (UPDATE id for the entire row)|update_agent(id, data)|
|Sets agent inactive status|deactivate_agent(id)|
|Updates the number of tasks completed|increment_completed(id)|
|Updates the number of failed tasks|increment_failed(id)|
|Returns a dictionary with these keys: completed, failed, total, success_rate|get_agent_performance(id)|
|Returns the number of active agents|count_active_agents()|

### class MissionDB

|  `role`  | `method`  |
|----------|-----------|
|Creates a new task and returns the entire object|create_mission(data)|
|Returns all tasks|get_all_missions()|
|Returns one mission by ID or NONE|get_mission_by_id(id)|
|Assigning a task to an agent|assign_mission(m_id, a_id)|
|Used for any status change|update_mission_status(id, status)|
|Returns agent ASSIGNED/IN_PROGRESS tasks|get_open_missions_by_agent(id)|
|Total tasks|count_all_missions()|
|Counting by a certain status|count_by_status(status)|
|Open task counter|count_open_missions()|
|CRITICAL tasks counter|count_critical_missions()|
|The agent with the highest completed_missions|get_top_agent()|

## System rules

|  `num`  | `law`  |
|---------|--------|
|1|rank must be Commander / Senior / Junior — any other value throws an error|
|2|culty and importance must be between 1 and 10 - otherwise an error.|
|3|risk_level is calculated automatically when a task is created—the user does not submit it|
|4|An agent with is_active=False cannot accept tasks|
|5|An agent cannot have more than 3 open tasks (PROGRESS_IN / ASSIGNED) at the same time|
|6|If risk_level=CRITICAL — only an agent with the rank of Commander can accept the mission|
|7|Only a task with a status of NEW can be assigned. After assignment: status=ASSIGNED|
|8|Only a task with the ASSIGNED status can be started. After: status=IN_PROGRESS|
|9|Only a task can be completed. IN_PROGRESS and changed to completed or failed status|
|10|Only a task with a status of New or Assigned can be canceled - otherwise an error will occur|

## Endpoint List

### Agents endpoints

|  `Method`  | `Endpoint`  |  `Description`  |
|------------|-------------|-----------------|
|POST|agents/|Create a new agent|
|GET|agents/|All agents|
|GET|agents/{id}|Agent by id|
|PUT|agents/{id}|Update agent|
|PUT|agents/{id}/deactivate|Deactivate agent|
|GET|agents/{id}/performance|Agent performance|

### Missions endpoints

|  `Method`  | `Endpoint`  |  `Description`  |
|------------|-------------|-----------------|
|POST|missions/|Create a new mission|
|GET|missions/|All missions|
|GET|missions/{id}|Missions by id|
|PUT|missions/{id}/assign/{agent_id}|Agent association|
|PUT|missions/{id}/start|Starting a task|
|PUT|missions/{id}/complete|Successful completion|
|PUT|missions/{id}/fail|Ending in failure|
|PUT|missions/{id}/start|Cancel a task|

### Reports endpoints

|  `Method`  | `Endpoint`  |  `Description`  |
|------------|-------------|-----------------|
|GET|reports/summary|General system report|
|GET|reports/missions-by-status|Missions by status|
|GET|reports/top-agent|top_agent|



## `Running instructions`
#### docker run -d --name intelligence-mysql\
#### -e MYSQL_ROOT_PASSWORD=1234 \
#### -e MYSQL_DATABASE=Intelligence_db\
#### -p 3306:3306\
#### -d mysql:8

#### python -m venv venv
#### venv/Scripts/activate

#### pip install -r requirements.txt

#### pythom main.py
.