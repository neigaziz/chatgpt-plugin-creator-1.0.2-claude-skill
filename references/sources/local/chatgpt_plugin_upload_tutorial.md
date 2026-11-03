# Creating a ChatGPT Plugin Using “Upload Plugin Archive”

**Conversation export**  
**Date:** 31 October 2026

## Original question

> Give me tutorial step by steps how can I create plugin in www.chatgpt.com via upload plugin archive. What are the required files for plugin archive?

The tutorial below is an export of the response to that question. The original conversation also included a screenshot of the ChatGPT Plugins page showing the **Add** menu with **Create plugin**, **Upload plugin archive**, and **Add custom MCP server**.

---

# Complete tutorial: Creating a ChatGPT plugin using Upload plugin archive

The screenshot shows the ChatGPT Plugins interface, which offers an upload flow for plugin archives.

You can build a plugin on your computer, package its files into a `.zip` archive, and upload it through the ChatGPT interface.

The plugin system described here distinguishes between:

1. **Skills:** Reusable instructions that teach ChatGPT how to perform a task or follow a workflow.
2. **Apps / MCP integrations:** Connections that allow ChatGPT to interact with external tools, APIs, databases, and services.

A plugin can contain skills, an MCP integration, or both. A skills-only plugin does not need a backend server or an API connection.

## 1. Understand the plugin architecture

Before creating the archive, understand what each component does.

```text
ChatGPT
  |
  v
Your plugin (.zip archive)
  |
  +-- plugin.json       Main plugin manifest
  |
  +-- skills/           Optional reusable workflows
  |     +-- skill-name/
  |           +-- SKILL.md
  |
  +-- mcp.json          Optional MCP server configuration
  |
  +-- assets/           Optional images, icons, and other resources
  |
  v
Installed plugin
```

A **plugin manifest** is the configuration file that identifies the plugin, describes it, and specifies its components. For the portable package format discussed in this tutorial, the root manifest is `plugin.json`.

## 2. Required files for a plugin ZIP archive

A typical portable plugin structure is:

```text
research-paper-review/
├── plugin.json                 # Main manifest; required
├── skills/                     # Optional directory of skills
│   └── paper-review/
│       ├── SKILL.md            # Required for this skill
│       ├── references/         # Optional supporting documents
│       ├── scripts/            # Optional helper scripts
│       └── assets/             # Optional supporting assets
├── mcp.json                    # Optional MCP configuration
├── assets/                     # Optional plugin-level assets
└── .codex-plugin/              # Optional Codex compatibility files
```

| File or directory | Purpose | Required? |
|---|---|---|
| `plugin.json` | Main plugin manifest and identity | Yes |
| `skills/` | Contains reusable skills | No |
| `SKILL.md` | Instructions for an individual skill | Yes, when including that skill |
| `mcp.json` | Configures bundled MCP servers | No |
| `assets/` | Icons, logos, images, and other assets | No |
| `.codex-plugin/plugin.json` | Optional Codex compatibility manifest | No |
| `hooks/` | Optional lifecycle hooks and scripts | No; only when supported and needed |

### File 1: `plugin.json` — the main manifest

This file identifies the plugin and provides its metadata.

Example:

**`plugin.json`**

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "research-paper-review",
  "version": "1.0.0",
  "description": "A plugin for structured scientific paper analysis.",
  "author": {
    "name": "Your Name"
  },
  "extensions": {
    "com.openai": {
      "interface": {
        "displayName": "Research Paper Review",
        "shortDescription": "Structured paper analysis",
        "longDescription": "Analyze scientific papers, extract methodologies, evaluate statistical approaches, interpret findings, and identify research limitations.",
        "developerName": "Your Name",
        "category": "Productivity"
      }
    }
  }
}
```

Important properties:

| Property | Explanation |
|---|---|
| `$schema` | Identifies the manifest specification used for validation |
| `name` | Technical plugin identifier; use lowercase letters and hyphens |
| `version` | Plugin version, commonly following semantic versioning |
| `description` | Explains the plugin's purpose |
| `author` | Identifies the author |
| `extensions.com.openai` | Contains OpenAI-specific settings |
| `displayName` | Name displayed to users |
| `shortDescription` | Short summary |
| `longDescription` | Detailed description |
| `developerName` | Publisher or developer name |
| `category` | Plugin category |

### File 2: `SKILL.md` — the skill instructions

A skill contains reusable instructions, procedures, rules, examples, and output requirements. Each skill has its own directory and its own `SKILL.md` file.

For example, a Research Paper Review skill could instruct ChatGPT to analyse a scientific article using these sections:

1. Research background and objectives.
2. Research questions and hypotheses.
3. Experimental design and methodology.
4. Data characteristics and sample size.
5. Statistical models and software.
6. Results and findings.
7. Genetic parameters and statistical interpretation, where relevant.
8. Limitations and potential biases.
9. Scientific contributions.
10. Future research directions.

Example:

**`skills/paper-review/SKILL.md`**

````markdown
---
name: paper-review
description: Analyse scientific research papers and provide
  structured methodological, statistical, and scientific
evaluations. Use when users provide academic papers for
critical analysis or literature review.
---

# Research Paper Review

## Role

Act as an experienced scientific researcher,
bioinformatician, and statistical geneticist.

## Main objective

Provide comprehensive and evidence-based analyses
of scientific research papers.

## Analysis workflow

Whenever the user provides a research paper:

1. Identify the research title, authors, journal,
   publication year, and DOI.
2. Explain the scientific background and research
   objectives.
3. Identify the research questions and hypotheses.
4. Describe the experimental design, population,
   sample size, and data collection methods.
5. Explain the statistical methodology, including
   mathematical models where relevant.
6. Identify all software, programming languages,
   packages, and computational tools used.
7. Extract and interpret the main results.
8. Explain the scientific implications.
9. Critically evaluate the limitations and potential
   sources of bias.
10. Identify research gaps and future directions.

## Accuracy requirements

- Base the analysis on the supplied paper.
- Never invent data, references, or DOI numbers.
- Distinguish reported findings from your own
  scientific interpretation.
- Explain technical terminology clearly.
- Identify missing information explicitly.

## Output structure

Organise the analysis into numbered sections.
Use paragraphs for detailed scientific explanations
and tables for software, methodology, and data.
````

The first section is **YAML frontmatter**. It provides the skill's name and description. The description helps ChatGPT determine when the skill is relevant to a user's request.

### File 3: `mcp.json` — connecting external tools

This file is optional. Include it when your plugin needs to connect to an external MCP server.

**MCP (Model Context Protocol)** is a standard that allows AI applications to communicate with external tools and services.

Examples of possible integrations for a research plugin include:

- Searching scientific papers through Semantic Scholar.
- Retrieving bibliographic information from OpenAlex.
- Searching research articles using Crossref.
- Retrieving scientific metadata from Europe PMC.
- Accessing a custom genomic database.

Example configuration:

**`mcp.json`**

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "literature-search": {
      "type": "streamable-http",
      "url": "https://your-server.example.com/mcp"
    }
  }
}
```

| Parameter | Meaning |
|---|---|
| `$schema` | MCP configuration specification |
| `mcpServers` | Collection of MCP server connections |
| `literature-search` | Chosen server identifier |
| `type` | MCP transport type |
| `url` | Address of the hosted MCP server |

**Important:** `mcp.json` does not contain the MCP server implementation. It describes how to connect to a server. The server must already exist and be reachable. Configure authentication separately where needed. Do not put private API keys or client secrets directly into the ZIP archive.

## 3. Three types of plugins

### Type A: Skills-only plugin

No backend, API, or MCP server is required.

```text
plugin.json
skills/
└── your-skill/
    └── SKILL.md
```

Example: a scientific literature review assistant that follows a defined paper-analysis workflow.

### Type B: MCP-only plugin

Connects ChatGPT to an existing hosted MCP server.

```text
plugin.json
mcp.json
```

Example: a plugin connecting ChatGPT to an OpenAlex MCP server with literature-search tools.

### Type C: Combined plugin

Combines instructions with external tools.

```text
plugin.json
mcp.json
skills/
└── your-skill/
    └── SKILL.md
assets/                 # Optional
```

Example: a literature research agent that searches academic databases, retrieves papers, evaluates statistical methods, and produces structured literature reviews.

**Recommendation:** Start with Type A to learn the archive format. Move to Type C when you want the plugin to interact with external scientific databases.

## 4. Step-by-step: Build your first plugin on macOS

This example creates a plugin called **Research Paper Review**. The instructions use macOS Terminal and do not require additional software for basic file creation and ZIP packaging.

### Step 1. Create the plugin directory

Open Terminal and run:

```bash
mkdir -p ~/Desktop/research-paper-review/skills/paper-review
```

Navigate into the plugin directory:

```bash
cd ~/Desktop/research-paper-review
```

### Step 2. Create `plugin.json`

Run:

```bash
nano plugin.json
```

Paste this content:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "research-paper-review",
  "version": "1.0.0",
  "description": "A structured scientific paper analysis assistant.",
  "author": {
    "name": "Your Name"
  },
  "extensions": {
    "com.openai": {
      "interface": {
        "displayName": "Research Paper Review",
        "shortDescription": "Structured paper analysis",
        "longDescription": "Analyse scientific papers, research methodologies, statistical models, findings, limitations and future research opportunities.",
        "developerName": "Your Name",
        "category": "Productivity"
      }
    }
  }
}
```

Save in Nano:

1. Press `Control + O`.
2. Press `Enter`.
3. Press `Control + X`.

### Step 3. Create `SKILL.md`

Run:

```bash
nano skills/paper-review/SKILL.md
```

Paste:

````markdown
---
name: paper-review
description: Analyse scientific papers using structured
  methodological, statistical, and scientific evaluation.
  Use when the user provides a research paper for analysis.
---

# Research Paper Review

## Role

Act as an experienced scientific researcher,
bioinformatician, and statistical geneticist.

## Objective

Analyse scientific publications in depth and provide
comprehensive, evidence-based scientific explanations.

## Workflow

Whenever the user provides a scientific paper:

1. Extract bibliographic information.
2. Identify the scientific background and objectives.
3. Identify the research questions and hypotheses.
4. Explain the experimental design.
5. Describe the datasets and sample sizes.
6. Explain the statistical models and methodology.
7. Identify software, packages, and computational tools.
8. Evaluate the main results and scientific findings.
9. Explain the biological and statistical implications.
10. Identify research limitations and potential biases.
11. Identify research gaps and future directions.

## Statistical methodology

Explain statistical methods in detail.

Where relevant, include:
- Mathematical equations.
- Model assumptions.
- Parameter definitions.
- Statistical interpretation.
- Model limitations.

## Accuracy requirements

- Use the provided scientific paper as the primary source.
- Never invent numerical results or references.
- Distinguish original findings from interpretation.
- Explain all technical terminology.
- Clearly indicate when information is unavailable.

## Output format

Produce a structured scientific report with:

1. General information
2. Research background
3. Research objectives
4. Materials and methods
5. Statistical methodology
6. Software and computational tools
7. Main results
8. Scientific interpretation
9. Critical evaluation
10. Conclusions and future research

Use detailed paragraphs for scientific explanations
and tables for technical comparisons.
````

Save using `Control + O`, `Enter`, and `Control + X`.

### Step 4. Validate your files

Validate the JSON syntax:

```bash
python3 -m json.tool plugin.json
```

If the JSON is valid, Python prints a formatted version without an error.

Check the directory contents:

```bash
find . -type f
```

Expected output:

```text
./plugin.json
./skills/paper-review/SKILL.md
```

### Step 5. Create the ZIP archive

Run:

```bash
zip -r ~/Desktop/research-paper-review.zip plugin.json skills
```

The archive should appear on your Desktop:

```text
Desktop/
├── research-paper-review/
│   ├── plugin.json
│   └── skills/
│       └── paper-review/
│           └── SKILL.md
└── research-paper-review.zip
```

**Important packaging detail:** `plugin.json` must be at the root of the ZIP archive, not nested inside an additional enclosing folder.

Correct:

```text
research-paper-review.zip
├── plugin.json
└── skills/
    └── paper-review/
        └── SKILL.md
```

Avoid:

```text
research-paper-review.zip
└── research-paper-review/
    ├── plugin.json
    └── skills/
```

Verify the archive:

```bash
unzip -l ~/Desktop/research-paper-review.zip
```

## 5. Upload your plugin to ChatGPT

Use the ChatGPT interface shown in the original screenshot.

1. Open [ChatGPT](https://chatgpt.com/) in your browser.
2. Navigate to **Plugins** in the sidebar.
3. Click **Add** in the upper-right corner.
4. Select **Upload plugin archive**.
5. Browse your Mac and select `research-paper-review.zip` from the Desktop.
6. Follow the upload and validation prompts. ChatGPT should inspect the package and report any package problems it detects.
7. Once imported, open the plugin details and review its metadata, included skills, and other components.
8. Install or enable the plugin where prompted, then test it in a new conversation.

Example test prompt:

```text
@Research Paper Review

Analyse the scientific paper I have attached.
Follow your complete 10-section research paper
analysis methodology.
```

**Permissions note:** ZIP uploads may require upload permission or access as an eligible workspace owner or administrator. The documented workspace route is **Admin console → select workspace → Plugins → Add → Upload plugin**. A permission error does not necessarily mean the archive is defective.

## 6. Adding additional components

### A. Add reference documents

You can include supporting guidance, scripts, templates, and other resources in the skill directory.

Example:

```text
research-paper-review/
├── plugin.json
└── skills/
    └── paper-review/
        ├── SKILL.md
        ├── references/
        │   ├── statistical-methodology.md
        │   ├── literature-review-guidelines.md
        │   └── scientific-writing-guidelines.md
        ├── scripts/
        │   └── calculate_statistics.py
        └── assets/
            └── paper-review-template.docx
```

You can instruct `SKILL.md` to consult these reference documents when appropriate. Supporting files do not replace the required `SKILL.md`.

### B. Add multiple skills

One plugin can contain multiple independent skills.

```text
research-assistant/
├── plugin.json
└── skills/
    ├── literature-search/
    │   └── SKILL.md
    ├── paper-review/
    │   └── SKILL.md
    ├── systematic-review/
    │   └── SKILL.md
    ├── statistical-genetics/
    │   └── SKILL.md
    └── scientific-writing/
        └── SKILL.md
```

Each `SKILL.md` has its own name, description, and instructions. Keep each skill focused on a distinct workflow rather than putting every instruction into one very large file.

### C. Add an MCP server

When ready to connect external services, add `mcp.json` to the root directory:

```text
research-assistant/
├── plugin.json
├── mcp.json
└── skills/
    ├── literature-search/
    │   └── SKILL.md
    └── paper-review/
        └── SKILL.md
```

The MCP server must already be deployed and accessible. For a web-based plugin, use an appropriate remote MCP endpoint rather than assuming a server running on your Mac's `localhost` will be accessible to ChatGPT.

## 7. Personal upload versus public publication

These are different objectives:

| Objective | Meaning |
|---|---|
| Personal use | Create and use your own plugin |
| Workspace sharing | Make a plugin available to selected workspace members |
| Public publication | Submit a plugin for review and possible listing in a public directory |

Uploading a ZIP does not automatically publish a plugin publicly. Public publication has a separate submission process, which can involve developer verification, package metadata, automated checks, and review.

## 8. Common mistakes to avoid

| Mistake | Correct approach |
|---|---|
| Missing `plugin.json` | Include it at the ZIP root |
| Incorrect folder structure | Put `skills/` at the plugin root |
| Missing skill metadata | Include `name` and `description` in YAML frontmatter |
| Invalid JSON syntax | Validate with `python3 -m json.tool plugin.json` |
| Incorrect ZIP packaging | Avoid an unnecessary parent-folder level |
| Broken asset references | Ensure every referenced file exists |
| Including API keys | Configure authentication separately |
| Including `mcp.json` without a working server | Deploy and test the MCP server first |
| Following older tutorials exclusively | Use the current portable `plugin.json` format where applicable |

Older ChatGPT plugin tutorials may describe `ai-plugin.json` and `openapi.yaml`. Those files belong to an older integration approach. For a new portable plugin, follow the current root `plugin.json` format described in the relevant OpenAI documentation. Compatibility with other manifest formats may vary.

## 9. Official documentation and resources

- [OpenAI Developers — Package your plugin](https://developers.openai.com/plugins/build/plugins)
- [OpenAI Developers — Build skills](https://developers.openai.com/plugins/build/skills)
- [OpenAI Developers — MCP server development](https://developers.openai.com/plugins/build/mcp)
- [OpenAI Developers — Upload and submit](https://developers.openai.com/plugins/deploy/submission)
- [ChatGPT — Build plugins](https://learn.chatgpt.com/docs/build-plugins)

Consult the current documentation before relying on schema details or workspace upload requirements, as these can change.

## 10. Summary: What do you actually need?

For a first skill-based plugin, the minimum useful archive contains:

```text
research-paper-review.zip
├── plugin.json
└── skills/
    └── my-skill/
        └── SKILL.md
```

Package those files into one ZIP, then choose **Add → Upload plugin archive** in ChatGPT.

You do not need an API, MCP server, database, or backend to create a skills-only plugin. You can create reusable AI workflows using `plugin.json` and one or more `SKILL.md` files. To interact with external databases and services, add an MCP component when necessary.

### Recommended next project: AI Research Assistant

A useful next project is an AI Research Assistant plugin containing five independent skills:

1. Literature Search and Discovery.
2. Scientific Paper Analysis.
3. Systematic Literature Review and PRISMA.
4. Statistical Genetics and Bioinformatics.
5. Scientific Writing and Manuscript Preparation.

Package the skills in one ZIP file and add optional MCP connections to OpenAlex, Semantic Scholar, and other research services when those servers are available and configured.

---

## Export note

This Markdown file contains the original question and the substantive tutorial response. The original screenshot is not embedded in this text export.
