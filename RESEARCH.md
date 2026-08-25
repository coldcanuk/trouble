# Research: marketplace catalogs for `/trouble`

Findings used to freeze the remaining implementation. Sources: Grok user-guide
`09-plugins.md`, Claude Code plugin-marketplaces docs, GitHub Copilot CLI plugin
reference, OpenAI Codex "Package your plugin" docs, DeepSeek Harness
skill-filesystem README, and the public example `7etsuo/write-legible-c`.

## Layout (mirror write-legible-c)

```
.
├── .claude-plugin/marketplace.json     # Claude Code `/plugin marketplace add`
├── .grok-plugin/marketplace.json       # Grok `plugin marketplace add`
├── .grok-plugin/plugin-index.json      # optional Grok browser catalog
├── .github/plugin/marketplace.json     # Copilot CLI `plugin marketplace add`
├── .agents/plugins/marketplace.json    # Codex / .agents marketplace
├── plugins/trouble/
│   ├── plugin.json                     # Grok / Copilot root manifest
│   ├── .claude-plugin/plugin.json      # Claude Code plugin identity (required)
│   ├── .codex-plugin/plugin.json       # Codex required plugin manifest
│   └── skills/trouble/SKILL.md         # single source of protocol text
├── LICENSE                             # GPLv3
└── README.md                           # host install recipes
```

Local clone path (user-requested; parent did not exist before this work):
`/opt/repo/ai/marketplace/skills/trouble`.

GitHub: authenticated owner `coldcanuk`; no `trouble` repo existed at plan time
(API 404). Repo name: `trouble`. Example: https://github.com/7etsuo/write-legible-c

## Catalog `source` schemas (do not mix)

| Host | Catalog path | Plugin `source` |
| --- | --- | --- |
| Grok | `.grok-plugin/marketplace.json` | object `{ "type": "local", "path": "./plugins/trouble" }` |
| Claude Code | `.claude-plugin/marketplace.json` | same local object (write-legible-c dual catalog) or string path |
| Copilot CLI | `.github/plugin/marketplace.json` | **string** `"./plugins/trouble"` (not Grok's `{type,path}` object) |
| Codex / `.agents` | `.agents/plugins/marketplace.json` | `{ "source": { "source": "local", "path": "./plugins/trouble" }, "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" }, "category": "…" }` |

Grok also accepts a plain string path; Copilot's documented local form is the
string. Codex requires nested `policy.installation`, `policy.authentication`,
and `category`. Codex plugin identity lives at
`plugins/trouble/.codex-plugin/plugin.json` with `skills: "./skills/"`.

`plugin-index.json` is optional display metadata for the Grok marketplace
browser. Installs work without it. Include a minimal catalog so `/plugins`
shows the `trouble` skill before install.

## DeepSeek: no git marketplace catalog

DeepSeek Harness discovers `SKILL.md` under:

- project `.dsh/skills/` and `.agents/skills/`
- user `~/.dsh/skills/` and `~/.agents/skills/`

There is **no** `.deepseek-plugin/marketplace.json` analogous to Grok/Claude.
DSH "plugin add" installs Cordis/npm bundles (`package.json` `dsh.bundle`),
which is out of scope. Document copy into a skill root and, when useful,
`npx skills add <owner/repo>`. Do not invent a DeepSeek marketplace file.

## Skill sanitization

The Overmind in-tree `/trouble` skill is the protocol source. Before publish:

- Strip host-absolute home paths and IDE-specific MCP descriptor directories.
- Strip Overmind-only search scripts, exit codes, and GitLab paperwork rules.
- Keep four personalities (Data, Sherlock Holmes, Linus Torvalds, Brian Cox),
  Bayesian ranking, unanimous agreement gate, and `TROUBLE_VERDICT_BEGIN` /
  `TROUBLE_VERDICT_END`.

## Install commands (owner/repo)

```bash
# Grok
grok plugin marketplace add coldcanuk/trouble
grok plugin install trouble --trust

# Claude Code
claude plugin marketplace add coldcanuk/trouble
claude plugin install trouble@trouble

# Copilot CLI
copilot plugin marketplace add coldcanuk/trouble
copilot plugin install trouble@trouble

# Codex / .agents
codex plugin marketplace add coldcanuk/trouble
```

## Risks carried into implementation

- `gh` is unauthenticated here; `ssh git@github.com` failed host-key checks.
  Publish via GitHub MCP `create_repository` (`private: false`, no auto-init)
  plus `push_files`.
- `grok plugin marketplace add` mutates user Grok config; verification must
  remove the source afterward.
