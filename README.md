# trouble

Marketplace plugin that ships **`/trouble`** — a four-minds debug protocol for
stuck incidents and “nothing I try is fixing this” bugs.

The four personalities are **Data**, **Sherlock Holmes**, **Linus Torvalds**,
and **Brian Cox**. They collect evidence, rank hypotheses with explicit Bayesian
arithmetic, and must **unanimously agree** before a fix. Every run ends with a
machine-parseable `TROUBLE_VERDICT_BEGIN` / `TROUBLE_VERDICT_END` block.

Modeled on [7etsuo/write-legible-c](https://github.com/7etsuo/write-legible-c):
one plugin leaf, host-canonical marketplace catalogs, GitHub `owner/repo`
install.

## Install (recommended)

Add this marketplace, then install the plugin. Replace nothing — the shorthand
is `coldcanuk/trouble`.

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
- Triggers: “troubleshoot”, “debug this”, “let's Bayesian this”, “bring in
  Sherlock/Linus/Data/Brian”, “we need the four minds”, or a problem that has
  already been worked on unsuccessfully

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

MIT.
