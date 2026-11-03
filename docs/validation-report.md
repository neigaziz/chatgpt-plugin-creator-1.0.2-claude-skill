# Build and validation report

Package: **chatgpt-plugin-creator 1.0.0**
Build date: **31 October 2026**
Target: file-capable agent hosts generating portable ChatGPT web plugins.

## Evidence and provenance
All seven supplied Markdown files are retained verbatim and mapped in references/source-map.md. Source-index.json records exact file hashes, byte counts, origin and timestamps. Five live official documentation snapshots and two official JSON schemas were successfully retrieved. Standalone authentication.md and guidelines.md returned HTTP 404; these fetches are explicitly blocked, not successful checks. Auth/policy guidance is therefore partial and advanced auth configuration requires fresh verification.

## Executed checks
- A failing preimplementation CLI-presence test was observed and saved in red-test.log. This is deterministic test-first evidence, **not** a behavioral no-skill agent baseline.
- Initial validator/packager suite: **37 tests passed** (5.831 seconds in the initial run). Tests exercise valid sources/ZIPs, strict JSON/YAML, schema rejection, duplicate skill names, broken references, symlinks, endpoint placeholders/private IPs, header/auth rejection, archive traversal/collisions/type conflicts, wrapper roots and no-overwrite packaging.
- Skill package checks: **8 tests**, checking frontmatter/size, all seven supplied source hashes, successful live-capture hashes, disclosure of failed fetches, authored Markdown links, model-test status, schemas and required deliverables. One initial run correctly failed while this report had not yet been written. Final combined results are in final-tests.log.
- The document-summary source package passes workspace-profile offline validation. It has three files: plugin.json, skills/summarize/SKILL.md and assets/icon.svg. It is separately packaged and its ZIP revalidated by the actual packager.
- Icon was viewed with the host image viewer: original document glyph, square 128x128 SVG/viewBox, no external references or scripts. It is still not a ChatGPT rendering test. Validator's generic IMAGE_REVIEW warning remains visible for both logo/composer references.
- JSON Schema validation uses the actual captured official Draft 2020-12 schemas and installed jsonschema library; YAML uses PyYAML safe parsing with duplicate/alias controls. It is not regex-only JSON validation.

## Specialist check applicability
The upstream agent-skills-specialist linter was run against the complete evidence-bearing folder. It reported **9 link findings**, all in verbatim captures: one missing screenshot from the supplied conversation, five original website /llms.txt links, and three HTTPS angle-bracket image links misread as local by its simple parser. These were preserved rather than modifying source evidence. Authored Markdown/link tests separately verify the actual skill's authored resources. A second authored-only scoped lint is saved as specialist-lint-authored.json.

The upstream specialist package checker was also run: **56 findings**. It hardcodes that specialist's own architecture (its adapters, workflows, schemas, manifest and tests); it is not a general Agent Skills package specification. These findings are not claimed as passes and are not requirements of this new skill. Its raw output is provided for transparency; this package uses its own purpose-specific tests instead of adding meaningless specialist files.

The upstream specialist's **own** self-evaluation command returned pass. That command tests the specialist package, not this generated creator; it does not establish creator behavior and is not counted in the creator's 45 tests.

## Checks not run
- Isolated model/subagent baseline or with-skill semantic/activation comparison: no such runner provided. Twelve explicit cases are in tests/evaluation-cases.json, marked not run.
- Actual plugin upload/acceptance, account permission checks, use via @mention, or execution of creator helper scripts inside ChatGPT.
- Live MCP protocol discovery/calls, OAuth, DNS routing safety or hosted UI interaction.
- OpenAI automated scans, complete public policies, domain/identity verification, reviewer testing or directory approval.
- Exhaustive malware/secret detection, all extension-field validation, or broad production deployment hardening.

## Release status
**Authored and locally tested.** The example is an offline-validated archive, not a live-accepted or publicly approved plugin. The creator skill has not been installed; no source files in the user's directory were modified, and no account/upload/deploy/publish actions were taken. The 45 deterministic tests cannot establish semantic intelligence or guaranteed acceptance. Raw-source citation warnings and specialist-specific layout findings have been assessed as reference/tool-applicability limitations, not hidden or mislabeled.

## Reproduce
From the skill folder with approved dependencies available:

```
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/validate_plugin.py examples/document-summary --profile workspace
python3 scripts/package_plugin.py examples/document-summary ../document-summary-1.0.0-upload.zip --profile workspace
python3 scripts/validate_plugin.py ../document-summary-1.0.0-upload.zip --profile workspace
```

Use a new ZIP output path for repeated packaging; overwrite is intentionally rejected. Source-index hashes verify preserved evidence; archive SHA-256 values are supplied in the external release manifest to avoid a self-referential hash inside the package.
