import json
import time
import os
import argparse
from ecos.simulation.grid2d import Grid2DEnvironment
from companion.shell import CognitiveShell

def run_experiment_trial(config_name: str, use_memory: bool, use_world_model: bool, trial_id: int):
    print(f"--- Trial {trial_id} ---")
    
    env = Grid2DEnvironment()
    shell = CognitiveShell()
    
    if not use_memory:
        shell.memory_system.retrieve = lambda q, limit=10: []
        shell.memory_system.store = lambda k, v: None
        
    if not use_world_model:
        shell.world_model.process_observation = lambda obs: None
        shell.world_model.get_state = lambda: {}
        shell.world_model.get_beliefs = lambda: []
    
    goal = "Navigate the 2D grid and reach the final destination at (3, 3)."
    obs = env.reset()
    
    provider = os.environ.get("ELIZA_MODEL_PROVIDER", "mock")
    
    experiment_results = {
        "trial_id": trial_id,
        "cycles": 0,
        "goal_completed": False,
        "actions": [],
        "errors": [],
        "memory_retrievals": 0,
        "successful_memory_retrievals": 0,
        "world_model_updates": 0,
        "model_calls": 0,
        "fallback_actions": 0,
        "invalid_actions": 0,
        "environment_errors": 0,
        "critical_actions": [],
        "traces": []
    }
    
    max_cycles = 15
    
    for cycle in range(1, max_cycles + 1):
        try:
            result = shell.run_cycle(goal, obs)
            action = result["selected_action"]
            experiment_results["actions"].append(action)
            experiment_results["model_calls"] += 1
            
            trace_entry = {
                "cycle": cycle,
                "observation": obs,
                "world_model_context": shell.world_model.get_state() if use_world_model else {},
                "memory_query": goal,
                "retrieved_memories": result.get("retrieved_memories", []),
                "model": result.get("model_selected", "unknown"),
                "decision": result.get("reasoning", ""),
                "action": action
            }
            
            if use_memory:
                experiment_results["memory_retrievals"] += 1
                if result.get("retrieved_memories"):
                    experiment_results["successful_memory_retrievals"] += 1
                    
            if use_world_model:
                experiment_results["world_model_updates"] += 1
            
            if "fallback logic" in result['reasoning'].lower():
                experiment_results["fallback_actions"] += 1
                
            obs = env.step(action, "")
            trace_entry["environment_result"] = obs
            experiment_results["traces"].append(trace_entry)
            
            if action.startswith("unlock_door_"):
                if "Correct password" in obs['message']:
                    info_source = "UNKNOWN"
                    if use_memory and not use_world_model:
                        info_source = "MEMORY"
                    elif use_world_model and not use_memory:
                        info_source = "WORLD_MODEL"
                    elif use_memory and use_world_model:
                        info_source = "MEMORY"
                        
                    experiment_results["critical_actions"].append({
                        "action": action,
                        "required_information": "8592",
                        "information_source": info_source
                    })
                    
            if "Unknown" in obs['message'] or "Cannot pass" in obs['message'] or "Incorrect password" in obs['message'] or "invalid" in obs['message']:
                experiment_results["environment_errors"] += 1
            
            if obs.get("agent_location") == env.goal_pos:
                experiment_results["goal_completed"] = True
                experiment_results["cycles"] = cycle
                break
                
        except Exception as e:
            experiment_results["errors"].append(str(e))
            experiment_results["invalid_actions"] += 1
            break
            
        time.sleep(0.1)
        
    if not experiment_results["goal_completed"]:
        experiment_results["cycles"] = max_cycles
        
    return experiment_results

def run_configuration(config_name: str, use_memory: bool, use_world_model: bool, trials: int):
    print(f"================================================================")
    print(f"  EXPERIMENT: {config_name} ({trials} trials)")
    print(f"================================================================\n")
    
    results = []
    for i in range(trials):
        results.append(run_experiment_trial(config_name, use_memory, use_world_model, i+1))
        
    successes = sum(1 for r in results if r["goal_completed"])
    print(f"\nResult: {successes}/{trials} successful.\n")
    return {
        "experiment": config_name,
        "success_rate": f"{successes}/{trials}",
        "trials": results
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["mock", "live"], default="mock")
    args = parser.parse_args()
    
    print(f"ELIZA ECOS - Runtime v0.4 2D Benchmark ({args.mode.upper()} MODE)\n")
    
    if args.mode == "mock":
        os.environ["ELIZA_MODEL_PROVIDER"] = "mock"
        os.environ["ELIZA_EMBEDDING_PROVIDER"] = "deterministic"
        num_trials = 1
    else:
        # For live, require credentials
        if not os.environ.get("OPENAI_API_KEY"):
            print("LIVE_MODEL = NOT_RUN")
            print("REASON = credentials/configuration unavailable")
            exit(0)
            
        os.environ["ELIZA_MODEL_PROVIDER"] = "cloud"
        os.environ["ELIZA_EMBEDDING_PROVIDER"] = "cloud"
        num_trials = 3
    
    results_A = run_configuration("Configuration A - Stateless LLM", use_memory=False, use_world_model=False, trials=num_trials)
    results_B = run_configuration("Configuration B - World Model Only", use_memory=False, use_world_model=True, trials=num_trials)
    results_C = run_configuration("Configuration C - Memory Only", use_memory=True, use_world_model=False, trials=num_trials)
    results_D = run_configuration("Configuration D - E.L.I.Z.A.", use_memory=True, use_world_model=True, trials=num_trials)
    
    final_report = {
        "experiment": "ELIZA_V04_2D_GENERALIZATION",
        "mode": args.mode,
        "timestamp": time.time(),
        "provider": os.environ.get("ELIZA_MODEL_PROVIDER"),
        "embedding_provider": os.environ.get("ELIZA_EMBEDDING_PROVIDER"),
        "configurations": {
            "A": results_A,
            "B": results_B,
            "C": results_C,
            "D": results_D
        }
    }
    
    with open("docs/EXPERIMENT_V04_REPORT.json", "w") as f:
        json.dump(final_report, f, indent=2)
        
    print("\nBenchmark complete. Saved to docs/EXPERIMENT_V04_REPORT.json")
