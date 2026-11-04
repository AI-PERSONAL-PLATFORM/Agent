# Agents

FastAPI and Pydantic AI service using Python and uv. Runs agents over the Vercel AI SDK UI message stream protocol (`VercelAIAdapter`, SDK v6); it is stateless and the client sends the full message history on each run.

## Quick start

For Docker, follow the [root quick start](../README.md). For native development, run `mise setup` from the repository root, then run:

```bash
cp agents/.env.example agents/.env
```

Set `OPENCODE_API_KEY` in `agents/.env`. Check `OPENCODE_BASE_URL` for your model provider, then start the service:

```bash
mise -C agents run dev
```

Open <http://localhost:8000/docs> for interactive API documentation. Native execution loads `agents/.env`; Docker uses the root `.env`.

## Agent configuration

- **Agents:** Each agent is a module in [src/app/agents](src/app/agents) that builds a `BaseAgent` with its `name`, `description`, and `instructions`, as [assistant.py](src/app/agents/assistant.py) does. Its `name` is the agent ID. Register it in [src/app/agents/__init__.py](src/app/agents/__init__.py).
- **Web UI (optional):** `mise web-ui` from the repository root (or `mise -C agents run web-ui`) serves Pydantic AI's chat UI for the assistant at http://127.0.0.1:8001, using the root `.env`. It is a separate app in [src/app/web_ui.py](src/app/web_ui.py); delete that file and the `web-ui` tasks in `mise.toml` and the root `mise.toml` to remove it.
- **Model:** `MODEL_PROVIDER` is `opencode` (default) or `ollama`, and `AGENT_MODEL` names the model; its default is in [config.py](src/app/core/config.py). For Ollama, also set `OLLAMA_BASE_URL`.
- **Limits:** each run stops after `AGENT_REQUEST_LIMIT` model requests (default 20) or `AGENT_TOTAL_TOKENS_LIMIT` tokens (default 200000), counting the summarize tool's own request.

## API

| Method | Path                         | Purpose                                 |
| ------ | ---------------------------- | --------------------------------------- |
| GET    | `/`                          | Redirect to the API docs at `/docs`     |
| GET    | `/health`                    | Check process health                    |
| POST   | `/agents/{agent_id}`         | Run an agent and stream Vercel AI chunks |
| GET    | `/agents/{agent_id}/tools`   | List the agent's tool catalog           |
| GET    | `/agents/{agent_id}/skills`  | List the skills the agent offers        |

## Tracing

Set `LOGFIRE_TOKEN` to your project's write token to enable optional tracing for FastAPI, Pydantic AI, and outgoing HTTP requests. Leave it empty to disable cloud export. Use the root `.env` for Docker or `agents/.env` for native development, then restart the service; rebuild the agents container for Docker.

`LOGFIRE_ENVIRONMENT` labels the environment. Model prompts, replies, and tool content are excluded by default; set `LOGFIRE_INCLUDE_CONTENT=true` to capture them. View requests and model activity in your Logfire project's Live view.

## Useful commands

Run these from the repository root:

| Command                         | Purpose                                                |
| ------------------------------- | ------------------------------------------------------ |
| `mise -C agents run dev`        | Start Uvicorn with reload                              |
| `mise -C agents run check`      | Run Ruff, formatting, mypy, and tests                  |
| `mise -C agents run test`       | Run pytest; skip the live test without `AGENT_API_URL` |
| `mise -C agents run test-agent` | Run the live model test                |
| `mise -C agents run logs`       | Follow container logs                                  |

See [mise.toml](mise.toml) for all tasks.

## Live test

With the agents service running, export its host-accessible URL:

```bash
export AGENT_API_URL=http://127.0.0.1:8000
mise -C agents run test-agent
```

The test sends one real model request and checks matching thread/run IDs, the structured response, and successful completion.

The [Agents workflow](../.github/workflows/agents.yml) runs this test on relevant pull requests and manual dispatches. It requires the `OPENCODE_API_KEY` repository secret.
