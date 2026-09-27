import json
import time
import os
import argparse
from typing import Dict, Any, List

from ecos.simulation.planning_world import PlanningWorld
from ecos.world.graph import ECOSWorldModel
from ecos.memory.system import ECOSMemorySystem, get_embedding_provider
from llms.router import ModelRouter
from ecos.tools.registry import ToolRegistry
from ecos.tools.calculator import CalculatorTool
from ecos.tools.memory_search import MemorySearchTool
from ecos.tools.environment import EnvironmentActionTool
from ecos.planning.planner_v05 import Planner
from ecos.planning.validator import PlanValidator
from ecos.planning.executor import PlanExecutor
from companion.shell import CognitiveShell

def setup_tool_registry(env, memory_system):
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    
    mem_tool = MemorySearchTool()
    registry.register(mem_tool)
    
    env_tool = EnvironmentActionTool()
    registry.register(env_tool)
    
    return registry

def run_reactive_trial(config_name: str, use_world_model: bool, use_memory: bool, trial_id: int):
    env = PlanningWorld()
    world_model = ECOSWorldModel() if use_world_model else None
    
    if not world_model:
        class DummyWorldModel:
            def process_observation(self, obs): pass
            def get_state(self): return {}
            def get_beliefs(self): return []
        world_model = DummyWorldModel()
        
    memory_system = ECOSMemorySystem() if use_memory else None
    if not memory_system:
        class DummyMemorySystem:
            def store(self, k, v): pass
            def retrieve(self, q, limit=10): return []
        memory_system = DummyMemorySystem()

    shell = CognitiveShell(world_model=world_model, memory_system=memory_system)
    goal = "Navigate through the rooms, find the base code and multiplier, calculate the password, unlock the door, and reach the final destination."
    
    results = {
        "trial_id": trial_id,
        "config": config_name,
        "goal_completed": False,
        "replan_count": 0,
        "traces": [],
    }
    
    obs = env.reset()
    world_model.process_observation(obs)
    
    for cycle in range(1, 15):
        result = shell.run_cycle(goal, obs)
        action = result["selected_action"]
        
        results["traces"].append({
            "cycle": cycle,
            "action": action,
            "observation": obs
        })
        
        obs = env.step(action, "")
        
        if env.agent_pos == env.goal_pos:
            results["goal_completed"] = True
            break
            
    return results

def run_planned_trial(config_name: str, use_world_model: bool, use_memory: bool, use_replanning: bool, trial_id: int):
    env = PlanningWorld()
    world_model = ECOSWorldModel() if use_world_model else None
    
    # Quick mock implementation of world model if None
    if not world_model:
        class DummyWorldModel:
            def process_observation(self, obs): pass
            def get_state(self): return {}
            def get_beliefs(self): return []
        world_model = DummyWorldModel()
        
    memory_system = ECOSMemorySystem() if use_memory else None
    if not memory_system:
        class DummyMemorySystem:
            def store(self, k, v): pass
            def retrieve(self, q, limit=10): return []
        memory_system = DummyMemorySystem()

    router = ModelRouter()
    registry = setup_tool_registry(env, memory_system)
    
    planner = Planner(router, registry)
    validator = PlanValidator(registry)
    executor = PlanExecutor(planner, validator, registry, world_model, memory_system)
    executor.context["environment"] = env
    
    goal = "Navigate through the rooms, find the base code and multiplier, calculate the password, unlock the door, and reach the final destination."
    
    results = {
        "trial_id": trial_id,
        "config": config_name,
        "goal_completed": False,
        "plan_created": False,
        "plan_validation_errors": 0,
        "replan_count": 0,
        "invalid_actions": 0,
        "environment_errors": 0,
        "tool_calls": 0,
        "successful_tool_calls": 0,
        "failed_tool_calls": 0,
        "memory_retrievals": 0,
        "traces": [],
        "leakage_detected": False,
        "critical_information_source": "UNKNOWN"
    }
    
    obs = env.reset()
    world_model.process_observation(obs)
    
    max_replans = 3 if use_replanning else 0
    
    # Environmental Change failure injection for trial 2
    if trial_id == 2 and use_replanning:
        env.inject_environmental_change()
        
    # Execution
    initial_plan = planner.create_plan(goal, world_model.get_state(), [])
    results["plan_created"] = True
    
    final_plan = executor.execute_plan(initial_plan, max_replans=max_replans)
    
    results["replan_count"] = len(final_plan.replanning_history)
    results["traces"] = final_plan.to_dict()
    
    if env.agent_pos == env.goal_pos:
        results["goal_completed"] = True
        
    return results

def run_configuration(name, use_world_model, use_memory, use_replanning, is_planned, trials):
    print(f"\nRunning {name} ...")
    trial_results = []
    for i in range(trials):
        if is_planned:
            res = run_planned_trial(name, use_world_model, use_memory, use_replanning, i+1)
        else:
            res = run_reactive_trial(name, use_world_model, use_memory, i+1)
        trial_results.append(res)
    successes = sum(1 for r in trial_results if r["goal_completed"])
    print(f"Result: {successes}/{trials} successful.")
    return {
        "experiment": name,
        "success_rate": f"{successes}/{trials}",
        "trials": trial_results
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["mock", "live"], default="mock")
    args = parser.parse_args()
    
    print(f"ELIZA ECOS - Runtime v0.5 Planning Benchmark ({args.mode.upper()} MODE)")
    
    if args.mode == "mock":
        os.environ["ELIZA_MODEL_PROVIDER"] = "mock"
        os.environ["ELIZA_EMBEDDING_PROVIDER"] = "deterministic"
        trials = 3
    else:
        if not os.environ.get("OPENAI_API_KEY"):
            print("LIVE_MODEL = NOT_RUN")
            print("REASON = credentials unavailable")
            exit(0)
        os.environ["ELIZA_MODEL_PROVIDER"] = "cloud"
        os.environ["ELIZA_EMBEDDING_PROVIDER"] = "cloud"
        trials = 3
        
    res_A = run_configuration("A - Stateless", False, False, False, False, trials)
    res_B = run_configuration("B - World Model Only", True, False, False, False, trials)
    res_C = run_configuration("C - Memory Only", False, True, False, False, trials)
    res_D = run_configuration("D - E.L.I.Z.A. Core", True, True, False, False, trials)
    res_E = run_configuration("E - E.L.I.Z.A. + Planning", True, True, False, True, trials)
    res_F = run_configuration("F - Full v0.5", True, True, True, True, trials)
    
    report = {
        "experiment": "ELIZA_V05_PLANNING_BENCHMARK",
        "mode": args.mode,
        "timestamp": time.time(),
        "configurations": {
            "A": res_A,
            "B": res_B,
            "C": res_C,
            "D": res_D,
            "E": res_E,
            "F": res_F
        }
    }
    
    with open("docs/EXPERIMENT_V05_REPORT.json", "w") as f:
        json.dump(report, f, indent=2)
    print("\nSaved docs/EXPERIMENT_V05_REPORT.json")
