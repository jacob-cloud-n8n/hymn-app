# AGENTS.md - OpenCode Local Workspace

## Purpose

This workspace supports the OpenCode remote coding deployment documented in
KB-Vault. The current assigned task is preparation and deployment of OpenAB
with OpenCode on Zeabur.

## Source Of Truth

Use the Mac copy of KB-Vault:

```text
/Users/jacob/Library/CloudStorage/GoogleDrive-chen.uvtai12@gmail.com/我的雲端硬碟/wiki/KB-Vault
```

Before taking action on an assigned backup task, read:

1. `團隊交接.md`
2. `Wiki駕駛艙.md`
3. `AGENTS.md`
4. `Projects/open-code/AGENTS.md`
5. `Projects/open-code/_worklog.md`

## Operating Rules

- Do not invent or reassign tasks; follow the current handoff entry.
- Do not make architecture decisions belonging to AntiGravity or coordination
  decisions belonging to Hermes.
- Keep changes narrow and verify every claimed artifact on disk.
- Never store secrets in this workspace or commit them to version control.
- When the deployment task is started or finished, update only the status locations
  permitted by the KB-Vault handoff rules.
- Validate deployment instructions against official template documentation before
  entering credentials or creating services.

## Current Workspace State

- Initialized: 2026-05-27
- Runtime/application scaffold: intentionally absent
- Deployment target: Zeabur OpenAB + OpenCode
- Active assignment: OpenCode deployment is verified; OpenCode -> Hermes direct
  API channel is verified as of 2026-05-29.
- Deployment route: Discord native integration; Telegram gateway intentionally
  not used after evaluating additional operational risk.
- Default model: DeepSeek API `deepseek-v4-pro`; use `deepseek-v4-flash` only
  for low-risk speed-oriented tasks.
- Hermes integration: OpenCode uses Zeabur private variables
  `HERMES_BASE_URL` and `HERMES_API_KEY`, passed into the agent runtime through
  OpenAB `[agent].inherit_env`. Never store or print the key value.
