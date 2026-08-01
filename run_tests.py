"""
Master Test & Verification Runner for ELIZA Cognitive OS.
Executes complete suite verifying compliance across Phase 1 to Phase 5, ELIZA Studio, and ELIZA Companion architecture.
"""

import os
import sys
import traceback

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from companion.client import ECOSClient
from companion.manager import ConversationManager, DecisionReasoningTrace
from companion.shell import CognitiveShell
from ELIZA_OBJECTS import Action, Belief, Decision, Goal, Memory, Observation, Outcome, Plan
from ecos.benchmarks.evaluator import CognitiveEvaluator
from ecos.benchmarks.suite import CognitiveBenchmarkSuite
from ecos.cfs.filesystem import CognitiveFilesystem
from ecos.civilization.collaboration import CognitiveCoordinator
from ecos.civilization.federation import DistributedWorldModel, KnowledgeFederationGateway
from ecos.civilization.governance import CognitiveGovernanceEngine, ReputationEngine
from ecos.civilization.minds import SpecializedMind
from ecos.civilization.network import CognitiveNetworkNode
from ecos.civilization.preservation import HumanPartnershipInterface, KnowledgeArchive
from ecos.cognition.state import CognitiveStateMachine, StateStage
from ecos.compiler.compiler import CognitiveCompiler
from ecos.cvm.vm import CognitiveCPU
from ecos.evolution.assets import VersionedPolicy, VersionedSkill
from ecos.evolution.meta_optimizer import ArchitectureOptimizer, MetaCognitiveOptimizer
from ecos.experiments.framework import ExperimentFramework, HumanCollaborationGateway
from ecos.isa import CognitiveInstruction, CognitiveISAVirtualMachine, CognitiveOpcode
from ecos.kernel.vm import ECOSVMKernel
from ecos.learning.adaptive_pipeline import AdaptiveLearningPipeline
from ecos.memory.hierarchy import CognitiveMemoryHierarchy
from ecos.memory.system import ECOSMemorySystem
from ecos.os.kernel_os import ECOSOperatingSystem
from ecos.planning.planner import ECOSPlanner
from ecos.process.process import ProcessScheduler
from ecos.reasoning.engine import ECOSReasoner
from ecos.science.engine import ScientificEngine
from ecos.simulation.simulator import ECOSSimulator
from ecos.strategies.library import StrategyLibrary
from ecos.world.graph import ECOSWorldModel
from run_ecos_adaptive_loop import run_phase4_adaptive_loop
from run_ecos_brainstem import run_brainstem
from run_ecos_civilization import run_phase5_civilization_milestone
from run_ecos_runtime import run_ecos_phase3_milestone
from studio.server import ELIZAStudioRequestHandler


def test_eliza_companion_manager_and_assistants() -> None:
    """Test ConversationManager, assistant switching, and decision reasoning trace generation."""
    mgr = ConversationManager()
    assert mgr.current_assistant.id == "architect"

    assert mgr.set_assistant("researcher") is True
    assert mgr.current_assistant.id == "researcher"

    res = mgr.process_message("Design scheduler")
    assert "response" in res
    assert "trace" in res
    assert isinstance(res["trace"], DecisionReasoningTrace)
    assert res["trace"].confidence > 0.80


def test_cognitive_shell_commands() -> None:
    """Test Mode 3 Cognitive Shell commands."""
    shell = CognitiveShell()
    res_mem = shell.execute_command("/memory search scheduler")
    assert res_mem["status"] == "SUCCESS"

    res_goal = shell.execute_command("/goal create Build Planner")
    assert res_goal["status"] == "SUCCESS"

    res_sim = shell.execute_command("/simulate scenario_a")
    assert res_sim["status"] == "SUCCESS"


def test_ecos_automation_client_sdk() -> None:
    """Test ECOSClient Automation API Python SDK."""
    client = ECOSClient()
    g_res = client.submit_goal("Test SDK goal", priority=10)
    assert g_res["pid"] > 0

    bm = client.run_benchmark()
    assert bm["aggregate_score"] > 0.85


def test_model_router_and_adapters() -> None:
    """Test Model Abstraction Layer, ModelRegistry, and ModelRouter dynamic task routing."""
    from llms.router import ModelRouter, TaskIntent
    from llms.keys import set_api_key
    
    # Set dummy keys to prevent fallback for testing normal routing
    set_api_key("deepseek", "dummy_key")
    set_api_key("qwen", "dummy_key")
    
    router = ModelRouter()
    
    res_code = router.route_task(TaskIntent.CODING, "Write python code")
    assert res_code["selected_model"] == "deepseek-coder"
    
    res_reason = router.route_task(TaskIntent.REASONING, "Formulate proof")
    assert res_reason["selected_model"] == "qwen-2.5-72b"
    
    # Test Fallback (intentionally break key)
    set_api_key("deepseek", "")
    router.adapters["deepseek-coder"].api_key = ""  # Force clear for test instance
    res_fallback = router.route_task(TaskIntent.CODING, "Write python code")
    assert res_fallback["selected_model"] == "llama-3.1-8b"
    assert res_fallback["routed_by"] == "ModelRouter_Fallback"


def run_all_tests() -> bool:
    tests = [
        ("Model-Agnostic LLM Abstraction Layer & ModelRouter", test_model_router_and_adapters),
        ("ELIZA Companion Manager & Assistant Profiles", test_eliza_companion_manager_and_assistants),
        ("Mode 3 Cognitive Shell CLI Command Processor", test_cognitive_shell_commands),
        ("ECOS Automation API Python Client SDK", test_ecos_automation_client_sdk),
        ("ELIZA Studio v0.1 API Backend Bridge", lambda: test_studio_backend()),
        ("Layer 1: Specialized Mind Profiles (Multiple Minds)", lambda: test_specialized_minds_and_roles()),
        ("Layer 2: Cognitive Networking (P2P CCP Delivery)", lambda: test_cognitive_networking_p2p()),
        ("Layer 3 & 8: Distributed World Model & Knowledge Federation", lambda: test_distributed_world_model_and_federation()),
        ("Layer 4 & 5: Cognitive Governance & Reputation Routing", lambda: test_governance_and_reputation_routing()),
        ("Layer 6, 7 & 11: Multi-Agent Collaborative Workflows", lambda: test_cognitive_coordinator_collaboration()),
        ("Layer 12 & 14: Knowledge Archive & Human Ethical Gateway", lambda: test_knowledge_archive_and_human_gateway()),
        ("Phase 2 Milestone: Functioning Brain Stem", lambda: run_brainstem("Brainstem test")),
        ("Phase 3 Milestone: ELIZA Cognitive Runtime (ECOS)", lambda: run_ecos_phase3_milestone("ECOS test")),
        ("Phase 4 Milestone: Adaptive Feedback Loop & Hypothesis H1", lambda: run_phase4_adaptive_loop()),
        ("Phase 5 Milestone: Cognitive Civilization Ecosystem Architecture", lambda: run_phase5_civilization_milestone()),
    ]

    passed = 0
    failed = 0

    print("==================================================")
    print("  ELIZA ECOS — MASTER SUITE & COMPANION VERIFICATION")
    print("==================================================\n")

    for name, test_func in tests:
        try:
            test_func()
            print(f"[PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            traceback.print_exc()
            failed += 1

    print("\n--------------------------------------------------")
    print(f"Summary: {passed} passed, {failed} failed out of {len(tests)} tests.")
    print("==================================================")

    return failed == 0


def test_studio_backend():
    assert ELIZAStudioRequestHandler is not None


def test_specialized_minds_and_roles():
    sm = SpecializedMind(name="Sci", role="Scientist")
    assert sm.process_task("test")["role"] == "Scientist"


def test_cognitive_networking_p2p():
    na = CognitiveNetworkNode("na")
    nb = CognitiveNetworkNode("nb")
    na.connect_peer(nb)
    assert na.send_ccp_message("nb", "hello") is True


def test_distributed_world_model_and_federation():
    dwm = DistributedWorldModel()
    gw = KnowledgeFederationGateway(dwm)
    assert gw.federate_item("concept", ["fact"], 0.95) is True


def test_governance_and_reputation_routing():
    rep = ReputationEngine()
    rep.update_reputation("m1", 0.95)
    m = SpecializedMind(mind_id="m1", role="Planner")
    assert rep.select_best_specialist([m], "Planner") == m


def test_cognitive_coordinator_collaboration():
    rep = ReputationEngine()
    coord = CognitiveCoordinator(rep)
    m = SpecializedMind(role="Scientist")
    coord.register_mind(m)
    assert "project_name" in coord.execute_collaborative_workflow("P1", "Problem")


def test_knowledge_archive_and_human_gateway():
    ka = KnowledgeArchive()
    art = ka.archive_artifact("T", "A", "C", ["P"])
    assert ka.get_artifact(art.artifact_id) == art
    hw = HumanPartnershipInterface()
    assert hw.verify_ethical_compliance("Valid action") is True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
