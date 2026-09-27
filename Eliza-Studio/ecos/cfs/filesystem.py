"""
Layer 7: Cognitive Filesystem (CFS) implementation.
Provides an inspectable virtual filesystem hierarchy:
/memory/, /beliefs/, /goals/, /plans/, /policies/, /experiences/, /skills/, /world/, /agents/.
"""

from typing import Any, Dict, List, Optional


class CognitiveFilesystem:
    """
    Virtual inspectable filesystem tree.
    No hidden state. Everything is browsable by virtual path.
    """

    def __init__(self) -> None:
        self._tree: Dict[str, Dict[str, Any]] = {
            "/memory": {},
            "/beliefs": {},
            "/goals": {},
            "/plans": {},
            "/policies": {},
            "/experiences": {},
            "/skills": {},
            "/world": {},
            "/agents": {},
        }

    def write(self, path: str, obj: Any) -> None:
        parts = [p for p in path.split("/") if p]
        if not parts:
            raise ValueError(f"Invalid path '{path}'")

        root_dir = f"/{parts[0]}"
        if root_dir not in self._tree:
            self._tree[root_dir] = {}

        file_name = "/".join(parts[1:]) if len(parts) > 1 else str(getattr(obj, "id", "data"))
        self._tree[root_dir][file_name] = obj

    def read(self, path: str) -> Optional[Any]:
        parts = [p for p in path.split("/") if p]
        if not parts:
            return None

        root_dir = f"/{parts[0]}"
        if root_dir not in self._tree:
            return None

        file_name = "/".join(parts[1:]) if len(parts) > 1 else ""
        if not file_name:
            return self._tree[root_dir]
        return self._tree[root_dir].get(file_name)

    def list_dir(self, directory: str) -> List[str]:
        dir_name = directory if directory.startswith("/") else f"/{directory}"
        return list(self._tree.get(dir_name, {}).keys())

    def get_full_tree(self) -> Dict[str, int]:
        return {d: len(contents) for d, contents in self._tree.items()}
