import json
import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..db.models import Entity, Relationship
from .llm_router import llm_router
from .event_bus import event_bus

class WorldModelManager:
    def __init__(self):
        pass

    async def extract_and_store_graph(self, db: AsyncSession, context: str):
        """Uses LLM to extract entities and relationships from text."""
        await event_bus.publish("thought_stream", {
            "type": "thought",
            "content": f"Mapping contextual World Model graph...",
            "module": "WorldModel"
        })
        
        prompt = f"""
Extract exactly 2 entities and 1 relationship connecting them from this text.
Return ONLY valid JSON matching this schema:
{{
  "entities": [ {{"name": "...", "type": "..."}} ],
  "relationships": [ {{"source": "name1", "target": "name2", "relation": "..."}} ]
}}
Text: {context}
"""
        system = "You are the World Model ontology engine. Output strictly valid JSON."
        
        try:
            response = await llm_router.generate(prompt, system)
            
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
                
            graph = json.loads(response.strip())
            
            entity_map = {}
            for ent_data in graph.get("entities", []):
                ent = Entity(
                    id=f"ent_{uuid.uuid4().hex[:8]}",
                    name=ent_data.get("name", "Unknown"),
                    type=ent_data.get("type", "Concept"),
                    attributes="{}"
                )
                db.add(ent)
                entity_map[ent.name] = ent.id
                
            for rel_data in graph.get("relationships", []):
                src = entity_map.get(rel_data.get("source"))
                tgt = entity_map.get(rel_data.get("target"))
                if src and tgt:
                    rel = Relationship(
                        id=f"rel_{uuid.uuid4().hex[:8]}",
                        source_id=src,
                        target_id=tgt,
                        relation_type=rel_data.get("relation", "connected_to")
                    )
                    db.add(rel)
                    
            await db.commit()
            
            await event_bus.publish("thought_stream", {
                "type": "thought",
                "content": f"Extracted {len(entity_map)} entities into World Graph.",
                "module": "WorldModel"
            })
            
            return graph
        except Exception as e:
            print(f"World Model extraction failed: {e}")
            return {"entities": [], "relationships": []}

    async def retrieve_graph(self, db: AsyncSession):
        entities = (await db.execute(select(Entity))).scalars().all()
        relationships = (await db.execute(select(Relationship))).scalars().all()
        
        return {
            "entities": [{"id": e.id, "name": e.name, "type": e.type} for e in entities],
            "relationships": [{"source": r.source_id, "target": r.target_id, "relation": r.relation_type} for r in relationships]
        }

world_model = WorldModelManager()
