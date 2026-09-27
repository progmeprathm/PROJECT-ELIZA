import json
import time
import os
import argparse
from typing import Dict, Any, List

from ecos.simulation.task_generator import TaskGenerator
from ecos.simulation.task_environment import TaskEnvironment
from ecos.world.graph import ECOSWorldModel
from ecos.memory.system import ECOSMemorySystem
from llms.router import ModelRouter
from ecos.tools.registry import ToolRegistry
from ecos.tools.calculator import CalculatorTool
from ecos.tools.memory_search import MemorySearchTool
from ecos.tools.environment import EnvironmentActionTool
from ecos.planning.planner_v05 import Planner
from ecos.planning.validator import PlanValidator
from ecos.planning.executor import PlanExecutor
from companion.shell import CognitiveShell
from llms.adapters.cloud import CloudAPIAdapter
from llms.adapters.mock import MockAdapter

def setup_tool_registry(env, memory_system):
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    registry.register(MemorySearchTool())
    
    # Custom environment tool mapping for generalized TaskEnvironment
    class GenEnvTool(EnvironmentActionTool):
        def execute(self, arguments: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
            action = arguments.get("action", "")
            if not context or "environment" not in context:
                return {"error": "Environment not provided in context."}
            env = context["environment"]
            try:
                # pass arguments to step to support interact_item and unlock_code
                obs = env.step(action, arguments)
                return {"observation": obs}
            except Exception as e:
                return {"error": str(e)}
                
    registry.register(GenEnvTool())
    return registry

def run_reactive_trial(config_name: str, task, use_world_model: bool, use_memory: bool, trial_id: int):
    env = TaskEnvironment(task)
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
    goal = f"Reach the goal room. (Family {task.family})"
    
    results = {
        "trial_id": trial_id,
        "config": config_name,
        "task_id": task.task_id,
        "task_family": task.family,
        "goal_completed": False,
        "traces": [],
    }
    
    obs = env.get_observation()
    world_model.process_observation(obs)
    
    for cycle in range(1, 15):
        try:
            result = shell.run_cycle(goal, obs)
            action = result["selected_action"]
        except Exception as e:
            action = "error"
            
        results["traces"].append({
            "cycle": cycle,
            "action": action,
            "observation": obs
        })
        
        obs = env.step(action)
        
        if env.goal_completed:
            results["goal_completed"] = True
            break
            
    return results

def run_planned_trial(config_name: str, task, use_world_model: bool, use_memory: bool, use_replanning: bool, trial_id: int, router):
    env = TaskEnvironment(task)
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

    registry = setup_tool_registry(env, memory_system)
    
    planner = Planner(router, registry)
    validator = PlanValidator(registry)
    executor = PlanExecutor(planner, validator, registry, world_model, memory_system)
    executor.context["environment"] = env
    
    # We define the goal generically
    goal = f"Navigate through the rooms, find any necessary codes, calculate required values, unlock mechanisms, and reach the goal room. Family: {task.family}."
    
    results = {
        "trial_id": trial_id,
        "config": config_name,
        "task_id": task.task_id,
        "task_family": task.family,
        "goal_completed": False,
        "plan_created": False,
        "replan_count": 0,
        "traces": [],
        "leakage_detected": False,
    }
    
    obs = env.get_observation()
    world_model.process_observation(obs)
    
    max_replans = 3 if use_replanning else 0
    
    initial_plan = planner.create_plan(goal, world_model.get_state(), [])
    results["plan_created"] = (len(initial_plan.steps) > 0)
    
    final_plan = executor.execute_plan(initial_plan, max_replans=max_replans)
    
    results["replan_count"] = len(final_plan.replanning_history)
    results["traces"] = final_plan.to_dict()
    
    if env.goal_completed:
        results["goal_completed"] = True
        
    return results

def run_model_only_trial(config_name: str, task, trial_id: int, router):
    env = TaskEnvironment(task)
    goal = f"Reach the goal room. Family: {task.family}."
    
    registry = setup_tool_registry(env, None)
    
    results = {
        "trial_id": trial_id,
        "config": config_name,
        "task_id": task.task_id,
        "task_family": task.family,
        "goal_completed": False,
        "traces": [],
    }
    
    obs = env.get_observation()
    
    for cycle in range(1, 15):
        tools_schema = json.dumps(registry.get_tool_schemas(), indent=2)
        prompt = (
            f"GOAL: {goal}\n"
            f"CURRENT OBSERVATION: {obs}\n"
            f"Available Tools:\n{tools_schema}\n\n"
            "Select exactly ONE tool to use next."
        )
        schema = {
            "type": "object",
            "properties": {
                "tool": {"type": "string"},
                "arguments": {"type": "object"}
            },
            "required": ["tool", "arguments"]
        }
        
        try:
            res = router.route_task("reasoning", prompt, schema=schema)
            tool_name = res.get("tool", "")
            args = res.get("arguments", {})
        except Exception:
            tool_name = "error"
            args = {}
            
        results["traces"].append({
            "cycle": cycle,
            "tool": tool_name,
            "arguments": args,
            "observation": obs
        })
        
        if tool_name:
            try:
                if tool_name == "environment_action":
                    obs = env.step(args.get("action", ""), args)
                else:
                    context = {"environment": env, "memory_system": None}
                    obs = registry.execute(tool_name, args, context)
            except Exception as e:
                obs = {"error": str(e)}
        
        if env.goal_completed:
            results["goal_completed"] = True
            break
            
    return results

def run_benchmark():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["mock", "live"], default="mock")
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--difficulty", type=int, default=2)
    args = parser.parse_args()
    
    generator = TaskGenerator(seed=args.seed)
    
    if args.mode == "mock":
        os.environ["ELIZA_MODEL_PROVIDER"] = "mock"
        router = ModelRouter()
    else:
        if not os.environ.get("OPENAI_API_KEY"):
            print("LIVE_MODEL = NOT_RUN\nREASON = credentials unavailable")
            with open("docs/EXPERIMENT_V06_REPORT.json", "w") as f:
                json.dump({"mode": "live", "status": "NOT_RUN"}, f)
            return
        os.environ["ELIZA_MODEL_PROVIDER"] = "cloud"
        os.environ["ELIZA_EMBEDDING_PROVIDER"] = "cloud"
        router = ModelRouter()
        
    tasks = [generator.generate_random_task(args.difficulty) for _ in range(args.trials)]
    
    configs = [
        ("MODEL_ONLY", False, False, False, False, True),
        ("A - Stateless", False, False, False, False, False),
        ("B - World Model Only", True, False, False, False, False),
        ("C - Memory Only", False, True, False, False, False),
        ("D - Cognitive Core", True, True, False, False, False),
        ("E - Planning", True, True, False, True, False),
        ("F - Full v0.6", True, True, True, True, False)
    ]
    
    report = {
        "experiment": "ELIZA_V06_LIVE_BENCHMARK",
        "mode": args.mode,
        "seed": args.seed,
        "difficulty": args.difficulty,
        "timestamp": time.time(),
        "configurations": {}
    }
    
    for name, wm, mem, rep, plan, raw in configs:
        print(f"\nRunning {name} ...")
        trials_res = []
        for i, task in enumerate(tasks):
            if raw:
                res = run_model_only_trial(name, task, i+1, router)
            elif plan:
                res = run_planned_trial(name, task, wm, mem, rep, i+1, router)
            else:
                res = run_reactive_trial(name, task, wm, mem, i+1)
            trials_res.append(res)
        
        successes = sum(1 for r in trials_res if r["goal_completed"])
        print(f"Result: {successes}/{args.trials} successful.")
        report["configurations"][name] = {
            "success_rate": f"{successes}/{args.trials}",
            "trials": trials_res
        }
        
    with open("docs/EXPERIMENT_V06_REPORT.json", "w") as f:
        json.dump(report, f, indent=2)
    print("\nSaved docs/EXPERIMENT_V06_REPORT.json")

if __name__ == "__main__":
    run_benchmark()
