from pathlib import Path
from unittest.mock import Mock

import tomllib

from victor_sdk import VictorPlugin

from victor_research.assistant import ResearchAssistant
from victor_research.plugin import ResearchPlugin, plugin


def _entry_points() -> dict:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    return pyproject["project"]["entry-points"]


def test_pyproject_registers_plugin_instance_entry_point() -> None:
    entry_points = _entry_points()

    assert entry_points["victor.plugins"]["research"] == "victor_research.plugin:plugin"


def test_pyproject_registers_canonical_runtime_extension_entry_points() -> None:
    entry_points = _entry_points()

    assert entry_points["victor.prompt_contributors"]["research"] == (
        "victor_research.prompts:ResearchPromptContributor"
    )
    assert entry_points["victor.mode_configs"]["research"] == (
        "victor_research.mode_config:ResearchModeConfigProvider"
    )
    assert entry_points["victor.workflow_providers"]["research"] == (
        "victor_research.workflows:ResearchWorkflowProvider"
    )
    assert entry_points["victor.capability_providers"]["research"] == (
        "victor_research.capabilities:ResearchCapabilityProvider"
    )
    assert entry_points["victor.team_spec_providers"]["research"] == (
        "victor_research.teams:ResearchTeamSpecProvider"
    )
    assert entry_points["victor.framework.teams.providers"]["research"] == (
        "victor_research.teams:ResearchTeamSpecProvider"
    )


def test_plugin_implements_protocol_and_registers_vertical() -> None:
    context = Mock()

    assert isinstance(plugin, VictorPlugin)
    assert isinstance(plugin, ResearchPlugin)
    assert plugin.name == "research"

    plugin.register(context)

    context.register_vertical.assert_called_once_with(ResearchAssistant)
