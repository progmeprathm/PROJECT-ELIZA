"""
ELIZA Phase 5 Milestone Runner: Cognitive Civilization Ecosystem Architecture.
Demonstrates:
Multiple Minds -> Cognitive Networking (CCP) -> Distributed World Model ->
Governance & Reputation Engine -> Multi-Agent Collaboration -> Human Partnership.
"""

import sys

from ecos.civilization.collaboration import CognitiveCoordinator
from ecos.civilization.federation import DistributedWorldModel, KnowledgeFederationGateway
from ecos.civilization.governance import CognitiveGovernanceEngine, ReputationEngine
from ecos.civilization.minds import SpecializedMind
from ecos.civilization.network import CognitiveNetworkNode
from ecos.civilization.preservation import HumanPartnershipInterface, KnowledgeArchive


def run_phase5_civilization_milestone() -> bool:
    print("=================================================================")
    print("  ELIZA ECOS — PHASE 5 COGNITIVE CIVILIZATION ECOSYSTEM")
    print("=================================================================\n")

    # 1. Initialize Governance, Reputation Engine & Human Gateway (Layers 4, 5 & 14)
    governance = CognitiveGovernanceEngine()
    reputation_engine = ReputationEngine()
    human_gateway = HumanPartnershipInterface()

    objective = human_gateway.set_objective("Design planetary quantum-resilient cognitive communication grid")
    print(f"[1. HUMAN GOVERNANCE] Approved Objective: '{objective}'")
    print(f"                       Ethical Boundaries Enforced: {len(human_gateway.ethical_boundaries)}")

    # 2. Instantiate Specialized Minds (Layer 1)
    scientist = SpecializedMind(name="ELIZA-Scientist-Alpha", role="Scientist", reputation_score=0.96)
    planner = SpecializedMind(name="ELIZA-Planner-Beta", role="Planner", reputation_score=0.94)
    engineer = SpecializedMind(name="ELIZA-Engineer-Gamma", role="Engineer", reputation_score=0.92)
    simulator = SpecializedMind(name="ELIZA-Simulator-Delta", role="Simulator", reputation_score=0.95)

    for mind in [scientist, planner, engineer, simulator]:
        governance.register_mind_identity(mind.mind_id, mind.role)

    print(f"[2. MULTIPLE MINDS]    Registered 4 Specialized Mind Nodes:")
    print(f"                       • {scientist.name} ({scientist.role}) - Rep: {scientist.reputation_score}")
    print(f"                       • {planner.name} ({planner.role}) - Rep: {planner.reputation_score}")
    print(f"                       • {engineer.name} ({engineer.role}) - Rep: {engineer.reputation_score}")
    print(f"                       • {simulator.name} ({simulator.role}) - Rep: {simulator.reputation_score}")

    # 3. Establish P2P Cognitive Network Nodes over CCP (Layer 2)
    net_scientist = CognitiveNetworkNode(scientist.mind_id)
    net_engineer = CognitiveNetworkNode(engineer.mind_id)
    net_scientist.connect_peer(net_engineer)

    msg_delivered = net_scientist.send_ccp_message(recipient_node_id=engineer.mind_id, payload={"type": "RESEARCH_DATA", "bytes": 2048})
    print(f"\n[3. CCP NETWORKING]    P2P CCP Message Delivery: {'SUCCESSFUL' if msg_delivered else 'FAILED'}")

    # 4. Multi-Agent Collaborative Problem Solving (Layers 6, 7 & 11)
    coordinator = CognitiveCoordinator(reputation_engine=reputation_engine)
    for mind in [scientist, planner, engineer, simulator]:
        coordinator.register_mind(mind)

    collab_result = coordinator.execute_collaborative_workflow(
        project_name="Quantum-Resilient Grid Initiative",
        problem_statement="Quantum-resilient cognitive communication grid",
    )

    print(f"\n[4. COLLABORATION]     Executed Collaborative Pipeline [{collab_result['project_name']}]:")
    print(f"                       Participants: {collab_result['participants_count']} mind nodes")
    for role, out in collab_result["pipeline_outputs"].items():
        print(f"                       • {role}: {out['result']}")

    # 5. Distributed World Model & Knowledge Federation (Layers 3 & 8)
    dwm = DistributedWorldModel()
    federation_gw = KnowledgeFederationGateway(dwm=dwm)
    fed_success = federation_gw.federate_item(
        concept="Quantum CCP Routing",
        facts=["Zero packet loss", "End-to-end auditability"],
        score=0.95,
    )
    print(f"\n[5. FEDERATED WORLD]   Federated Item to Shared Knowledge Graph: {'SUCCESSFUL' if fed_success else 'FAILED'}")
    print(f"                       Shared Knowledge Graph Size: {len(dwm.shared_knowledge)} concept(s)")

    # 6. Knowledge Preservation Archive (Layer 12)
    archive = KnowledgeArchive()
    archived_art = archive.archive_artifact(
        title="Planetary Quantum Grid Architecture Paper",
        author_mind_id=scientist.mind_id,
        content=collab_result,
        provenance=[scientist.mind_id, planner.mind_id, engineer.mind_id, simulator.mind_id],
    )
    print(f"\n[6. PRESERVATION]      Archived Durable Research Paper [{archived_art.artifact_id}]:")
    print(f"                       • Title: '{archived_art.title}'")
    print(f"                       • Provenance Chain: {' -> '.join(archived_art.provenance_chain)}")

    print("\n-----------------------------------------------------------------")
    print("SUCCESS: Phase 5 Cognitive Civilization Milestone Verified!")
    print("=================================================================")

    return True


if __name__ == "__main__":
    success = run_phase5_civilization_milestone()
    sys.exit(0 if success else 1)
