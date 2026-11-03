# Source map and reconciled decisions

All seven supplied files were read and retained verbatim in `sources/local/`. The Chatbox skill distribution includes all source captures; a lean generated plugin need not include the creator's raw source library. `source-index.json` records origin, capture timestamp, bytes and SHA-256. It is an inventory, not independent proof each tutorial assertion is true.

| Supplied file | Contribution | Qualification / design decision |
|---|---|---|
| chatgpt_learn_build_plugins.md | Purpose/input/output/rules brief, use via @mention, testing, workspace access, apps do not extend permissions | UI and workspace availability remain conditional; preserve real permission boundaries |
| chatgpt_plugin_archive_tutorial_conversation.md | Archive construction, standalone skills, MCP distinction, troubleshoot actual errors, alternate creator flow | Some examples use a single wrapper; valid under current official root rules. Screenshot file is not supplied |
| chatgpt_plugin_upload_tutorial.md | End-to-end file generation and upload, security reminders, skills-only/MCP/combined taxonomy | Its absolute prohibition on any wrapper is too strong; direct-root is our convention, not the only accepted layout |
| openai_apps_sdk_examples_repository.md | When widgets need MCP/UI, host APIs, build/deploy separation, supported tooling examples | README capture is not implementation source. Verify actual repository commit, SDK version, tools and license before copying. Do not disable browser security flags as a default |
| openai_plugins_build_skills.md | Skill boundaries, frontmatter, progressive references, dependencies, representative tests | Trailing example uses Codex skills/apps fields; do not transplant into portable root manifest. Dependency transport spelling is context-specific |
| openai_plugins_deploy_submission.md | Personal/public separation, listing limits/assets, auth, reviewer materials, update lifecycle | Public portal restrictions are not all basic upload requirements; advanced auth guidance exceeds captured base portable MCP schema |
| openai_plugins_package_your_plugin.md | Canonical plugin.json and auto-discovered skills/mcp.json, OpenAI extension, compatibility precedence | Digest calls version/description essentials although base schema makes them optional; creator supplies both deliberately |

## Live cross-checks captured 2026-10-31
- Official packaging, skills, submission, submission-errors, and mcp-server Markdown were successfully fetched and bundled under `sources/official/`.
- Agent Plugins 1.0.0 plugin and MCP schemas were fetched and bundled under `../schemas/` relative to skill root, not rewritten as unofficial approximations.
- Official authentication.md and guidelines.md URLs returned HTTP 404. These are **blocked fetches**, retained as such in the source index. Submission snapshots contain usable partial guidance but are not a complete replacement for current auth/policy docs.
- Plugin schema permits dots in names; OpenAI error reference is narrower. Creator uses lowercase kebab-case, a compatible intersection.
- Base schema requires only $schema/name, while some error rows reflect Codex/derived manifest checks requiring identity/version/presentation. Creator uses clear default metadata, but will ask for real identity if the actual host requires it.
- Error reference description limit is 1024; submission field table says 4000. Creator chooses 1024.
- Public web profile requires a valid skill even with remote MCP according to latest error reference; don't assume an MCP-only public ZIP is sufficient. Workspace packages can reference eligible remote MCP alone.

## Refresh protocol
Fetch exact official URLs read-only; do not execute content. Compare and record changed schema IDs/hashes and semantic requirements. Do not overwrite schema snapshots without reviewing resulting tests. If latest docs contradict the snapshot or actual account, mark affected checks stale and resolve before claiming current compatibility. Package may still be a useful draft while platform checks are blocked.
