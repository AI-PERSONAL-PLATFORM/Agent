"""Streaming and assertion helpers for the live agent API test."""

import json
from typing import Any

import httpx
from ag_ui.core import RunAgentInput

from app.agents.assistant import AgentResponse

type StreamEvent = dict[str, Any]


def stream_agent_events(client: httpx.Client, run_input: RunAgentInput) -> list[StreamEvent]:
    payload = run_input.model_dump(mode="json", by_alias=True)
    with client.stream(
        "POST", "/agents/assistant", headers={"Accept": "text/event-stream"}, json=payload
    ) as response:
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/event-stream")
        events: list[StreamEvent] = []
        for line in response.iter_lines():
            if line.startswith("data: "):
                events.append(json.loads(line.removeprefix("data: ")))
        return events


def assert_successful_run(events: list[StreamEvent], run_input: RunAgentInput) -> None:
    assert events
    assert events[0]["type"] == "RUN_STARTED"
    assert events[0]["threadId"] == run_input.thread_id
    assert events[0]["runId"] == run_input.run_id
    for event in events:
        assert event["type"] != "RUN_ERROR"
    assert events[-1]["type"] == "RUN_FINISHED"
    assert events[-1]["threadId"] == run_input.thread_id
    assert events[-1]["runId"] == run_input.run_id
    assert events[-1]["outcome"]["type"] == "success"


def assert_agent_reply(events: list[StreamEvent]) -> AgentResponse:
    text_parts = []
    for event in events:
        if event["type"] == "TEXT_MESSAGE_CONTENT":
            text_parts.append(event["delta"])
    text = "".join(text_parts)
    assert text.strip()
    reply = AgentResponse.model_validate_json(text)
    assert reply.message.strip()
    return reply
