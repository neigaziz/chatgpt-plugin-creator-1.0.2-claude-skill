# ChatGPT Plugin Creator

Version 1.0.0 · Evidence captured 31 October 2026.

An agent skill for generating purpose-specific **ChatGPT portable plugin archives** from a purpose and intended use cases. It includes actual validation and ZIP-building tools, not merely a prompt. Default: skills-only personal/workspace package. External APIs/MCP/UI require real services and supported authentication. Public submission is opt-in.

## Use the skill
Install the `chatgpt-plugin-creator` skill folder using your host's supported skill installer, then invoke it with:

> Use chatgpt-plugin-creator. Purpose: analyse quantitative-genetics research papers. Intended use: I upload PDFs and want statistical models, assumptions, genetic parameters, software, limitations and evidence-linked conclusions. Create a personal/workspace ChatGPT plugin archive and validation report.

A shorter prompt works too:

> Create a ChatGPT plugin for preparing weekly meeting summaries from notes I upload. I need decisions, action items, owners and unanswered questions, without inventing missing deadlines.

The agent derives a focused contract and sensible defaults. It asks only for missing essentials. For a private service or protected API, purpose alone cannot supply access, hosting, real endpoint or auth configuration.

**This ZIP is an agent-skill distribution, not itself a ChatGPT plugin archive.** Do not select it under ChatGPT Upload plugin archive. The skill's generated `<name>-<version>-upload.zip` is the file to upload. A separately delivered document-summary example demonstrates that output format. This skill has not been installed automatically.

## Included
- SKILL.md: activation boundaries and full generation workflow.
- references/: authored requirements, writing/integration/public/security guidance and verbatim evidence snapshots.
- schemas/: captured official Agent Plugins 1.0.0 schemas.
- scripts/: offline validation and packaging; no network or uploaded-code execution.
- templates/: brief, manifest example, evaluation and delivery contracts.
- tests/: adversarial/positive executable regression suite and semantic evaluation scenarios.
- examples/document-summary/: fully authored minimal usable skills-only plugin.
- docs/: build validation report and plan.

## Requirements for executable checks
Python 3.10+; jsonschema 4.18–4.x; PyYAML 6.x. No npm/build tooling needed for these helpers. In an approved environment, install requirements manually if absent:

```bash
python3 -m pip install -r requirements.txt
```

Do not run dependency installation automatically. Skill instructions can be read without Python; inability to run checks must be disclosed. A ChatGPT runtime may not expose a shell or file-generation tools: a skill does not create those capabilities.

## Test and package the example
From this skill folder:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/validate_plugin.py examples/document-summary --profile workspace > example-validation.json
python3 scripts/package_plugin.py examples/document-summary ../document-summary-1.0.0-upload.zip --profile workspace
python3 scripts/validate_plugin.py ../document-summary-1.0.0-upload.zip --profile workspace
```

Output ZIP must not already exist and must be outside source. Keep reports outside upload source. Generated archives use plugin.json directly at ZIP root. One wrapper is accepted by the validator for inspecting imports. Strict creator profile is not a general converter for Codex, Claude, desktop-only plugins or the retired ai-plugin.json system.

## Important limits
Local checks catch many packaging mistakes, not all OpenAI rules. The base plugin schema deliberately leaves extension namespaces unspecified. Advanced authentication is not in captured base MCP schema; host-specific adapters must be verified rather than invented. Image dimensions/contrast and semantic prompt quality need review. No live account upload, external MCP/tool call, isolated model benchmark or public review was performed during this build. See `docs/validation-report.md` for exact evidence and `references/tool-coverage.md` for gaps.

Keep the editable sources and actual validation report for later updates. Follow the target account's real upload errors; do not assume missing permissions indicate malformed files. No installation, deployment, publication, backend hosting or account changes are implied by generating an archive.

## Source attribution
User-supplied documentation is preserved for traceability; official materials remain attributable to their linked sources. A repository README mentioning MIT is not a license grant for all OpenAI documentation. No additional license is imposed on the user's original files. No third-party application code or dependencies are vendored. The source index records which retrievals succeeded and which returned HTTP 404.
