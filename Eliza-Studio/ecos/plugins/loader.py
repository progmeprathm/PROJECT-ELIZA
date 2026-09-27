"""
Plugin loader and base plugin interface for ELIZA v0.1.
Enforces ELIZA_PLUGIN_SPEC.md.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import logging

from eliza.kernel.spec import ICognitiveModule, ModuleHealth, ModuleManifest, ModuleState

logger = logging.getLogger(__name__)


class BasePlugin(ICognitiveModule, ABC):
    def __init__(self, plugin_id: str, version: str = "1.0.0", capabilities: Optional[List[str]] = None) -> None:
        self._id = plugin_id
        self._version = version
        self._capabilities = capabilities or []
        self._state = ModuleState.CREATED

    @property
    def manifest(self) -> ModuleManifest:
        return ModuleManifest(module_id=self._id, version=self._version, capabilities=self._capabilities)

    @property
    def state(self) -> ModuleState:
        return self._state

    def health(self) -> ModuleHealth:
        return ModuleHealth(module_id=self._id, status="Healthy")


class PluginLoader:
    def __init__(self) -> None:
        self._plugins: Dict[str, BasePlugin] = {}

    def load_plugin(self, plugin: BasePlugin) -> bool:
        self._plugins[plugin.manifest.module_id] = plugin
        logger.info(f"Loaded plugin: {plugin.manifest.module_id}")
        return True

    def get_plugin(self, plugin_id: str) -> Optional[BasePlugin]:
        return self._plugins.get(plugin_id)
