"""
Layer 7: Strategy Library.
Stores reusable cognitive strategies chosen by the planner based on goal context.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Strategy:
    name: str
    category: str
    description: str
    steps: List[str]
    success_rate: float = 0.90


class StrategyLibrary:
    """Repository of pre-compiled, reusable cognitive strategies."""

    def __init__(self) -> None:
        self._strategies: Dict[str, Strategy] = {
            "scientific_review": Strategy(
                name="Scientific Review Strategy",
                category="research",
                description="Intake literature, extract knowledge, detect contradictions, generate hypotheses.",
                steps=["Intake Literature", "Extract Knowledge", "Detect Contradictions", "Generate Hypotheses"],
            ),
            "debugging": Strategy(
                name="Debugging Strategy",
                category="troubleshooting",
                description="Inspect logs, isolate failure site, hypothesize cause, verify fix.",
                steps=["Inspect Logs", "Isolate Failure", "Hypothesize Cause", "Verify Fix"],
            ),
            "negotiation": Strategy(
                name="Negotiation Strategy",
                category="interaction",
                description="Identify constraints, evaluate trade-offs, formulate counter-proposals.",
                steps=["Identify Constraints", "Evaluate Trade-offs", "Formulate Proposals"],
            ),
            "research": Strategy(
                name="Research Strategy",
                category="exploration",
                description="Search domain sources, summarize evidence, synthesize findings.",
                steps=["Search Sources", "Summarize Evidence", "Synthesize Findings"],
            ),
            "planning": Strategy(
                name="Planning Strategy",
                category="execution",
                description="Decompose goal, evaluate risk, simulate counterfactuals, generate tasks.",
                steps=["Decompose Goal", "Evaluate Risk", "Simulate Counterfactuals", "Generate Tasks"],
            ),
        }

    def get_strategy(self, category_or_name: str) -> Optional[Strategy]:
        key = category_or_name.lower().replace(" ", "_")
        if key in self._strategies:
            return self._strategies[key]

        for s in self._strategies.values():
            if s.category == category_or_name or key in s.name.lower():
                return s
        return None

    def list_strategies(self) -> List[str]:
        return [s.name for s in self._strategies.values()]
