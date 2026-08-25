# /trouble — four-minds debug protocol for stuck incidents

<p align="center">
  <img src="trouble-skill.jpg" alt="The four minds of /trouble: Data, Sherlock Holmes, Linus Torvalds, and Brian Cox around a holographic debug console" width="720">
</p>

**Stop guessing. Make the agent argue until the evidence wins.**

`/trouble` is an open-source **AI agent skill** and **marketplace plugin** for
hard debugging: production incidents, debug loops, and “nothing I try is
fixing this” bugs. It installs on **Grok**, **Claude Code**, **GitHub Copilot
CLI**, **OpenAI Codex**, and **DeepSeek Harness**.

Four personalities — **Data** (Star Trek), **Sherlock Holmes**, **Linus
Torvalds**, and **Brian Cox** — collect verbatim evidence, rank hypotheses
with explicit **Bayesian** arithmetic, and **will not apply a fix until they
unanimously agree**. Every run ends with a machine-parseable
`TROUBLE_VERDICT_BEGIN` / `TROUBLE_VERDICT_END` block that pipelines can gate
on.

If your coding agent patches first and thinks later, this is the protocol that
slows it down on purpose.

## Why people install it

- **Root-cause analysis, not vibes.** Claims without a quoted log line, file,
  or command output are tagged unverified and cannot support a fix.
- **Incident response for agents.** Exit-code triage, MCP documentation
  survey, smuggled-assumption hunt, timeline / causality check.
- **A real agreement gate.** Data, Sherlock, Linus, and Brian Cox each vote
  yes/no with a 0–10 confidence score before any code change.
- **Host coverage.** One plugin leaf, GitHub `owner/repo` install — the same
  shape as marketplace skills such as
  [write-legible-c](https://github.com/7etsuo/write-legible-c).

## Install (recommended)

Add this marketplace, then install the plugin. The shorthand is
`coldcanuk/trouble`.

### Grok

```bash
grok plugin marketplace add coldcanuk/trouble
grok plugin install trouble --trust
```

Enable it if it shows as installed but inactive:

```bash
grok plugin enable trouble
```

Or in the TUI: `/plugins` → Plugins tab → select **trouble** → `Space` to
enable → `r` to reload (or start a new session).

#### One-shot install from the plugin path

```bash
grok plugin install coldcanuk/trouble#plugins/trouble --trust
```

#### Local clone

```bash
git clone https://github.com/coldcanuk/trouble.git
grok plugin marketplace add ./trouble
grok plugin install trouble --trust
```

### Claude Code

```bash
claude plugin marketplace add coldcanuk/trouble
claude plugin install trouble@trouble
```

In a session: `/plugin marketplace add coldcanuk/trouble` then
`/plugin install trouble@trouble`.

### GitHub Copilot CLI

```bash
copilot plugin marketplace add coldcanuk/trouble
copilot plugin install trouble@trouble
```

In a session: `/plugin marketplace add coldcanuk/trouble`. Copilot reads
`.github/plugin/marketplace.json` (and also accepts `.claude-plugin/`).

### Codex / `.agents`

```bash
codex plugin marketplace add coldcanuk/trouble
```

Codex reads `.agents/plugins/marketplace.json`. The plugin manifest is
`plugins/trouble/.codex-plugin/plugin.json`. After adding the marketplace,
install **trouble** from the plugin directory.

### DeepSeek Harness

DeepSeek Harness has **no** git marketplace catalog analogous to
`.grok-plugin/marketplace.json` or `.claude-plugin/marketplace.json`. Do not
look for `.deepseek-plugin/marketplace.json` — that file is not a DSH
interface. DSH discovers `SKILL.md` by copying the skill bundle into a skill
root (or via `npx skills add` when you want a generic Agent Skills installer).

Copy the shipped skill directory:

```bash
git clone https://github.com/coldcanuk/trouble.git
mkdir -p ~/.dsh/skills ~/.agents/skills
cp -R trouble/plugins/trouble/skills/trouble ~/.dsh/skills/trouble
cp -R trouble/plugins/trouble/skills/trouble ~/.agents/skills/trouble
```

Project-local:

```bash
mkdir -p .dsh/skills .agents/skills
cp -R /path/to/trouble/plugins/trouble/skills/trouble .dsh/skills/trouble
```

Optional Agent Skills CLI (not a DSH marketplace):

```bash
npx skills add coldcanuk/trouble
```

If that installer does not find the nested `SKILL.md`, use the copy commands
above. Restart the DSH session and invoke `/trouble`.

## Use

- Slash command: `/trouble`
- Skills menu: `/skills trouble`
- Triggers: “troubleshoot”, “debug this”, “root cause”, “incident response”,
  “let's Bayesian this”, “bring in Sherlock/Linus/Data/Brian”, “we need the
  four minds”, or a problem that has already been worked on unsuccessfully

The agent must announce **Using the four-minds debug protocol** and follow the
phases in `SKILL.md`.

## What you get

```
plugins/trouble/
  plugin.json
  .claude-plugin/plugin.json
  .codex-plugin/plugin.json
  skills/trouble/
    SKILL.md
```

Host catalogs (all point at `./plugins/trouble`):

| Host | Catalog |
| --- | --- |
| Grok | `.grok-plugin/marketplace.json` |
| Claude Code | `.claude-plugin/marketplace.json` |
| Copilot CLI | `.github/plugin/marketplace.json` |
| Codex / `.agents` | `.agents/plugins/marketplace.json` |

## Uninstall

```bash
grok plugin uninstall trouble --confirm
grok plugin marketplace remove coldcanuk/trouble

claude plugin uninstall trouble@trouble
# then remove the marketplace in /plugin

copilot plugin uninstall trouble
copilot plugin marketplace remove trouble --force
```

## Validate (maintainers)

```bash
grok plugin validate ./plugins/trouble
python3 -m unittest discover -s tests -v
```

## License

[GNU General Public License v3.0 or later](LICENSE) (GPLv3).

Copyright (C) 2026 coldcanuk.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
