from collections.abc import Sequence
from pathlib import Path
from typing import Any, Literal

from pydantic_ai import Agent
from pydantic_ai.capabilities import AbstractCapability
from pydantic_ai.workspaces import LocalWorkspaceBackend
from pydantic_ai_harness import ArtifactScanner
from pydantic_ai_harness.skills import Skills

from app.agents.base.catalog import catalog_from_toolsets
from app.agents.base.model import AgentDeps, agent_model_settings, get_agent_model

AGENTS_DIR = Path(__file__).resolve().parents[1]


def skills_capability(skills: Literal["all"] | list[str]) -> Skills[AgentDeps]:
    """`Skills` over `app/agents/skills/`: every skill, only the listed ones, or none for `[]`.

    `ArtifactScanner` leaves out any skill whose description or body looks like prompt injection,
    credential exfiltration, or hidden content.
    """
    include: list[str] | None
    if skills == "all":
        include = None
    else:
        include = skills
    workspace = LocalWorkspaceBackend(AGENTS_DIR)
    return Skills[AgentDeps](
        "skills", include=include, workspace=workspace, scanner=ArtifactScanner()
    )


class BaseAgent[OutputT](Agent[AgentDeps, OutputT]):
    """Shared-model agent with `AgentDeps`, its tool catalog, and the skills it selects."""

    def __init__(
        self,
        *,
        skills: Literal["all"] | list[str],
        capabilities: Sequence[AbstractCapability[AgentDeps]] = (),
        **kwargs: Any,
    ) -> None:
        self.skills = skills_capability(skills)
        super().__init__(
            get_agent_model(),
            deps_type=AgentDeps,
            model_settings=agent_model_settings,
            capabilities=[self.skills, *capabilities],
            **kwargs,
        )
        self.tool_catalog = catalog_from_toolsets(self.toolsets)
