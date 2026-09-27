import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.middleware.cors import CORSMiddleware
from ..db import models, database
from ..kernel.planner import planner

app = FastAPI(title="ECOS Kernel API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    # create db tables async
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.get("/")
def read_root():
    return {"message": "ECOS Kernel Online (Production Grade)"}

@app.get("/api/goals")
async def get_goals(db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.Goal))
    return result.scalars().all()

@app.post("/api/goals")
async def create_goal(goal: dict, db: AsyncSession = Depends(database.get_db)):
    # 1. Use the true LLM to decompose the goal
    generated_plan = await planner.decompose(goal.get("title"))
    
    # 2. Extract Cognitive Context (Memory and World Model)
    import asyncio
    asyncio.create_task(memory_manager.extract_and_store(db, goal.get("title"), source="Goal"))
    asyncio.create_task(world_model.extract_and_store_graph(db, goal.get("title")))
    
    # 3. Store persistently
    new_goal = models.Goal(
        id=goal.get("id", f"goal_{uuid.uuid4().hex[:8]}"),
        title=goal.get("title"),
        priority=goal.get("priority", "Medium"),
        project_id=goal.get("project_id"),
        plan=generated_plan
    )
    db.add(new_goal)
    await db.commit()
    await db.refresh(new_goal)
    return new_goal

from ..kernel.event_bus import event_bus
from ..kernel.llm_router import llm_router
from ..kernel.memory import memory_manager
from ..kernel.world_model import world_model
from ..kernel.simulator import simulator
from ..kernel.knowledge import knowledge_manager
import uuid

@app.get("/api/knowledge")
async def search_knowledge(q: str = "", db: AsyncSession = Depends(database.get_db)):
    results = await knowledge_manager.search(db, q)
    return results

@app.post("/api/knowledge")
async def add_knowledge(payload: dict, db: AsyncSession = Depends(database.get_db)):
    res = await knowledge_manager.add_document(db, payload.get("title", "Untitled"), payload.get("content", ""))
    return res

@app.get("/api/projects")
async def get_projects(db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.Project))
    return result.scalars().all()

@app.post("/api/projects")
async def create_project(payload: dict, db: AsyncSession = Depends(database.get_db)):
    proj = models.Project(
        id=f"proj_{uuid.uuid4().hex[:8]}",
        name=payload.get("name", "New Project"),
        description=payload.get("description", "")
    )
    db.add(proj)
    await db.commit()
    await db.refresh(proj)
    return proj

@app.get("/api/agents")
async def get_agents(db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.Agent))
    return result.scalars().all()

@app.post("/api/agents")
async def create_agent(payload: dict, db: AsyncSession = Depends(database.get_db)):
    agent = models.Agent(
        id=f"agent_{uuid.uuid4().hex[:8]}",
        name=payload.get("name", "New Agent"),
        role=payload.get("role", "Worker"),
        capabilities=payload.get("capabilities", "[]"),
        status=payload.get("status", "Idle")
    )
    db.add(agent)
    await db.commit()
    await db.refresh(agent)
    return agent

@app.get("/api/skills")
async def get_skills(db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.Skill))
    return result.scalars().all()

@app.post("/api/skills")
async def create_skill(payload: dict, db: AsyncSession = Depends(database.get_db)):
    skill = models.Skill(
        id=f"skill_{uuid.uuid4().hex[:8]}",
        name=payload.get("name", "new_skill"),
        description=payload.get("description", "A cognitive skill"),
        endpoint_mock=payload.get("endpoint_mock", "")
    )
    db.add(skill)
    await db.commit()
    await db.refresh(skill)
    return skill

@app.get("/api/memory")
async def get_memories(db: AsyncSession = Depends(database.get_db)):
    memories = await memory_manager.retrieve(db)
    return memories

@app.get("/api/world")
async def get_world(db: AsyncSession = Depends(database.get_db)):
    graph = await world_model.retrieve_graph(db)
    return graph

@app.post("/api/simulate")
async def simulate_plan(payload: dict, db: AsyncSession = Depends(database.get_db)):
    plan = payload.get("plan", [])
    goal_title = payload.get("goal_title", "")
    result = await simulator.simulate(db, plan, goal_title)
    return result

# Chat API for legacy interface
@app.post("/api/chat")
async def chat_interaction(payload: dict, db: AsyncSession = Depends(database.get_db)):
    user_msg = payload.get("message", "")
    
    # Background extraction (Memory and World Model)
    asyncio.create_task(memory_manager.extract_and_store(db, user_msg, source="Chat"))
    asyncio.create_task(world_model.extract_and_store_graph(db, user_msg))
    
    system_prompt = "You are ELIZA. The user is talking to you through a legacy chat interface. Be helpful, concise, and occasionally remind them to use the Workspace for complex multi-step goals."
    try:
        response = await llm_router.generate(user_msg, system_prompt)
        return {"response": response}
    except Exception as e:
        return {"response": f"System Error: {e}"}

# WebSocket for live Cognitive Trace streaming
@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    queue = event_bus.subscribe("thought_stream")
    try:
        while True:
            # Wait for a real event from the Cognitive Kernel
            trace_event = await queue.get()
            await websocket.send_text(json.dumps(trace_event))
    except WebSocketDisconnect:
        event_bus.unsubscribe("thought_stream", queue)
        print("Client disconnected")
