from sqlalchemy import Column, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base
import json

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="Active")

class Goal(Base):
    __tablename__ = "goals"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    priority = Column(String)
    progress = Column(Float, default=0.0)
    status = Column(String, default="PLANNING")
    activity = Column(String, default="")
    next_step = Column(String, default="")
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
    _plan_json = Column("plan", String)

    @property
    def plan(self):
        return json.loads(self._plan_json) if self._plan_json else []
        
    @plan.setter
    def plan(self, value):
        self._plan_json = json.dumps(value)

class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    source_url = Column(String)

class Agent(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String)
    capabilities = Column(String) # JSON list of skill IDs
    status = Column(String, default="Idle")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    endpoint_mock = Column(String)

class MemoryFragment(Base):
    __tablename__ = "memory_fragments"

    id = Column(String, primary_key=True, index=True)
    content = Column(String)
    tier = Column(String) # 'Working', 'Semantic', 'Episodic'
    confidence = Column(Float, default=1.0)
    source = Column(String, default="System")

class Entity(Base):
    __tablename__ = "entities"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String) # 'Person', 'Project', 'Technology'
    attributes = Column(String) # JSON string of key-value pairs

class Relationship(Base):
    __tablename__ = "relationships"

    id = Column(String, primary_key=True, index=True)
    source_id = Column(String, ForeignKey("entities.id"))
    target_id = Column(String, ForeignKey("entities.id"))
    relation_type = Column(String) # e.g. 'prioritizes', 'depends_on'
    
class MemoryEntry(Base):
    __tablename__ = "memories"
    
    id = Column(String, primary_key=True, index=True)
    tier = Column(String)  # WORKING, SEMANTIC, EPISODIC
    content = Column(String)
    metadata_json = Column(JSON, default=dict)
