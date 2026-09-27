import json
from typing import Dict, Any
from .llm_router import llm_router
from .event_bus import event_bus
from .world_model import world_model
from sqlalchemy.ext.asyncio import AsyncSession

class SimulatorEngine:
    def __init__(self):
        pass

    async def simulate(self, db: AsyncSession, plan: list, goal_title: str) -> Dict[str, Any]:
        """
        Simulates the execution of a plan against the World Model context.
        """
        await event_bus.publish("thought_stream", {
            "type": "thought",
            "content": f"Initializing Monte Carlo simulation for plan execution...",
            "module": "Simulator"
        })
        
        # 1. Fetch current world model context
        world_graph = await world_model.retrieve_graph(db)
        world_context = json.dumps(world_graph)

        prompt = f"""
Given the current World Model:
{world_context}

Critique the following plan for the goal: "{goal_title}"
Plan:
{json.dumps(plan)}

Return ONLY a JSON object with this structure:
{{
  "success_probability": 0.85,
  "critique": "A brief 2-sentence analysis of why this plan might fail or succeed."
}}
"""
        system = "You are the Simulator module of the ECOS Kernel. You output strictly valid JSON."

        try:
            await event_bus.publish("thought_stream", {
                "type": "thought",
                "content": "Simulating plan against World Graph...",
                "module": "Simulator"
            })
            
            response = await llm_router.generate(prompt, system)
            
            # Naive JSON extraction
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
                
            result = json.loads(response.strip())
            
            await event_bus.publish("thought_stream", {
                "type": "thought",
                "content": f"Simulation complete. Probability: {result.get('success_probability', 0)}",
                "module": "Simulator"
            })
            
            return result
        except Exception as e:
            print(f"Simulator failed: {e}")
            await event_bus.publish("thought_stream", {
                "type": "thought",
                "content": f"ERROR: Simulation failed ({e})",
                "module": "Simulator"
            })
            return {
                "success_probability": 0.0,
                "critique": "Simulation engine failure. Check LLM logs."
            }

simulator = SimulatorEngine()
