#!/usr/bin/env python3
"""Structure tests for the shipped /trouble marketplace plugin.

Reads the files on disk in this repository (catalogs, manifests, SKILL.md).
Does not re-implement installers or copy fixtures of the skill body.
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CATALOGS = (
    ROOT / ".claude-plugin" / "marketplace.json",
    ROOT / ".grok-plugin" / "marketplace.json",
    ROOT / ".github" / "plugin" / "marketplace.json",
    ROOT / ".agents" / "plugins" / "marketplace.json",
)

PLUGIN_DIR = ROOT / "plugins" / "trouble"
SKILL_MD = PLUGIN_DIR / "skills" / "trouble" / "SKILL.md"

FORBIDDEN_HOST_PATH = "/" + "home" + "/" + "chuck"


def plugin_source_path(entry: dict) -> str:
    """Resolve a catalog plugin entry's source to a repo-relative directory."""
    source = entry.get("source")
    if isinstance(source, str) and source.strip():
        return source
    if isinstance(source, dict):
        path = source.get("path")
        if isinstance(path, str) and path.strip():
            return path
    raise AssertionError(f"plugin entry has no resolvable source path: {entry!r}")


def parse_skill_md(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        raise AssertionError("SKILL.md must start with YAML frontmatter ---")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise AssertionError("SKILL.md frontmatter is not closed")
    frontmatter = parts[1]
    body = parts[2]
    name = None
    for raw in frontmatter.splitlines():
        line = raw.strip()
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip("\"'")
            break
    if not name:
        raise AssertionError("SKILL.md frontmatter is missing name:")
    return name, body


def tracked_paths() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    names = [n for n in result.stdout.decode().split("\0") if n]
    return [ROOT / name for name in names]


class TestMarketplaceCatalogs(unittest.TestCase):
    def test_each_catalog_lists_trouble_plugin_pointing_at_skill(self) -> None:
        self.assertEqual(len(CATALOGS), 4)
        for catalog in CATALOGS:
            with self.subTest(catalog=str(catalog.relative_to(ROOT))):
                self.assertTrue(catalog.is_file(), f"missing catalog {catalog}")
                data = json.loads(catalog.read_text(encoding="utf-8"))
                plugins = data.get("plugins")
                self.assertIsInstance(plugins, list)
                self.assertTrue(plugins, f"{catalog} has empty plugins[]")
                matches = [p for p in plugins if p.get("name") == "trouble"]
                self.assertEqual(len(matches), 1, f"{catalog} must list one plugin named trouble")
                rel = plugin_source_path(matches[0])
                plugin_dir = (ROOT / rel).resolve()
                self.assertTrue(plugin_dir.is_dir(), f"source {rel} is not a directory")
                skill = plugin_dir / "skills" / "trouble" / "SKILL.md"
                self.assertTrue(skill.is_file(), f"{rel} does not contain skills/trouble/SKILL.md")
                self.assertEqual(skill.resolve(), SKILL_MD.resolve())

    def test_copilot_source_is_a_string(self) -> None:
        data = json.loads(
            (ROOT / ".github" / "plugin" / "marketplace.json").read_text(encoding="utf-8")
        )
        source = data["plugins"][0]["source"]
        self.assertIsInstance(source, str)
        self.assertEqual(Path(source).as_posix().rstrip("/"), "plugins/trouble")

    def test_grok_and_claude_source_is_local_object(self) -> None:
        for rel in (".grok-plugin/marketplace.json", ".claude-plugin/marketplace.json"):
            with self.subTest(catalog=rel):
                data = json.loads((ROOT / rel).read_text(encoding="utf-8"))
                source = data["plugins"][0]["source"]
                self.assertIsInstance(source, dict)
                self.assertEqual(source.get("type"), "local")
                self.assertEqual(source.get("path"), "./plugins/trouble")

    def test_agents_catalog_has_codex_policy_shape(self) -> None:
        data = json.loads(
            (ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8")
        )
        entry = data["plugins"][0]
        self.assertEqual(entry["name"], "trouble")
        source = entry["source"]
        self.assertIsInstance(source, dict)
        self.assertEqual(source.get("source"), "local")
        self.assertEqual(source.get("path"), "./plugins/trouble")
        policy = entry.get("policy") or {}
        self.assertEqual(policy.get("installation"), "AVAILABLE")
        self.assertEqual(policy.get("authentication"), "ON_INSTALL")
        self.assertTrue(entry.get("category"))

    def test_no_invented_deepseek_marketplace_catalog(self) -> None:
        self.assertFalse((ROOT / ".deepseek-plugin").exists())
        self.assertFalse((ROOT / ".deepseek-plugin" / "marketplace.json").exists())


class TestShippedSkill(unittest.TestCase):
    def test_skill_yaml_name_and_protocol_body(self) -> None:
        self.assertTrue(SKILL_MD.is_file())
        text = SKILL_MD.read_text(encoding="utf-8")
        name, body = parse_skill_md(text)
        self.assertEqual(name, "trouble")
        self.assertIn("/trouble", text)
        for person in (
            "Data",
            "Sherlock Holmes",
            "Linus Torvalds",
            "Brian Cox",
        ):
            self.assertIn(person, body)
        self.assertIn("## Phase 3 — Bayesian evaluation", body)
        self.assertIn("Unanimous agreement gate", body)
        self.assertIn("TROUBLE_VERDICT_BEGIN", body)
        self.assertIn("TROUBLE_VERDICT_END", body)

    def test_plugin_manifests_exist(self) -> None:
        grok_manifest = json.loads((PLUGIN_DIR / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(grok_manifest["name"], "trouble")
        claude_path = PLUGIN_DIR / ".claude-plugin" / "plugin.json"
        self.assertTrue(claude_path.is_file(), "Claude Code requires plugins/trouble/.claude-plugin/plugin.json")
        claude_manifest = json.loads(claude_path.read_text(encoding="utf-8"))
        self.assertEqual(claude_manifest["name"], "trouble")
        codex_manifest = json.loads(
            (PLUGIN_DIR / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual(codex_manifest["name"], "trouble")
        self.assertEqual(codex_manifest.get("skills"), "./skills/")

    def test_readme_install_commands(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("grok plugin marketplace add coldcanuk/trouble", readme)
        self.assertIn("claude plugin marketplace add coldcanuk/trouble", readme)
        self.assertIn("copilot plugin marketplace add coldcanuk/trouble", readme)
        self.assertIn("codex plugin marketplace add coldcanuk/trouble", readme)
        self.assertIn("npx skills add coldcanuk/trouble", readme)
        self.assertIn(".dsh/skills", readme)
        self.assertRegex(
            readme,
            r"no.{0,80}git marketplace catalog",
            "README must say DeepSeek has no git marketplace catalog",
        )
        self.assertIn("Do not\nlook for `.deepseek-plugin/marketplace.json`", readme)
        self.assertIn("trouble-skill.jpg", readme)
        hero = ROOT / "trouble-skill.jpg"
        self.assertTrue(hero.is_file(), "README hero image trouble-skill.jpg must be in the repo")
        self.assertEqual(hero.read_bytes()[:3], b"\xff\xd8\xff")

    def test_gplv3_license_present(self) -> None:
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("GNU GENERAL PUBLIC LICENSE", license_text)
        self.assertIn("Version 3, 29 June 2007", license_text)
        grok_manifest = json.loads((PLUGIN_DIR / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(grok_manifest.get("license"), "GPL-3.0-or-later")
        claude_manifest = json.loads(
            (PLUGIN_DIR / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual(claude_manifest.get("license"), "GPL-3.0-or-later")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertRegex(readme, r"GNU General Public License v3|GPLv3")
        self.assertNotIn("MIT.", readme.split("## License")[-1] if "## License" in readme else "")

    def test_tracked_files_have_no_host_home_path(self) -> None:
        files = tracked_paths()
        self.assertTrue(files, "git ls-files returned no tracked files")
        offenders = []
        for path in files:
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if FORBIDDEN_HOST_PATH in text:
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [], f"host home path leaked in {offenders}")


if __name__ == "__main__":
    unittest.main()
