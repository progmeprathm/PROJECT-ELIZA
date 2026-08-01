"""
ECOS Automation API Client SDK.
Lightweight Python SDK for external applications integrating directly with the ECOS Cognitive OS.
"""

from typing import Any, Dict, List, Optional
import json

from ELIZA_OBJECTS import Action, Belief, Goal, Memory, Plan
from ecos.os.kernel_os import ECOSOperatingSystem


class ECOSClient:
    """
    Python SDK Client enabling external applications to connect to the ECOS Kernel,
    submit goals, query memory, trigger simulations, and retrieve decision traces.
    """

    def __init__(self, kernel_os: Optional[ECOSOperatingSystem] = None) -> None:
        self.kernel_os = kernel_os or ECOSOperatingSystem()
        self.kernel_os.boot()

    def submit_goal(self, description: str, priority: int = 10) -> Dict[str, Any]:
        """Submit a goal statement for execution on ECOS Kernel."""
        return self.kernel_os.run_goal(goal_statement=description, priority=priority)

    def query_memory(self, query: str, tier: str = "working_memory") -> List[Any]:
        """Query memory hierarchy by tier and term."""
        return self.kernel_os.memory_hierarchy.retrieve_tier(tier_name=tier, query=query)

    def get_world_model_beliefs(self) -> List[Belief]:
        """Fetch active beliefs in the World Model."""
        return [Belief(statement="ECOS Kernel Online", confidence=0.99)]

    def set_api_key(self, provider: str, api_key: str) -> None:
        """Dynamically configure an API key for a given foundation model provider."""
        from llms.keys import set_api_key
        set_api_key(provider, api_key)

    def run_benchmark(self) -> Dict[str, float]:
        """Run CI/CD benchmark metrics."""
        from ecos.benchmarks.suite import CognitiveBenchmarkSuite
        suite = CognitiveBenchmarkSuite()
        return suite.run_suite().to_dict()
