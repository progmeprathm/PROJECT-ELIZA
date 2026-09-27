import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from ecos.db.database import AsyncSessionLocal
from ecos.kernel.world_model import world_model
from ecos.db import models, database

async def init_db():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

async def test():
    await init_db()
    async with AsyncSessionLocal() as db:
        context = """
        User is trying to build a scalable web application. They need a fast backend (Goal). 
        To do this, they plan to use FastAPI (Skill), but they are struggling with async DB connections (Obstacle).
        They believe (Belief) that SQLAlchemy 2.0 is the best ORM, but they have a constraint (Constraint) that it must run on a tiny AWS EC2 instance.
        Yesterday, the server crashed due to OOM (Event).
        The primary entity here is the WebApp (Entity).
        """
        print("Extracting...")
        graph = await world_model.extract_and_store_graph(db, context)
        print("Done!")
        import json
        print(json.dumps(graph, indent=2))

if __name__ == "__main__":
    asyncio.run(test())
