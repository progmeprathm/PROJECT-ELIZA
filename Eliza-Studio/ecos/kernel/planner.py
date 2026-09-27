from typing import List, Dict, Any
import json
from .llm_router import llm_router
from .event_bus import event_bus

class Planner:
    def __init__(self):
        pass

    async def decompose(self, goal_description: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Takes a high-level goal and uses the LLM to break it down into dual alternative plan trees.
        """
        # Publish thought trace
        await event_bus.publish("thought_stream", {
            "type": "thought",
            "content": f"Decomposing goal into Plan Alpha and Plan Beta: {goal_description}",
            "module": "Planner"
        })

        prompt = f"""
Decompose the following goal into two alternative plans.
Plan A should be "Safe and Iterative" (low risk, thorough).
Plan B should be "Aggressive and Fast" (high risk, quick).
Return ONLY a JSON object with this exact structure:
{{
  "plan_a": [{{"name": "Step 1", "status": "pending"}}],
  "plan_b": [{{"name": "Step 1", "status": "pending"}}]
}}
Goal: {goal_description}
"""
        system = "You are the Planner module of the ECOS Kernel. You output strictly valid JSON."
        
        try:
            await event_bus.publish("thought_stream", {
                "type": "thought",
                "content": "Routing task to LLM engine...",
                "module": "ModelRouter"
            })
            
            response = await llm_router.generate(prompt, system)
            
            # Naive JSON extraction in case of markdown wrapping
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
                
            plans = json.loads(response.strip())
            
            await event_bus.publish("thought_stream", {
                "type": "thought",
                "content": f"Successfully generated alternative plans.",
                "module": "Planner"
            })
            
            return plans
        except Exception as e:
            print(f"Planner failed: {e}")
            await event_bus.publish("thought_stream", {
                "type": "thought",
                "content": f"ERROR: Cognitive engine failed ({e})",
                "module": "Planner"
            })
            return {
                "plan_a": [{"name": "Fallback: Manual Planning Required", "status": "pending"}],
                "plan_b": [{"name": "Fallback: Manual Planning Required", "status": "pending"}]
            }

    def evaluate_alternatives(self, goal_description: str) -> List[Dict[str, Any]]:
        return [
            {"id": "plan_A", "cost": "Low", "risk": "Medium", "recommendation": True},
            {"id": "plan_B", "cost": "High", "risk": "Low", "recommendation": False}
        ]

planner = Planner()
