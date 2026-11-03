# ChatGPT upload compatibility — 1.0.1

The user's actual Upload plugin archive error lists `.codex-plugin/plugin.json`, `.agent-plugin/plugin.json`, `.claude-plugin/plugin.json`, or root `skills/*/SKILL.md`, `.mcp.json`, `.app.json` as recognized content. It did not recognize the standalone agent-skill distribution. This target evidence overrides a generic assumption about portable root recognition.

For this target account, create a Codex-compatible ChatGPT plugin archive with `.codex-plugin/plugin.json` and `skills/<skill>/SKILL.md` directly at ZIP root. A mere filename change to a standalone skill ZIP cannot fix its structure.

The existing validate_plugin.py and package_plugin.py are portable-format validators and intentionally reject Codex overlays. Use them only on a separate portable staging package; do not report that a Codex final ZIP passed that validator. For a Codex final archive, parse its JSON, check recognized root, skills path, skill frontmatter, included resources/assets, archive integrity and safety, and report those checks separately. In the compatibility manifest use root `skills: "./skills/"` and root `interface`; do not put those keys at the root of a portable plugin.json. A skills-only package needs no .mcp.json or .app.json.

Reuse only actual publisher metadata. For personal use, this wrapper uses the descriptive label 'Personal workspace'; it does not claim a verified individual or business publisher. Replace it with the user's real chosen publisher identity before public submission.

A successful import does not ensure scripts run. Check host file/code execution availability when creating a plugin. If unavailable, supply explicit file contents and honest manual packaging instructions; never invent a download or executed validation.

This patch fixes archive recognition locally. Actual ChatGPT acceptance, scanning and runtime behavior require the user's next upload. The original report and tests retained in this package describe version 1.0.0 local validation, not a live 1.0.1 acceptance test.
