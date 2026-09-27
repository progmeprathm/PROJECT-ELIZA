import json
import time
import os
from ecos.simulation.environment import SimpleEnvironment
from companion.shell import CognitiveShell

def run_experiment(config_name: str, use_memory: bool, use_world_model: bool):
    print(f"================================================================")
    print(f"  EXPERIMENT: {config_name}")
    print(f"================================================================\n")
    
    env = SimpleEnvironment()
    shell = CognitiveShell()
    
    # Disable components based on config
    if not use_memory:
        shell.memory_system.retrieve = lambda q, limit=10: []
        shell.memory_system.store = lambda k, v: None
        
    if not use_world_model:
        shell.world_model.process_observation = lambda obs: None
        shell.world_model.get_state = lambda: {}
        shell.world_model.get_beliefs = lambda: []
    
    goal = "Reach target location."
    obs = env.reset()
    
    provider = os.environ.get("ELIZA_MODEL_PROVIDER", "mock")
    
    experiment_results = {
        "experiment": config_name,
        "provider": provider,
        "cycles": 0,
        "goal_achieved": False,
        "actions": [],
        "errors": []
    }
    
    print(f"Goal: {goal}")
    print(f"Initial State: {obs}\n")
    
    max_cycles = 10
    
    for cycle in range(1, max_cycles + 1):
        print(f"--- Cycle {cycle} ---")
        try:
            result = shell.run_cycle(goal, obs)
            action = result["selected_action"]
            experiment_results["actions"].append(action)
            
            print(f"Reasoning -> {result['reasoning']}")
            print(f"Action -> {action}")
            
            obs = env.step(action, "")
            print(f"Observation -> {obs['message']}")
            
            if obs.get("agent_location") == obs.get("target_location"):
                print("\nSUCCESS: Agent reached target location!")
                experiment_results["goal_achieved"] = True
                experiment_results["cycles"] = cycle
                break
                
        except Exception as e:
            print(f"Error during cycle: {e}")
            experiment_results["errors"].append(str(e))
            break
            
        time.sleep(0.5)
        print("")
        
    if not experiment_results["goal_achieved"]:
        experiment_results["cycles"] = max_cycles
        print("\nFAILURE: Goal not achieved within cycle limit.")
        
    print("\n================================================================")
    print("  EXPERIMENT RESULTS")
    print("================================================================")
    print(json.dumps(experiment_results, indent=2))
    return experiment_results

if __name__ == "__main__":
    print("ELIZA ECOS - Runtime v0.2 Simulation\n")
    run_experiment("Configuration A - Stateless LLM", use_memory=False, use_world_model=False)
    run_experiment("Configuration B - LLM + World Model", use_memory=False, use_world_model=True)
    run_experiment("Configuration C - E.L.I.Z.A.", use_memory=True, use_world_model=True)
