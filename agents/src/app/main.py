from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.api.routes import agent_router, health_router
from app.core.config import get_settings
from app.core.telemetry import configure_telemetry

settings = get_settings()

app = FastAPI(title="AI Personal Platform", version="0.1.0")
app.include_router(health_router)
app.include_router(agent_router)

@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")

configure_telemetry(app, settings)
