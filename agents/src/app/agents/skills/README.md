# Agent skills

Each child directory holding a `SKILL.md` is an [Agent Skill](https://agentskills.io/specification)
offered through the `Skills` capability from `pydantic-ai-harness` to each agent that selects it with `skills="all"` or `skills=["<name>", ...]` (`skills=[]` offers none). The model
sees each skill's name and description and loads its body with the `load_capability` tool.

```text
skills/
  release-notes/
    SKILL.md
```

```markdown
---
name: release-notes
description: Write release notes from a list of merged changes.
---

Group the changes by type and lead with user-facing changes.
```

Skills that look like prompt injection, credential exfiltration, or hidden content are left out by `ArtifactScanner`. `GET /agents/{agent_id}/skills` lists the skills an agent offers.

The directory name must match `name`: lowercase letters, numbers, and single hyphens.
