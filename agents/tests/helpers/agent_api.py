"""Request, streaming, and assertion helpers for Vercel AI agent API tests."""

import json
from collections.abc import Iterable
from typing import Any
from uuid import uuid4

import httpx
from pydantic_ai.ui.vercel_ai.request_types import SubmitMessage, TextUIPart, UIMessage

from app.agents.assistant import AgentResponse

type StreamEvent = dict[str, Any]


def user_message(text: str) -> UIMessage:
    return UIMessage(id=str(uuid4()), role="user", parts=[TextUIPart(text=text)])


def parse_events(lines: Iterable[str]) -> list[StreamEvent]:
    """Decode SSE `data:` lines, skipping the closing `[DONE]` marker."""
    events: list[StreamEvent] = []
    for line in lines:
        if line.startswith("data: ") and line != "data: [DONE]":
            events.append(json.loads(line.removeprefix("data: ")))
    return events


def stream_agent_events(client: httpx.Client, run_input: SubmitMessage) -> list[StreamEvent]:
    payload = run_input.model_dump(mode="json", by_alias=True, exclude_none=True)
    with client.stream(
        "POST", "/agents/assistant", headers={"Accept": "text/event-stream"}, json=payload
    ) as response:
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/event-stream")
        assert response.headers["x-vercel-ai-ui-message-stream"] == "v1"
        return parse_events(response.iter_lines())


def assert_successful_run(events: list[StreamEvent]) -> None:
    assert events
    assert events[0]["type"] == "start"
    for event in events:
        assert event["type"] != "error"
    assert events[-1]["type"] == "finish"
    assert events[-1]["finishReason"] == "stop"


def assert_agent_reply(events: list[StreamEvent]) -> AgentResponse:
    text_parts = []
    for event in events:
        if event["type"] == "text-delta":
            text_parts.append(event["delta"])
    text = "".join(text_parts)
    assert text.strip()
    reply = AgentResponse.model_validate_json(text)
    assert reply.message.strip()
    return reply
