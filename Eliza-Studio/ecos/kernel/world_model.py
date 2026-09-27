import json
import uuid
import datetime
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
        """Uses LLM to extract rich cognitive graph entities and relationships from text."""
        await event_bus.publish("thought_stream", {
            "type": "thought",
            "content": f"Extracting Tier 3.0 Cognitive State Graph...",
            "module": "WorldModel"
        })
        
        prompt = f"""
Extract a rich cognitive graph from the text below.
Identify all relevant nodes. A node MUST have one of the following types: 
'Entity', 'Goal', 'Skill', 'Obstacle', 'Belief', 'Constraint', 'Event'.
Also extract relationships between these nodes (e.g., 'BLOCKS', 'REQUIRES', 'ENABLES', 'BELIEVES').

For each node, extract dynamic attributes such as:
- 'confidence' (float 0.0-1.0)
- 'progress' (string description)
- 'status' (string)
- 'last_updated' (current date/time or inferred)

Return ONLY valid JSON matching this schema:
{{
  "entities": [ 
    {{
      "name": "...", 
      "type": "Goal", 
      "attributes": {{"confidence": 0.9, "progress": "Started", "status": "active"}}
    }} 
  ],
  "relationships": [ {{"source": "name1", "target": "name2", "relation": "..."}} ]
}}
Text: {context}
"""
        system = "You are the ECOS Tier 3.0 World Model ontology engine. Output strictly valid JSON."
        
        try:
            response = await llm_router.generate(prompt, system)
            
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
                
            graph = json.loads(response.strip())
            
            entity_map = {}
            for ent_data in graph.get("entities", []):
                # Ensure last_updated is present
                attrs = ent_data.get("attributes", {})
                if "last_updated" not in attrs:
                    attrs["last_updated"] = datetime.datetime.now().isoformat()
                    
                ent = Entity(
                    id=f"ent_{uuid.uuid4().hex[:8]}",
                    name=ent_data.get("name", "Unknown"),
                    type=ent_data.get("type", "Concept"),
                    attributes=json.dumps(attrs)
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
                "content": f"Persisted {len(entity_map)} rich nodes into World Graph.",
                "module": "WorldModel"
            })
            
            return graph
        except Exception as e:
            print(f"World Model extraction failed: {e}")
            return {"entities": [], "relationships": []}

    async def retrieve_graph(self, db: AsyncSession):
        entities = (await db.execute(select(Entity))).scalars().all()
        relationships = (await db.execute(select(Relationship))).scalars().all()
        
        res_entities = []
        for e in entities:
            try:
                attrs = json.loads(e.attributes) if e.attributes else {}
            except:
                attrs = {}
            res_entities.append({"id": e.id, "name": e.name, "type": e.type, "attributes": attrs})
            
        return {
            "entities": res_entities,
            "relationships": [{"source": r.source_id, "target": r.target_id, "relation": r.relation_type} for r in relationships]
        }

world_model = WorldModelManager()
