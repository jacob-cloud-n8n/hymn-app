# OpenCode Project Cockpit

## Status

- Date: 2026-05-27
- Workspace: `2026 open-code`
- Mode: Discord remote coding deployed and verified
- Active task: task #2 - OpenAB + OpenCode Zeabur deployment completed

## Initialization Audit

Before initialization, this local workspace was empty and was not a Git
repository. A newly synchronized KB-Vault revision subsequently supplied the
active project identity and task:

- `團隊交接.md` v3.0 assigns Codex task #2 to deploy OpenAB + OpenCode on Zeabur.
- `Projects/open-code/OpenAB部署指南.md` documents the selected Discord deployment route.
- `Projects/open-code/_worklog.md` records the v3.0 remote coding upgrade.
- `知識庫/Tools/OpenCode使用教訓.md` records the reason asynchronous work is disallowed.

## Deployment Decision

The official `OpenAB OpenCode` template is Discord-first. Telegram support
would require an additional `OpenAB Gateway` service and webhook management.
Jacob selected Discord because its mobile app satisfies off-site access while
preserving the simpler official connection path.

Deployment also requires a model provider credential or an interactive OpenCode
login after the service is running.

For the default model, use the existing DeepSeek API access with
`deepseek-v4-pro`; reserve `deepseek-v4-flash` for lower-risk, speed-oriented
tasks. The official DeepSeek V4 API supports both IDs and deprecates the older
legacy aliases on 2026-07-24.

A Discord webhook URL was provided during setup, but OpenAB requires a Discord
bot token and allowed channel ID. Any exposed webhook URL must be rotated and
must not be used for deployment.

## Deployment Verification

- Zeabur `OpenAB OpenCode` template deployed successfully on 2026-05-27.
- Discord adapter is limited to the approved channel; user filtering was
  removed after the approved channel was confirmed.
- Discord exposed the selected `@opencode bot` target as a role mention, so its
  role ID was added to OpenAB `allowed_role_ids`.
- DeepSeek authentication is held as a Zeabur private variable, passed to
  OpenCode with `[agent].inherit_env`, and the default model is
  `deepseek/deepseek-v4-pro`.
- Direct OpenCode model test returned `OK`, then a Discord mention created a
  thread and returned the read-only test response.
- Operational caution: an API key inherited by the agent is accessible during
  agent execution; do not ask it to process untrusted prompts or files.

## Shutdown Summary - 2026-05-27

- Task #2 is complete: Discord -> OpenAB -> OpenCode -> DeepSeek V4 Pro was
  verified end to end with a read-only Discord reply.
- The reusable KB-Vault records were completed:
  `OpenAB部署指南.md`, `OpenAB部署懶人包.md`, and
  `OpenAB部署實戰紀錄-2026-05-27.md`.
- Resolved deployment pitfalls were documented: persistent `config.toml`,
  incorrect channel/user values, and Discord role mention triggering.
- The local workspace is not a Git repository, so no commit or push applies.
- Next operational guardrail: any first remote write task must be narrowly
  scoped and its produced changes reviewed by Jacob or Codex.

## Shutdown Summary - 2026-05-29

- Reviewed OpenCode and Hermes proposals for direct Zeabur-internal
  communication.
- Confirmed the Hermes gateway service identity from local project records:
  `service-6a0ab8c5cae74f9c179b5584`,
  `hermes-agent-gateway.zeabur.internal`, port `8080`.
- Verified the public Hermes gateway `/health` endpoint is healthy.
- Assessment: direct service-to-service networking is plausible for health
  checks, but not sufficient for agent messaging unless Hermes exposes a real
  message/task HTTP endpoint.
- Recommended next step: Hermes may perform read-only runtime inspection to
  identify any existing HTTP endpoint; do not open a new server, restart the
  gateway, clear memory, create cron jobs, or enable write automation without
  explicit approval and a rollback plan.
- KB-Vault was clean at shutdown. This local workspace is still not a Git
  repository, so no commit or push applies here.

## Shutdown Summary - 2026-05-29 Night

- Completed OpenCode -> Hermes direct API verification through the public
  Hermes gateway; Zeabur internal service DNS was not available from the
  OpenCode container.
- Confirmed the Hermes gateway exposes OpenAI-compatible endpoints on HTTPS:
  `/v1/models` and `/v1/chat/completions`, protected by Bearer auth.
- Added OpenCode Zeabur private variables `HERMES_BASE_URL` and
  `HERMES_API_KEY`; no secret values are stored in this workspace.
- Fixed the OpenAB agent runtime environment allowlist by adding
  `HERMES_BASE_URL` and `HERMES_API_KEY` to
  `/home/node/.config/openab/config.toml` under `[agent].inherit_env`.
- Re-tested after API key rotation: `GET /v1/models` returned HTTP 200 with
  `hermes-agent`, and `POST /v1/chat/completions` returned HTTP 200 with the
  expected `"Hermes received."` response.
- Current integration status: OpenCode -> Hermes one-way agent API channel is
  verified. Hermes -> OpenCode reverse channel remains a separate future
  design item; n8n/Discord can remain the short-term return path.
- Remaining documentation task: sync KB-Vault handoff and OpenCode worklog so
  task #4 no longer appears pending.

## Shutdown Summary - 2026-06-05

- Resolved OpenCode KB-Vault sync drift: OpenCode now uses HTTPS with
  `KB_VAULT_READ_TOKEN` read-only access and `git pull --rebase` from
  `/home/node/kb-vault` instead of SSH, because the Zeabur container lacks the
  `ssh` binary.
- Confirmed OpenAB agent env propagation requires `[agent].inherit_env`;
  `KB_VAULT_READ_TOKEN` must be allowlisted there before OpenCode can read it.
- Documented the incident in KB-Vault:
  `知識庫/Tools/團隊踩坑與故障排除紀錄.md` and
  `Projects/open-code/_worklog.md`, pushed as
  `fa623ab docs: record opencode kb-vault sync fix`.
- Added the durable OpenCode sync rule to
  `Projects/open-code/AGENTS.md`, pushed as
  `7f8a5fd docs: add opencode kb-vault sync rule`.
- Archived the reusable procedure as local Codex skill:
  `/Users/jacob/.codex/skills/opencode-kb-sync/SKILL.md`.
- No secrets were recorded in local project files, KB-Vault, or the skill.

## Created Locally

- `README.md` - purpose, current state, and startup reading order
- `AGENTS.md` - local guardrails and source-of-truth paths
- `.gitignore` - basic exclusions for possible future engineering tasks
- `docs/project-cockpit.md` - this audit record

## Deliberately Not Created

- No application framework or source code: deployment uses Zeabur templates.
- No Git repository or GitHub remote: no publishing request was given.
- No Firebase configuration: it is unrelated to this deployment.
- No local application service was created: the running service is maintained
  in Zeabur and credentials remain only in Zeabur private variables.

## Read Before Any Future Task

Use the Mac path prefix below in place of the server `/root/kb-vault/` path:

```text
/Users/jacob/Library/CloudStorage/GoogleDrive-chen.uvtai12@gmail.com/我的雲端硬碟/wiki/KB-Vault/
```

Read the handoff, cockpit, global rules, OpenCode rules, and OpenCode worklog
before accepting remote coding work or changing the deployed service.
