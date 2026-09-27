"""
ELIZA Studio Backend Server API Bridge.
Serves HTTP REST endpoints exposing ECOS Kernel state, 7-Tier Memory, World Model Graph,
Goal Tree, Planner comparison, Simulator, Reasoning Inspector, Reflection Viewer, Benchmarks, Marketplace,
ELIZA Companion Chat, Cognitive Shell, and Decision Reasoning Traces,
while serving the Studio SPA static assets.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import sys
from urllib.parse import parse_qs, urlparse

# Add parent dir to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from companion.manager import ConversationManager
from companion.shell import CognitiveShell
from ELIZA_OBJECTS import Action, Belief, Goal, Memory, Outcome, Plan
from ecos.benchmarks.evaluator import CognitiveEvaluator
from ecos.benchmarks.suite import CognitiveBenchmarkSuite
from ecos.cfs.filesystem import CognitiveFilesystem
from ecos.civilization.minds import SpecializedMind
from ecos.compiler.compiler import CognitiveCompiler
from ecos.cvm.vm import CognitiveCPU
from ecos.learning.adaptive_pipeline import AdaptiveLearningPipeline
from ecos.marketplace.manager import CognitiveMarketplaceManager
from ecos.memory.hierarchy import CognitiveMemoryHierarchy
from ecos.os.kernel_os import ECOSOperatingSystem
from ecos.planning.planner import ECOSPlanner
from ecos.reasoning.engine import ECOSReasoner
from ecos.science.engine import ScientificEngine
from ecos.simulation.simulator import ECOSSimulator
from ecos.strategies.library import StrategyLibrary
from ecos.world.graph import ECOSWorldModel

# Global ECOS Runtime & Companion Instances
ecos_os = ECOSOperatingSystem()
ecos_os.boot()
marketplace = CognitiveMarketplaceManager()
marketplace.install("planner")
marketplace.install("scientist")

conversation_mgr = ConversationManager()
cognitive_shell = CognitiveShell()


class ELIZAStudioRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler serving Studio API JSON endpoints and static SPA files."""

    def _set_headers(self, content_type: str = "application/json", status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path.startswith("/api/"):
            self._handle_api_get(path, parsed_path.query)
        else:
            self._serve_static_file(path)

    def do_POST(self) -> None:
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        content_length = int(self.headers.get("Content-Length", 0))
        body_data = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            payload = json.loads(body_data)
        except Exception:
            payload = {}

        if path == "/api/goals/create":
            goal_text = payload.get("goal", "Build ECOS Kernel")
            res = ecos_os.run_goal(goal_text, priority=payload.get("priority", 10))
            self._set_headers()
            self.wfile.write(json.dumps({"status": "SUCCESS", "execution": res}).encode("utf-8"))

        elif path == "/api/chat":
            user_msg = payload.get("message", "Hello ELIZA")
            assistant_id = payload.get("assistant", "architect")
            conversation_mgr.set_assistant(assistant_id)
            try:
                chat_res = conversation_mgr.process_message(user_msg)
                trace_obj = chat_res["trace"]
                chat_res["trace"] = {
                    "trace_id": trace_obj.trace_id,
                    "goal_description": trace_obj.goal_description,
                    "evidence": trace_obj.evidence,
                    "alternatives": trace_obj.alternatives,
                    "chosen_option": trace_obj.chosen_option,
                    "confidence": trace_obj.confidence,
                    "assumptions": trace_obj.assumptions,
                }
            except Exception as e:
                print(f"Error processing message: {e}")
                chat_res = {
                    "response": f"SYSTEM ERROR: The cognitive engine encountered an error. This is likely an LLM Rate Limit (429 Too Many Requests). Wait a minute and try again.\nDetails: {e}",
                    "state": "error"
                }

            self._set_headers()
            self.wfile.write(json.dumps({"status": "SUCCESS", "chat": chat_res}).encode("utf-8"))

        elif path == "/api/shell/exec":
            cmd = payload.get("command", "/help")
            shell_res = cognitive_shell.execute_command(cmd)
            self._set_headers()
            self.wfile.write(json.dumps({"status": "SUCCESS", "result": shell_res}).encode("utf-8"))

        elif path == "/api/simulator/run":
            scenario = payload.get("scenario", "Default Scenario")
            sim = ECOSSimulator()
            p = Plan(id=f"plan-{scenario[:5]}", estimated_cost=1.5, risk=0.15)
            res = sim.simulate(p, [])
            res["scenario"] = scenario
            self._set_headers()
            self.wfile.write(json.dumps({"status": "SUCCESS", "simulation": res}).encode("utf-8"))

        elif path == "/api/marketplace/install":
            pkg = payload.get("package", "planner")
            installed = marketplace.install(pkg)
            self._set_headers()
            self.wfile.write(json.dumps({"status": "SUCCESS" if installed else "FAILED", "installed": marketplace.list_installed()}).encode("utf-8"))

        else:
            self._set_headers(status=404)
            self.wfile.write(json.dumps({"error": "POST Endpoint Not Found"}).encode("utf-8"))

    def _handle_api_get(self, path: str, query_str: str) -> None:
        params = parse_qs(query_str)
        self._set_headers()

        if path == "/api/assistants":
            data = {
                "current": conversation_mgr.current_assistant.id,
                "assistants": [
                    {"id": a.id, "name": a.name, "purpose": a.purpose}
                    for a in conversation_mgr.assistants.values()
                ],
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))

        elif path == "/api/dashboard":
            processes = []
            for pid, proc in ecos_os.active_processes.items():
                processes.append({
                    "pid": pid,
                    "name": proc.name,
                    "priority": "HIGH" if proc.priority > 5 else "NORMAL",
                    "status": proc.state.name,
                    "cpu_pct": 0.0,
                    "mem_mb": 0.0,
                })
            
            data = {
                "kernel_status": "ONLINE",
                "uptime_seconds": 0,
                "active_processes": processes,
                "active_thought": {
                    "current_goal": list(ecos_os.active_processes.values())[0].goal.description if ecos_os.active_processes else "Idle",
                    "subroutines": [],
                    "confidence_pct": 100,
                    "assumptions_count": 0,
                    "next_action": "Awaiting Input",
                },
                "cpu_usage_pct": len(processes) * 10,
                "memory_usage_mb": sum([t.current_count for t in ecos_os.memory_hierarchy.tiers.values()]),
                "reasoning_stage": "IDLE" if not processes else "EXECUTING",
                "scheduler_queue_depth": len(ecos_os.active_processes),
                "active_modules_count": 5,
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))

        elif path == "/api/state":
            goals = []
            for pid, proc in ecos_os.active_processes.items():
                if proc.goal:
                    goals.append({
                        "id": proc.goal.id,
                        "description": proc.goal.description,
                        "priority": proc.goal.priority,
                        "status": "active"
                    })
            data = {
                "runtime_id": getattr(ecos_os, 'runtime_id', 'sys'),
                "goals": goals,
                "agents": [{"id": "planner", "role": "planner"}], # simplified for now
                "memory_tiers": list(ecos_os.memory_hierarchy.tiers.keys())
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))

        elif path == "/api/stream":
            self.send_response(200)
            self.send_header('Content-type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            import queue
            client_queue = queue.Queue()
            
            def sse_callback(event):
                client_queue.put(event)
                
            sub_id = ecos_os.event_bus.subscribe(sse_callback)
            
            try:
                while True:
                    try:
                        event = client_queue.get(timeout=1.0)
                        data = event.model_dump_json()
                        self.wfile.write(f"event: {event.event_type.value}\n".encode('utf-8'))
                        self.wfile.write(f"data: {data}\n\n".encode('utf-8'))
                        self.wfile.flush()
                    except queue.Empty:
                        self.wfile.write(b": keepalive\n\n")
                        self.wfile.flush()
            except Exception as e:
                # Client disconnected or broken pipe
                pass
            finally:
                ecos_os.event_bus.unsubscribe(sub_id)
            return

        elif path == "/api/dashboard":
                "succeeded": False,
                "wrong_assumptions": [],
                "lessons_learned": [],
                "learning_candidates": [],
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))

        elif path == "/api/benchmarks":
            suite = CognitiveBenchmarkSuite()
            res = suite.run_suite()
            self.wfile.write(json.dumps(res.to_dict()).encode("utf-8"))

        elif path == "/api/models":
            registry = ecos_os.model_router.registry
            data = {
                "active_models": [
                    {
                        "name": m.name,
                        "provider": m.provider,
                        "reasoning": m.reasoning.value,
                        "coding": m.coding.value,
                        "speed": m.speed.value,
                        "cost": m.cost,
                        "context_window_k": m.context_window_k,
                        "is_local": m.is_local,
                        "recommended_tasks": m.recommended_tasks,
                    }
                    for m in registry.list_all()
                ]
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))

        elif path == "/api/marketplace":
            data = {
                "installed": marketplace.list_installed(),
                "available": marketplace.available_packages,
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))

        else:
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))

    def _serve_static_file(self, path: str) -> None:
        public_dir = os.path.join(os.path.dirname(__file__), "public")

        if path in ["/", "", "/index.html"]:
            file_path = os.path.join(public_dir, "index.html")
            content_type = "text/html"
        else:
            rel_path = path.lstrip("/")
            file_path = os.path.join(public_dir, rel_path)
            if rel_path.endswith(".css"):
                content_type = "text/css"
            elif rel_path.endswith(".js"):
                content_type = "application/javascript"
            elif rel_path.endswith(".png"):
                content_type = "image/png"
            elif rel_path.endswith(".svg"):
                content_type = "image/svg+xml"
            else:
                content_type = "text/plain"

        if os.path.exists(file_path) and os.path.isfile(file_path):
            self._set_headers(content_type=content_type)
            with open(file_path, "rb") as f:
                self.wfile.write(f.read())
        else:
            index_path = os.path.join(public_dir, "index.html")
            if os.path.exists(index_path):
                self._set_headers(content_type="text/html")
                with open(index_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self._set_headers(content_type="text/plain", status=404)
                self.wfile.write(b"404 Not Found")


def run_studio_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    server_address = (host, port)
    httpd = HTTPServer(server_address, ELIZAStudioRequestHandler)
    print(f"==================================================")
    print(f"  ELIZA COMPANION & STUDIO v0.1 — ECOS CONTROL DECK")
    print(f"  Running at: http://{host}:{port}/")
    print(f"==================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()


if __name__ == "__main__":
    run_studio_server()
