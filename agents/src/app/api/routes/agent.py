"""Agent endpoint configuration and request validation."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from pydantic_ai.ui.ag_ui import AGUIAdapter
from starlette.requests import Request
from starlette.responses import Response

from app.agents import find_agent
from app.agents.base import AgentDeps, BaseAgent
from app.agents.base.catalog import AgentSkill, AgentTool, catalog_from_skills
from app.core.config import get_settings

settings = get_settings()
router = APIRouter()


def get_agent(agent_id: str) -> BaseAgent[Any]:
    agent = find_agent(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail=f"Unknown agent: {agent_id}.")
    if not settings.model_configured:
        raise HTTPException(
            status_code=503,
            detail=(
                "Set MODEL_PROVIDER, AGENT_MODEL, and the provider's API key and base URL "
                "to run agents."
            ),
        )
    return agent


AgentDep = Annotated[BaseAgent[Any], Depends(get_agent)]


@router.get("/agents/{agent_id}/tools")
async def list_tools(agent: AgentDep) -> list[AgentTool]:
    return agent.tool_catalog


@router.get("/agents/{agent_id}/skills")
async def list_skills(agent: AgentDep) -> list[AgentSkill]:
    return await catalog_from_skills(agent.skills)


@router.post("/agents/{agent_id}")
async def run_agent(agent: AgentDep, request: Request) -> Response:
    try:
        adapter = await AGUIAdapter[AgentDeps, Any].from_request(request, agent=agent)
    except ValidationError as error:
        return Response(
            error.json(include_input=False), status_code=422, media_type="application/json"
        )
    run_input = adapter.run_input
    if not run_input.thread_id:
        raise HTTPException(status_code=422, detail="threadId must not be empty.")

    deps = AgentDeps(session_id=run_input.thread_id)
    stream = adapter.run_stream(deps=deps, usage_limits=settings.usage_limits)
    return adapter.streaming_response(stream)
