## Summary

<!-- Describe the change to the agents service and why it is needed. -->

## Changes

<!-- List the important changes: agents, specs/prompts, tools, routes, settings. -->

## Validation

- [ ] `mise -C agents run check` passes (lint, format-check, typecheck).
- [ ] `mise -C agents run test` passes.
- [ ] For changes to agent behavior, `mise -C agents run test-agent` passes against a real model, or the reason it was not run is noted below.
- [ ] Agent or prompt changes keep the `AgentResponse` contract and the AG-UI stream intact.
- [ ] `.env.example`, `README.md`, `AGENTS.md`, and `backend-schema.md` are updated if needed.
- [ ] No secrets, credentials, or database dependencies are added.

## Related issue

<!-- Link an issue, for example: Closes #123. -->
