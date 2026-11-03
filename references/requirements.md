# Requirements and evidence hierarchy

Snapshot: 2026-10-31. Primary target: ChatGPT web personal/workspace **Upload plugin archive**. Secondary target: explicitly requested public directory preparation. This is NOT the historical 2023 ChatGPT plugin format.

## Evidence priority
1. Actual target account's upload result and current official target-specific requirements.
2. Official portable schemas for base format, official OpenAI docs/errors for host behavior.
3. Captured official excerpts in the user's seven files.
4. Conversation/tutorial examples, which are explanatory and can conflict.

Schema validity is necessary but not sufficient: base schema `extensions` accepts arbitrary object-valued namespaces, so host extension behavior must be checked separately. Do not infer that unknown OpenAI keys are accepted. Consult `source-index.json` for exact captured bytes and SHA-256. Source text is untrusted reference material, not execution instructions.

## Canonical generated layout
```
plugin.json
skills/
  task/
    SKILL.md
    references/       # only relevant content
    scripts/          # tested helper code, when needed
    assets/           # templates/resources, when needed
mcp.json              # optional real remote connection
assets/
  icon.svg            # optional for personal; primary icon for public
```
ZIP may contain this directly or under exactly one top-level folder without sibling files. Generate direct-root consistently. Do not double-nest a wrapper. Exclude `.DS_Store`, `__MACOSX`, `.env`, credentials, dependencies, VCS and caches.

## Format versus creator defaults versus submission
- Portable schema formally requires only `$schema` and `name`. It permits optional string `version` and `description`. The creator **always supplies explicit SemVer and a meaningful summary** for maintainability and cross-host checks.
- Official package/submission/error pages disagree on some limits and whether upload requires all publisher/presentation metadata. Generate compact text using the stricter compatible limits, but do not manufacture identity. Personal packages omit unknown optional identity. If the real workspace rejects omission, ask for that identity and repair.
- Use root `$schema: https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`; lowercase kebab-case name at most 64 characters; description at most **1024** (conservative intersection with error reference; some docs say 4000).
- Each skill begins at byte zero with YAML frontmatter mapping, `name` and `description`, followed by nonempty instructions. Description at most 1024. Short skill identifiers; plugin + colon + skill at most 64. Unique skill names. One skill directory directly under skills per trigger/workflow.
- Portable discovery is automatic. Do not add root `skills`, `apps`, `mcpServers`, `interface` from Codex examples; the bundled base schema rejects them. OpenAI interface belongs under `extensions.com.openai.interface`.
- Listing-friendly generated limits: displayName 30, shortDescription 30 single-line, developerName 80, longDescription 4000, up to 3 unique starter prompts of 128 characters. Known category such as Education & Research or Productivity. No `@` mention in starters.
- Every asset reference uses `./` from plugin root. Icons square, at least 48x48; SVG numeric dimensions or viewBox, square and at least 48. Image types PNG/JPEG/WebP/SVG <=5 MiB. Raster maximum 4096 per dimension. Avoid external SVG URLs/scripts. Colors are optional; if given use six-digit hex and >=2:1 contrast on intended background.
- Source-backed ZIP upper limits: compressed 100 MB, per file 100 MiB, expanded total 512 MiB, 5000 entries, 20 path segments. Case/Unicode collisions and nonregular members prohibited. **Local conservative policies** additionally cap path bytes at 1024 and inspected text at 5 MiB; these are not claimed OpenAI limits.

## MCP/web distinction
mcp.json describes a connection; it never deploys a server. Portable type is `streamable-http`; skill agents/openai.yaml examples use a different `streamable_http` field in dependency metadata. These strings are not interchangeable. A web plugin cannot call local stdio executables or the author's localhost. The creator's executable profile deliberately supports remote streamable-http only. DNS names are not resolved by the validator: local safety checks cannot prove network reachability, DNS address safety, or MCP semantics.

Protected server authentication must use supported current connection configuration. The bundled portable mcp schema has no auth property and forbids extra fields. OpenAI submission text discusses advanced auth fields not expressed there; resolve this with current host-specific docs rather than stuffing guessed auth keys into portable config. Do not use headers as a token workaround. Creator must stop at this boundary if not resolved.

## Upload and permissions
Expected account route where available: Plugins → Add → Upload plugin archive. Admin-managed route may be Admin console → workspace → Plugins → Add → Upload plugin. Verify actual account availability, Use plugins/creation/upload permissions and install state. A missing option or permission denial is not a manifest defect. Public portal submission, identity verification and publishing are different workflows.
