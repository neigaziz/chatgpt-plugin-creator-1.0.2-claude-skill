# MCP, existing apps and interactive UI

## Decision
1. Files/text plus instruction workflow: skills-only.
2. Read/write external service: use an already allowed app if available, or a verified remote MCP server.
3. Inline widget/map/forms: MCP tool contracts plus Apps SDK UI resources and separately hosted assets/server.

Always describe what the ZIP accomplishes and what hosting/account/auth work remains. Purpose + usage alone is sufficient for self-contained skills; it is not enough to configure an unknown private API or invent business credentials.

## Endpoint and tool inventory
Record server owner, exact public HTTPS /mcp URL, transport, authentication requirements, actual exposed tool names, input/output schemas, read/write annotations, scopes, timeout/retry behavior, rate limits and safe error contract. User-provided URL may be authored as supplied, but label protocol/liveness untested until verified. Basic GET success is not tools/list or tools/call verification. Do not automatically call write tools to test a connection.

The deterministic validator does **not** make network requests. It excludes localhost, literal private IPs, reserved example domains, query credentials, nonstandard ports and nonempty headers as conservative creator policy. DNS rebinding/private DNS requires separate safe network handling; do not claim the URL filter guarantees public routing.

## Minimal portable remote declaration
This structural illustration is not a working endpoint and MUST NOT be emitted unchanged:
```
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "service-name": {
      "type": "streamable-http",
      "url": "https://REAL-USER-CONTROLLED-HOST/mcp"
    }
  }
}
```
Actual supplied URL and verified tool contract are essential. Do not add auth or dependency properties that the relevant schema does not support. Never replace a protected service with auth type none. Base portable schema supports streamable-http/sse/stdio but this creator targets only streamable-http for the web.

## Authentication gap and escalation
Captured submission docs mention provided OAuth clients, DCR/CIMD, discovery/overrides and portal secrets. Captured portable MCP 1.0.0 schema does not allow arbitrary authentication keys. The live standalone auth reference returned 404 during this build. Therefore advanced OAuth/host mappings need fresh authoritative host-specific configuration before release; the bundled validator intentionally rejects guessed auth fields. A compatible official adapter can be added with regression tests once verified. Do not secretly drop auth or embed a bearer token.

Public portal currently describes no auth/OAuth/mixed; API-key declarations alone cannot complete its connection flow. Reviewer secrets belong in secure portal fields. Private workspace connection capabilities may differ; verify in the target account. Do not infer legal/publication readiness from a technical endpoint.

## If no server exists
Offer a separate backend implementation project with actual API contracts, auth, server-side authorization, tests, deployment instructions and credentials configuration. Keep backend source OUTSIDE upload ZIP unless explicitly a needed resource. Label plugin draft integration-blocked until endpoint/config are ready; do not ship fake mcp.json. A skills-only fallback must explicitly state unsupported features and require user agreement if it materially changes the goal.

## UI-specific work
Use `sources/local/openai_apps_sdk_examples_repository.md` only as an index to official examples. Retrieve the actual implementation and current SDK docs at a pinned commit before copying; preserve applicable MIT notices. Verify tools/list, calls and resource metadata; bundle/build widgets; configure narrowly scoped CSP, widget state, origin protection, accessible UI and server-side persistent state. A widget is not just an icon or Markdown table. Do not disable browser security or expose arbitrary local services as a default. Do not assume React/npm availability; inspect and ask before dependency installation or deployment.
