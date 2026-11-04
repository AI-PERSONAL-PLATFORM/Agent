"""Development chat UI from Pydantic AI's `Agent.to_web()`, served apart from the API."""

from app.agents.assistant import get_assistant_agent
from app.agents.base import AgentDeps

app = get_assistant_agent().to_web(deps=AgentDeps(chat_id="web-ui"))
