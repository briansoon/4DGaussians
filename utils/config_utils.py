"""Lightweight loader for the Python experiment configs used by 4DGaussians.

This supports the subset of MMCV's ``Config.fromfile`` used by this project:
Python config files and recursive ``_base_`` inheritance.
"""

from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from types import ModuleType
from typing import Any


def load_config(filename: str | Path) -> dict[str, Any]:
    """Load a Python config file, resolving its optional ``_base_`` configs.

    Config files are executed just as they were by MMCV, so they must be
    treated as trusted project files.
    """
    return _load_config(Path(filename).resolve(), set())


def _load_config(path: Path, loading: set[Path]) -> dict[str, Any]:
    if path in loading:
        chain = " -> ".join(str(item) for item in (*loading, path))
        raise ValueError(f"Circular config inheritance: {chain}")
    if not path.is_file():
        raise FileNotFoundError(f"Config file not found: {path}")
    if path.suffix != ".py":
        raise ValueError(f"Only Python config files are supported: {path}")

    namespace: dict[str, Any] = {"__file__": str(path), "__name__": "__config__"}
    exec(compile(path.read_text(encoding="utf-8"), path, "exec"), namespace)

    base_files = namespace.pop("_base_", None)
    config = {
        key: value
        for key, value in namespace.items()
        if not key.startswith("__") and not isinstance(value, ModuleType)
    }

    merged: dict[str, Any] = {}
    if base_files:
        if isinstance(base_files, (str, Path)):
            base_files = [base_files]
        if not isinstance(base_files, (list, tuple)):
            raise TypeError(f"_base_ must be a path or a list of paths in {path}")
        for base_file in base_files:
            merged = _merge_config(
                merged, _load_config((path.parent / base_file).resolve(), loading | {path})
            )

    return _merge_config(merged, config)


def _merge_config(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    """Recursively merge config mappings, including MMCV's ``_delete_`` flag."""
    merged = deepcopy(dict(base))
    for key, value in override.items():
        if isinstance(value, Mapping):
            value = dict(value)
            delete_base = value.pop("_delete_", False)
            if not delete_base and isinstance(merged.get(key), Mapping):
                merged[key] = _merge_config(merged[key], value)
            else:
                merged[key] = deepcopy(value)
        else:
            merged[key] = deepcopy(value)
    return merged
