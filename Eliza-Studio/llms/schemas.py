"""
Structured Prompt & Output Schemas for LLM Execution.
Guarantees LLM outputs populate rigid FCRL cognitive object schemas.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StructuredOutputSchema:
    schema_name: str
    description: str
    required_fields: List[str]
    example: Dict[str, Any]

    def format_prompt(self, goal: str, beliefs: List[str], memories: List[str], constraints: List[str]) -> str:
        return (
            f"--- COGNITIVE TASK PROMPT ---\n"
            f"Goal:\n{goal}\n\n"
            f"Active Beliefs:\n" + "\n".join([f"- {b}" for b in beliefs]) + "\n\n"
            f"Relevant Memories:\n" + "\n".join([f"- {m}" for m in memories]) + "\n\n"
            f"Constraints:\n" + "\n".join([f"- {c}" for c in constraints]) + "\n\n"
            f"Required Output Schema ({self.schema_name}):\n"
            f"Provide JSON object with fields: {', '.join(self.required_fields)}\n"
            f"----------------------------"
        )
