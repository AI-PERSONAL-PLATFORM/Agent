"""Tool and skill catalog entries listed by `GET /agents/{agent_id}/tools` and `/skills`."""

from collections.abc import Iterable
from typing import Any

from pydantic import BaseModel
from pydantic_ai import FunctionToolset
from pydantic_ai.toolsets import AgentToolset
from pydantic_ai_harness.skills import Skills


class AgentTool(BaseModel):
    name: str
    label: str
    description: str
    deferred: bool = False
    requires_approval: bool = False


def catalog_from_toolsets(toolsets: Iterable[AgentToolset[Any] | None]) -> list[AgentTool]:
    """List the tools of the function toolsets among `toolsets`, skipping any other entry.

    A tool's description is its docstring and `metadata={"label": ...}` sets its label.
    `deferred` and `requires_approval` mirror the tool's native `defer_loading` and
    `requires_approval`.
    """
    return [
        AgentTool(
            name=tool.name,
            label=(tool.metadata or {}).get("label", tool.name),
            description=tool.description or "",
            deferred=tool.defer_loading,
            requires_approval=tool.requires_approval,
        )
        for toolset in toolsets
        if isinstance(toolset, FunctionToolset)
        for tool in toolset.tools.values()
    ]


class AgentSkill(BaseModel):
    name: str
    description: str
    model_invocable: bool
    user_invocable: bool


async def catalog_from_skills(skills: Skills[Any]) -> list[AgentSkill]:
    """List the skills `skills` offers, read with `Skills.load()` as a run would read them."""
    catalog = await skills.load()
    return [
        AgentSkill(
            name=skill.name,
            description=skill.description,
            model_invocable=skill.model_invocable,
            user_invocable=skill.user_invocable,
        )
        for skill in catalog.skills
    ]
