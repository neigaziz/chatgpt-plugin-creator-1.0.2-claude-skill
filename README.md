# ChatGPT Plugin Creator — Claude / Agent Skills edition

Standalone distribution **1.0.2** · Converted 2 November 2026 from the supplied ChatGPT plugin wrapper 1.0.1. Original bundled evidence snapshots retain their original dates.

**The same ChatGPT plugin creator, packaged as a standalone Claude/Agent Skill.** It still creates and repairs ChatGPT plugins; it has not been changed into a Claude skill creator. This package is not installed automatically, and no account was accessed.

## Preserved capabilities

- Purpose/use-case interpretation, focused task contracts, workflow and instruction authoring.
- Skills-only ChatGPT plugin generation, editable sources, presentation assets and upload guidance.
- Original portable JSON schemas, Python validation and ZIP packaging helpers.
- Target-account Codex-compatible archive override, with separate validation boundaries.
- Existing remote-MCP integration planning and declaration checks; honest authentication/hosting limits.
- Public-submission preparation, permission gates and evidence requirements.
- Original templates, documented sources, security guidance, document-summary example, executable tests and semantic-evaluation scenarios.

All 51 original skill files are retained: unchanged resources remain at their original relative paths; original versions of the three adapted entry/documentation files are preserved as SKILL.original.md, README.original.md and CHANGELOG.original.md. The original outer plugin manifest, root README and icon are archived in references/original-distribution. Only platform-independent copying excludes macOS .DS_Store and caches. The original SKILL.md workflow is retained verbatim with one short added host-adapter section.

## Install in Claude

### Claude Code

Extract the archive. Place its `chatgpt-plugin-creator` folder in your personal skills directory so the entry point is:

```text
~/.claude/skills/chatgpt-plugin-creator/SKILL.md
```

For project-scoped use, place that folder under your project's `.claude/skills/` instead. Keep all sibling folders and files together; SKILL.md alone is not the full package. Do not overwrite an existing installation without reviewing changes. Reload/restart the relevant session if the host requires it. This distribution does not perform installation or configure permissions.

### Claude web or desktop

If your current Claude account/interface exposes a custom Skills upload feature, upload the standalone skill ZIP through that feature, not a plugin importer. The ZIP has one top-level `chatgpt-plugin-creator/` folder containing SKILL.md. Enable the skill and any separately required file/code capabilities through the actual interface. Availability, labels and permissions depend on the product/account; live import was not tested in this conversion. Do not assume skill upload is available merely because Claude desktop is installed.

### Other Agent Skills hosts

Use the host's supported skill importer or skill directory. Preserve the folder structure and verify discovery from the frontmatter. A common file format is not a guarantee that each host supports terminal execution or downloadable artifacts. Chatbox installation, if desired, is a separate action requiring approval.

## Invoke it

> Use chatgpt-plugin-creator. Create a ChatGPT plugin for analysing quantitative-genetics research papers. I will upload papers and want models, assumptions, genetic parameters, software, limitations and evidence-linked conclusions. Deliver editable sources, the appropriate ChatGPT upload archive, a validation report and test prompts.

Or:

> Create a ChatGPT plugin for weekly meeting summaries from notes I upload. Include decisions, action items, owners and unanswered questions, without inventing missing deadlines.

A Claude invocation does not require ChatGPT @Plugin mention syntax. Generated instructions for using the finished plugin in ChatGPT may still use that syntax where supported.

## Runtime and executable requirements

Instructions can be read without a shell. Running the original helpers requires **Python 3.10+**, **jsonschema >=4.18,<5**, **PyYAML >=6.0,<7**, file access and a permitted code-execution environment. Do not install dependencies automatically. With explicit approval, use the original requirements.txt in an appropriate environment.

From the installed skill directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/validate_plugin.py examples/document-summary --profile workspace
python3 scripts/package_plugin.py examples/document-summary /your/permitted/output/document-summary-upload.zip --profile workspace
```

The last command uses an illustrative path: replace it with a real permitted output directory outside the source tree and a filename that does not already exist. These helpers validate **portable ChatGPT plugin staging packages**. They deliberately do not validate the target-account Codex overlay; read [target compatibility](references/chatgpt-upload-compatibility.md) for its separate required checks.

## What changed

The outer .codex-plugin wrapper is no longer the installation entry point. The skill folder itself is now the distributable. A short [Claude/agent host adapter](references/claude-agent-host.md) handles activation, paths and actual host file-delivery tools without changing the original generation workflow. No original executable helper, schema, example or source capture was rewritten. Original docs/ logs remain historical evidence; the separate conversion report records this build's checks.

## Important boundaries

This creator's ZIP is for a **Skills importer**, not ChatGPT Upload plugin archive. The archives it later generates for your requested ChatGPT plugins are different deliverables. No additional license is asserted over supplied source or captured third-party documentation.

The skill preserves implementation and intended capabilities, not a guarantee of identical model decisions or host permissions. It cannot grant code execution, API credentials, working MCP connections, OAuth, backend hosting, ChatGPT account features or submission approval. Where tools are absent it must provide an honest blocked/manual result, not fabricated files or validations. Live Claude activation, semantic equivalence and live ChatGPT upload acceptance were not tested. See the separately delivered conversion report for exact executed checks.
