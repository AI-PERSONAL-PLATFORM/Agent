"""Logfire tracing for the agents service, enabled for cloud export by a write token."""

from typing import Any

import logfire
from fastapi import FastAPI, Request, WebSocket

from app.core.config import Settings


def _request_attributes(request: Request | WebSocket, attributes: dict[str, Any]) -> dict[str, Any]:
    return {}


def configure_telemetry(app: FastAPI, settings: Settings) -> None:
    token = settings.logfire_token.get_secret_value()
    logfire.configure(
        token=token or None,
        send_to_logfire=bool(token),
        service_name=settings.logfire_service_name,
        environment=settings.logfire_environment,
        console=False,
    )
    logfire.instrument_pydantic_ai(
        include_content=settings.logfire_include_content,
        include_binary_content=True,
    )
    logfire.instrument_httpx()
    logfire.instrument_fastapi(
        app,
        excluded_urls=r"/health$",
        request_attributes_mapper=_request_attributes,
    )
