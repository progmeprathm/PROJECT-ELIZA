import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from ..db.models import Document
from .event_bus import event_bus

class KnowledgeManager:
    def __init__(self):
        pass

    async def add_document(self, db: AsyncSession, title: str, content: str, source_url: str = "") -> dict:
        doc = Document(
            id=f"doc_{uuid.uuid4().hex[:8]}",
            title=title,
            content=content,
            source_url=source_url
        )
        db.add(doc)
        await db.commit()
        await db.refresh(doc)
        
        await event_bus.publish("thought_stream", {
            "type": "thought",
            "content": f"Ingested document into Knowledge Base: {title}",
            "module": "KnowledgeBase"
        })
        return {"id": doc.id, "title": doc.title}

    async def search(self, db: AsyncSession, query: str) -> List[Dict[str, Any]]:
        """Basic text search (simulating vector search)."""
        await event_bus.publish("thought_stream", {
            "type": "thought",
            "content": f"Searching Knowledge Base for: '{query}'",
            "module": "KnowledgeBase"
        })

        if not query:
            result = await db.execute(select(Document).limit(10))
        else:
            search_term = f"%{query}%"
            result = await db.execute(
                select(Document).where(
                    or_(
                        Document.title.ilike(search_term),
                        Document.content.ilike(search_term)
                    )
                ).limit(10)
            )
            
        docs = result.scalars().all()
        return [{"id": d.id, "title": d.title, "content": d.content, "source_url": d.source_url} for d in docs]

knowledge_manager = KnowledgeManager()
