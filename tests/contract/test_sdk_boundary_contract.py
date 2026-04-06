from __future__ import annotations

from pathlib import Path


_MODULES = [
    "victor_research/assistant.py",
    "victor_research/protocols.py",
    "victor_research/prompts.py",
    "victor_research/safety.py",
    "victor_research/safety_enhanced.py",
]

_BANNED_IMPORTS = (
    "victor.core.verticals.protocols",
    "victor.core.verticals.registration",
)


def test_sdk_boundary_modules_avoid_core_vertical_protocol_imports() -> None:
    for module in _MODULES:
        source = Path(module).read_text(encoding="utf-8")
        for banned in _BANNED_IMPORTS:
            assert banned not in source, f"{module} still imports {banned}"
