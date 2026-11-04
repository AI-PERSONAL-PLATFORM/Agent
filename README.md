# AI Personal Platform

A personal AI platform with agent chat, saved conversations, attachments, and configurable tools. Built with FastAPI/Pydantic AI.

Built using my own knowledge and AI assistance for code, design, and documentation.

## Quick start

Install [mise](https://mise.jdx.dev/) and Docker Compose, then run from the project root:

```bash
cp .env.example .env
mise trust
mise install
```
Set `OPENCODE_API_KEY` in `.env`. The example already provides the URLs needed for Docker.

```bash
mise local
```

Set `LOGFIRE_TOKEN` in `.env` to enable optional agent tracing.

## Useful commands

| Command | Purpose |
| --- | --- |
| `mise local` | Build and start the Docker stack |
| `mise ps` | Show service status |
| `docker compose down` | Stop the stack and keep database data |
| `mise setup` | Install dependencies for native development and checks |
| `mise dev` | Run the agents service local |
| `mise check` | Run lint, format check, typecheck, and tests |

## Service documentation

- [Agents](agents/README.md): models, tools, tests, and Logfire setup.
