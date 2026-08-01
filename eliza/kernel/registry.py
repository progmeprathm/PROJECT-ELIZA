"""
ECOS Kernel Service Registry & Dependency Resolver.
Enforces Section IV, XVII, and XIX of ELIZA_KERNEL_SPEC.md.
"""

from typing import Dict, List, Optional
import logging

from eliza.kernel.spec import ICognitiveModule, ModuleManifest, ModuleState

logger = logging.getLogger(__name__)


class ServiceRegistry:
    """
    Service Registry tracks registered cognitive modules, capability discovery, and dependency graphs.
    Rejects registration if circular dependencies exist (Section XVII).
    """

    def __init__(self) -> None:
        self._modules: Dict[str, ICognitiveModule] = {}
        self._manifests: Dict[str, ModuleManifest] = {}

    def register_module(self, module: ICognitiveModule) -> None:
        m = module.manifest
        if m.module_id in self._modules:
            raise ValueError(f"Module '{m.module_id}' is already registered in ServiceRegistry.")

        # Check dependencies
        for dep in m.dependencies:
            if dep not in self._modules:
                logger.warning(f"Module '{m.module_id}' has unresolved dependency '{dep}'")

        self._modules[m.module_id] = module
        self._manifests[m.module_id] = m

        # Validate dependency graph (prohibit cycles)
        if self._detect_circular_dependency():
            del self._modules[m.module_id]
            del self._manifests[m.module_id]
            raise ValueError(f"Registration of module '{m.module_id}' introduced a circular dependency!")

    def get_module(self, module_id: str) -> Optional[ICognitiveModule]:
        return self._modules.get(module_id)

    def list_registered_modules(self) -> List[ModuleManifest]:
        return list(self._manifests.values())

    def discover_by_capability(self, capability: str) -> List[ICognitiveModule]:
        return [
            mod for mod_id, mod in self._modules.items()
            if capability in self._manifests[mod_id].capabilities
        ]

    def _detect_circular_dependency(self) -> bool:
        """Kahn's or DFS cycle detection algorithm on dependency graph."""
        visited = set()
        rec_stack = set()

        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            manifest = self._manifests.get(node)
            if manifest:
                for dep in manifest.dependencies:
                    if dep in self._manifests:
                        if dep not in visited:
                            if dfs(dep):
                                return True
                        elif dep in rec_stack:
                            return True
            rec_stack.remove(node)
            return False

        for mod_id in self._manifests:
            if mod_id not in visited:
                if dfs(mod_id):
                    return True
        return False
