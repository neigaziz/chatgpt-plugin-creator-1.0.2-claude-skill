---
title: "Package your plugin – OpenAI Developers"
source: "https://developers.openai.com/plugins/build/plugins?utm_source=chatgpt.com"
source_markdown: "https://developers.openai.com/plugins/build/plugins.md"
retrieved: "2026-10-31"
format: "Markdown digest of the official documentation page"
---

# Package your plugin

> This file is a concise Markdown digest of the official page, not a verbatim reproduction. The original page also provides a Markdown version: [open or download the source Markdown](https://developers.openai.com/plugins/build/plugins.md).

Official page: <https://developers.openai.com/plugins/build/plugins>

## Purpose

Packaging groups a plugin's identity, skills, MCP connections, and supporting resources so ChatGPT and Codex can treat them as one installable unit.

## Portable package structure

The portable format uses a root `plugin.json`. Other components are optional and remain at the plugin root:

```text
my-plugin/
├── plugin.json                 # Required portable manifest
├── skills/                     # Optional reusable workflows
│   └── my-skill/
│       └── SKILL.md
├── mcp.json                    # Optional portable MCP configuration
├── assets/                     # Optional icons, logos, screenshots
├── hooks/                      # Optional; Codex desktop support
└── .codex-plugin/
    └── plugin.json             # Optional compatibility fallback
```

## Manifest essentials

A minimal portable manifest declares the Agent Plugins schema, a stable kebab-case name, a version, and a description. Skills are discovered from `skills/`; a separate skills field is not needed for the portable layout.

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "my-first-plugin",
  "version": "1.0.0",
  "description": "Reusable workflow"
}
```

## Skills and MCP

A skill lives at `skills/<skill-name>/SKILL.md` and begins with YAML frontmatter containing at least its `name` and `description`. Portable MCP servers are configured in root `mcp.json`, under `mcpServers`; each server entry declares its transport type and endpoint. Authentication configuration is declared per server. Secrets and client secrets are supplied through the connection flow, not embedded in the package.

## OpenAI-specific settings

Use `extensions.com.openai` in the root manifest for interface metadata, registered MCP-app mappings, onboarding-skill paths, and hook settings. Keep referenced paths relative to the plugin root and prefix them with `./`. Store visual assets under `assets/` where practical.

## Plugin Creator compatibility layout

The built-in `@plugin-creator` workflow currently scaffolds a Codex-compatible layout centered on `.codex-plugin/plugin.json`. Depending on requested options, it may also create `.mcp.json`, `.app.json`, `skills/`, `hooks/`, `scripts/`, and `assets/`. This is distinct from the portable layout: do not simply rename `.mcp.json` to `mcp.json`, because portable MCP entries also specify a transport `type`.

## Local marketplaces and distribution

Local marketplaces are JSON catalogs for authoring, testing, and private distribution. A marketplace entry identifies a plugin source, installation policy, authentication policy, and category. Sources can be local folders, Git repositories, or npm packages. Repo and personal marketplaces are separate from the universal public plugin directory.

Workspace publication is restricted to workspace admins and makes a plugin available to selected workspace roles; it does not make the plugin public. Public distribution requires submission through the plugin portal. Lifecycle hooks are supported for manually installed Codex desktop plugins and make a plugin ineligible for the public directory.

## Official references

- [Package your plugin](https://developers.openai.com/plugins/build/plugins)
- [Build skills](https://developers.openai.com/plugins/build/skills)
- [Build an MCP server](https://developers.openai.com/plugins/build/mcp)
- [Connect and test your plugin](https://developers.openai.com/plugins/test/connect)
- [Submit and publish](https://developers.openai.com/plugins/deploy/submission)
- [Plugin examples](https://developers.openai.com/plugins/build/examples)
