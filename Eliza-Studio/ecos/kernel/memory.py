import json
import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..db.models import MemoryFragment
from .llm_router import llm_router
from .event_bus import event_bus

class MemoryManager:
    def __init__(self):
        pass

    async def extract_and_store(self, db: AsyncSession, context: str, source: str = "Chat"):
        """Uses LLM to extract beliefs and facts from text, then stores them."""
        await event_bus.publish("thought_stream", {
            "type": "thought",
            "content": f"Extracting cognitive fragments from {source}...",
            "module": "Memory"
        })
        
        prompt = f"Extract exactly 2 core facts or user beliefs from the following text. Return ONLY a JSON array of strings.\nText: {context}"
        system = "You are the Memory module. Output strictly valid JSON."
        
        try:
            response = await llm_router.generate(prompt, system)
            # Naive parse
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
                
            facts = json.loads(response.strip())
            
            for fact in facts:
                frag = MemoryFragment(
                    id=f"mem_{uuid.uuid4().hex[:8]}",
                    content=fact,
                    tier="Working",
                    confidence=0.9,
                    source=source
                )
                db.add(frag)
                
            await db.commit()
            
            await event_bus.publish("thought_stream", {
                "type": "thought",
                "content": f"Stored {len(facts)} memory fragments.",
                "module": "Memory"
            })
            
            return facts
        except Exception as e:
            print(f"Memory extraction failed: {e}")
            return []

    async def retrieve(self, db: AsyncSession, tier: str = None, limit: int = 20) -> List[MemoryFragment]:
        query = select(MemoryFragment)
        if tier:
            query = query.filter(MemoryFragment.tier == tier)
        result = await db.execute(query.limit(limit))
        return result.scalars().all()

memory_manager = MemoryManager()
