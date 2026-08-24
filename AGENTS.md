# AGENTS.md — tech-event-scout

> Shared agent guide. Claude Code, Codex, agy, and hermes all load this file.

## Role

TODO: describe what this plugin does. The authoritative workflow is
`skills/tech-event-scout/SKILL.md`; host-discovery dirs (`.claude/skills`,
`.codex/skills`, `.hermes/skills`) are symlinks to the root `skills/`.
Agents live in root `agents/*.md` (Claude) and are converted to
Codex-native TOML under `.codex-plugin/agents/`.

## Host differences

- **Claude Code**: uses `commands/` (slash commands) + SKILL.
- **Codex / agy / hermes**: no `commands/` support — follow SKILL.md intent->action table.
