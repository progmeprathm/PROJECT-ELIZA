"""
ECOS Kernel Package for ELIZA Cognitive Operating System.
Enforces ELIZA_KERNEL_SPEC.md Version 1.0 (Canonical Runtime Architecture).
"""

from eliza.kernel.spec import ICognitiveModule, ModuleState, TaskState
from eliza.kernel.registry import ServiceRegistry
from eliza.kernel.scheduler import KernelScheduler
from eliza.kernel.state_manager import StateManager
from eliza.kernel.ecos_kernel import ECOSKernel

__all__ = [
    "ICognitiveModule",
    "ModuleState",
    "TaskState",
    "ServiceRegistry",
    "KernelScheduler",
    "StateManager",
    "ECOSKernel",
]
