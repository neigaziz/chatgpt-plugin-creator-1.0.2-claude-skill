# Conversation Export: Creating a ChatGPT Plugin by Uploading a Plugin Archive

## User

![Screenshot of the ChatGPT Plugins page](8C385396-450A-4B3B-A145-97A508DF9E26.png)

Give me tutorial step by steps how can I create plugin in www.chatgpt.com via upload plugin archive. What are the required files for plugin archive?

## Assistant

# Complete Tutorial: How to Create a ChatGPT Plugin by Uploading a Plugin Archive

**You can create a ChatGPT plugin by preparing a ZIP archive containing a plugin manifest and its capabilities, then uploading it through the interface shown in your screenshot.** For a simple plugin that gives ChatGPT reusable instructions and workflows, you do not need to build a server or write an application.

The most straightforward approach is to create a **skill-based plugin**. It consists of two essential components:

1. **`plugin.json`** — identifies the plugin and provides its basic metadata.
2. **`skills/<skill-name>/SKILL.md`** — contains the instructions that tell ChatGPT how to perform a particular task.

You can add other files when necessary. For example, `mcp.json` can configure a connection to a remote Model Context Protocol (MCP) server, which exposes tools that ChatGPT can use.

The tutorial below follows the current plugin packaging approach documented by OpenAI. ([developers.openai.com](https://developers.openai.com/plugins/build/plugins?utm_source=chatgpt.com))

---

# Part 1. Understand What a Plugin Archive Contains

## 1.1. What is a ChatGPT plugin?

A **plugin** is a package that groups reusable instructions, tools, and related resources into a capability that you can use in ChatGPT.

For example, you could create a plugin called *Scientific Literature Review Assistant* that helps you:

- Formulate research questions.
- Develop literature-search strategies.
- Establish inclusion and exclusion criteria.
- Extract information from scientific papers.
- Compare research methodologies.
- Identify research gaps.
- Prepare structured literature-review summaries.

You define these instructions in the plugin's files. ChatGPT can then use the resulting skill when a relevant task arises.

OpenAI's current plugin architecture supports reusable skills, connections to external tools through MCP, and other optional components. A plugin does not necessarily need every component. ([developers.openai.com](https://developers.openai.com/plugins/build/plugins?utm_source=chatgpt.com))

## 1.2. Understand the three main components

| Component | Filename or location | Required? | Purpose |
|---|---|---|---|
| Plugin manifest | `plugin.json` | Yes for the recommended package format | Defines the plugin's identity and basic metadata. |
| Skill instructions | `skills/<skill-name>/SKILL.md` | Recommended and necessary for this tutorial's skill-based example | Tells ChatGPT how to perform the intended workflow. |
| MCP configuration | `mcp.json` | No | Configures connections to MCP servers and their tools. |
| Reference documents | Files inside a skill directory | No | Provides additional documentation, templates, examples, or reference material. |
| Scripts | Files inside a skill directory | No | Provides supporting code where the supported environment can execute it. |
| Assets | `assets/` | No | Stores optional images, templates, and other supporting resources. |

The distinction between the first two files is particularly important.

**`plugin.json` describes the plugin; `SKILL.md` describes what the plugin should do.**

For example, `plugin.json` might identify a plugin as a literature-review assistant. Its `SKILL.md` file would contain the instructions for performing the review.

OpenAI documents `plugin.json` as the root manifest for the portable plugin format. Skills are organized under a `skills/` directory, while MCP configuration and supporting assets are optional. ([developers.openai.com](https://developers.openai.com/plugins/build/plugins))

---

# Part 2. Choose the Type of Plugin You Want to Build

Before creating the archive, decide what your plugin needs to accomplish.

There are two common starting points.

## Option A. Skill-based plugin

A skill-based plugin primarily provides ChatGPT with reusable instructions.

For example, you could create a plugin that consistently applies a specific scientific workflow when analyzing research papers.

It might instruct ChatGPT to:

1. Identify the research objectives.
2. Extract the study population, dataset, and sample size.
3. Identify the statistical methods and software.
4. Summarize the main findings.
5. Assess the limitations.
6. Connect the findings to your research questions.
7. Record citations and distinguish supported findings from interpretation.

This kind of plugin can be created without building an external server.

**Recommended starting point:** Choose this approach when you want to package a persona, specialized instructions, a research workflow, or a repeatable analytical procedure.

## Option B. Plugin with MCP tools

An MCP-enabled plugin connects ChatGPT to tools supplied by an MCP server.

MCP stands for *Model Context Protocol*. It is a standard for connecting AI applications to external tools and resources.

For example, a plugin could connect ChatGPT to a server that provides tools for searching scientific publications.

Depending on the server's implementation, those tools might allow ChatGPT to:

- Search a scientific database.
- Retrieve paper metadata.
- Query an external API.
- Access a connected database.
- Execute supported operations in another application.

This approach requires more than adding instructions to a ZIP file. You must also configure an appropriate MCP server connection. A remote MCP server must be hosted at a working endpoint accessible to the service connecting to it. The ZIP configuration does not, by itself, deploy the server. ([developers.openai.com](https://developers.openai.com/plugins/build/plugins?utm_source=chatgpt.com))

**My recommendation:** Start with Option A. Once the instructional workflow works correctly, add MCP integration if the plugin needs to retrieve information from an external system or execute tool-based operations.

---

# Part 3. Create Your First Plugin

For this tutorial, we will create a working example named **Literature Review Assistant**.

You can replace the name, description, and instructions with your own requirements.

## Step 1. Create the plugin folder

On your Mac, create the following directory structure:

```text
literature-review-assistant/
│
├── plugin.json
│
└── skills/
    │
    └── literature-review-assistant/
        │
        └── SKILL.md
```

The structure is important.

The main plugin folder contains `plugin.json`. The skill is placed inside the `skills/` directory, with its own directory containing `SKILL.md`.

For the portable plugin format, skills are discovered under the root `skills/` directory. You do not need to add a separate skills-path declaration to the minimal `plugin.json` used in this example. ([developers.openai.com](https://developers.openai.com/plugins/build/plugins?utm_source=chatgpt.com))

### Creating the folder in Finder

1. Open Finder.
2. Navigate to your Desktop or another working directory.
3. Create a folder named `literature-review-assistant`.
4. Inside it, create another folder named `skills`.
5. Inside `skills`, create `literature-review-assistant`.
6. You will eventually place `plugin.json` in the first folder and `SKILL.md` in the innermost folder.

The completed directory structure should match the example above.

You can also create everything using Terminal, as demonstrated later in this tutorial.

---

## Step 2. Create `plugin.json`

The `plugin.json` file is the plugin's manifest.

A **manifest** is a structured file that identifies a software package and describes its basic properties. Think of it as the plugin's registration record.

Create a file named:

```text
plugin.json
```

Place it directly inside:

```text
literature-review-assistant/
```

Copy the following content into the file:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "literature-review-assistant",
  "version": "1.0.0",
  "description": "Helps plan and conduct structured, transparent, and reproducible scientific literature reviews."
}
```

This follows the minimal portable manifest format shown in OpenAI's plugin packaging documentation. ([developers.openai.com](https://developers.openai.com/plugins/build/plugins?utm_source=chatgpt.com))

### Explanation of the fields

| Field | Meaning | Example |
|---|---|---|
| `$schema` | Identifies the schema used to validate the manifest. A schema defines the structure and rules of the file. | `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` |
| `name` | The plugin's technical identifier. | `literature-review-assistant` |
| `version` | The plugin's version number. | `1.0.0` |
| `description` | A short explanation of what the plugin does. | Helps conduct structured scientific literature reviews. |

### Rules for naming your plugin

Use a stable identifier with lowercase letters, numbers, and hyphens.

Suitable examples include:

```text
scientific-workflow-analyst
genomic-selection-researcher
research-paper-analyzer
academic-writing-assistant
```

Avoid spaces in the technical `name` field. Keep the identifier stable as you update the plugin.

You can use a more readable display name in interfaces that support separate presentation metadata.

### Important: Save the file with the correct extension

The filename must be:

```text
plugin.json
```

Not:

```text
plugin.json.txt
```

If you use a text editor that automatically appends `.txt`, remove that extension.

The file must also contain valid JSON. For example, strings must use double quotation marks, and the last property must not have an extra trailing comma.

---

## Step 3. Create the `SKILL.md` file

This is the most important part of a skill-based plugin because it contains the actual instructions.

Create a file named:

```text
SKILL.md
```

Save it inside:

```text
literature-review-assistant/skills/literature-review-assistant/
```

The file should begin with a metadata section followed by the instructions.

Copy the example below.

```markdown
---
name: literature-review-assistant
description: Plans, structures, analyzes, and synthesizes scientific literature reviews using transparent criteria and traceable evidence.
---

# Literature Review Assistant

## Purpose

Help the user conduct rigorous and reproducible scientific
literature reviews.

Support research question development, search planning,
study screening, data extraction, evidence synthesis,
critical appraisal, and research-gap identification.

## General principles

1. Use precise scientific language.
2. Distinguish reported findings from interpretation.
3. Do not invent publications, authors, DOIs, study results,
   sample sizes, or statistical methods.
4. Identify missing information rather than silently assuming
   that it is available.
5. Preserve the connection between each scientific claim
   and its supporting source.
6. Clearly distinguish evidence obtained from full-text papers,
   abstracts, metadata, and user-provided notes.

## Workflow

### Step 1: Define the research question

Clarify the research objective, scientific domain, target
population or biological system, variables of interest,
and intended type of literature review.

### Step 2: Develop the review protocol

Define the search concepts, proposed databases, date range,
inclusion criteria, exclusion criteria, and information
that must be extracted from each eligible study.

Distinguish a planned search from a search that has actually
been conducted.

### Step 3: Organize the evidence

Create structured tables containing relevant information,
such as:

- Authors and publication year
- Research objective
- Biological population or study system
- Dataset and sample size
- Experimental or statistical methods
- Software used
- Principal findings
- Study limitations
- Relevance to the review question

Include additional fields when required by the research
question.

### Step 4: Critically assess individual studies

Evaluate the suitability of the research design, data,
statistical methods, assumptions, interpretation, and
reported limitations.

Do not infer that a study used a method or software package
unless the available source supports that conclusion.

### Step 5: Synthesize the literature

Compare studies to identify consistent findings,
contradictory results, methodological differences,
limitations, and unresolved research questions.

Organize the synthesis by scientific theme rather than
merely listing papers one after another.

### Step 6: Identify research gaps

Distinguish clearly between gaps explicitly identified by
The original authors and gaps inferred from comparisons
across studies.

Explain the evidence supporting each proposed research gap.

### Step 7: Report the findings

Present the review using informative headings, clear tables,
and accurate citations.

Identify uncertainties, incomplete evidence, and limitations
in the available literature.

Do not claim that a review is systematic or exhaustive
unless its methods justify that description.
```

### Why does `SKILL.md` need a metadata section?

The beginning of the file contains:

```yaml
---
name: literature-review-assistant
description: Plans, structures, analyzes, and synthesizes scientific literature reviews using transparent criteria and traceable evidence.
---
```

This is called **YAML front matter**. It is a small metadata section at the beginning of a Markdown file.

It tells the plugin system the skill's name and what the skill does.

OpenAI's skill documentation specifies that each skill should have its own directory containing `SKILL.md`, with `name` and `description` in its metadata. ([developers.openai.com](https://developers.openai.com/plugins/build/skills?trk=article-ssr-frontend-pulse_little-text-block&utm_source=chatgpt.com))

The rest of the document contains the instructions ChatGPT should follow when the skill is used.

### How should you write the instructions?

Treat `SKILL.md` as a workflow specification, not simply a general description of the assistant's personality.

For example, compare these two instructions.

**Weak instruction:**

> Help the user with scientific papers.

This is too vague. It does not define what the assistant should do.

**Stronger instruction:**

> Extract the study objective, dataset, sample size, statistical model, software, principal findings, limitations, and relevance to the review question. Use only information supported by the available paper, and explicitly mark missing information as not reported.

The stronger instruction defines both the expected output and the evidence standards.

You can expand the file to include tables, templates, detailed decision rules, or scientific procedures. For a large skill, place supporting material in additional files in the same skill directory and reference those files in `SKILL.md`.

---

# Part 4. Understand the Minimum Required Files

At this point, your plugin contains the two files necessary for the example:

```text
literature-review-assistant/
│
├── plugin.json
│
└── skills/
    └── literature-review-assistant/
        └── SKILL.md
```

Here is the role of each file.

| File | Essential for this example? | Reason |
|---|---|---|
| `plugin.json` | Yes | Identifies the plugin using the recommended portable manifest format. |
| `skills/literature-review-assistant/SKILL.md` | Yes | Provides the actual skill instructions. |
| `README.md` | No | Useful for documentation, but not necessary for this minimal package. |
| `mcp.json` | No | Needed only if you are configuring MCP connections in this format. |
| `.codex-plugin/plugin.json` | No | An optional compatibility manifest for another supported plugin layout. |
| `.mcp.json` | No | Used by the Codex compatibility configuration rather than being interchangeable with portable `mcp.json`. |
| `assets/` | No | Optional directory for supporting assets. |
| `scripts/` | No | Optional supporting code. |

**The key principle is to follow one supported package format consistently.** Do not randomly combine manifest formats from different tutorials.

For the example here, use the root `plugin.json` and the `skills/` directory.

OpenAI documents other compatible manifest locations, including `.codex-plugin/plugin.json`, but the example above uses the portable Agent Plugins format. ([developers.openai.com](https://developers.openai.com/plugins/build/plugins?utm_source=chatgpt.com))

---

# Part 5. Package the Plugin into a ZIP Archive

The ChatGPT interface in your screenshot offers **Add → Upload plugin archive**. You now need to package your directory so that it can be uploaded.

## Step 1. Check the directory structure

Before compressing the directory, confirm that it looks like this:

```text
literature-review-assistant/
├── plugin.json
└── skills/
    └── literature-review-assistant/
        └── SKILL.md
```

There should be only one plugin in this example.

Do not put several unrelated plugin folders into the archive.

The current OpenAI packaging validation documentation specifies that an archive should identify exactly one plugin root, either directly at the archive root or inside a single top-level directory. If you put the plugin in a top-level directory, do not put unrelated files or additional folders alongside that directory in the archive. ([developers.openai.com](https://developers.openai.com/plugins/deploy/submission-errors))

## Step 2. Create the ZIP file on macOS

There are two practical methods.

### Method A: Use Finder

1. Locate the `literature-review-assistant` folder.
2. Right-click or Control-click the folder.
3. Select **Compress "literature-review-assistant"**.
4. macOS creates a ZIP archive, normally named:

   ```text
   literature-review-assistant.zip
   ```

5. Keep the ZIP file somewhere easy to locate, such as your Desktop.

The archive will contain the plugin directory and its files.

### Method B: Use Terminal

Terminal provides a convenient way to package the folder and validate the manifest.

Assuming your plugin directory is on your Desktop, open Terminal and run:

```bash
cd ~/Desktop
```

First, check that `plugin.json` contains valid JSON:

```bash
python3 -m json.tool \
  literature-review-assistant/plugin.json
```

If the JSON is valid, the command prints the formatted manifest. If it is invalid, Python displays an error.

Next, create the archive:

```bash
zip -r literature-review-assistant.zip \
  literature-review-assistant \
  -x "*/.DS_Store"
```

The resulting file is:

```text
~/Desktop/literature-review-assistant.zip
```

This ZIP contains a single top-level plugin directory, with the manifest and skill files beneath it.

## Step 3. Verify the archive

Before uploading, list the files contained in the archive:

```bash
unzip -l ~/Desktop/literature-review-assistant.zip
```

You should see entries similar to:

```text
literature-review-assistant/
literature-review-assistant/plugin.json
literature-review-assistant/skills/
literature-review-assistant/skills/literature-review-assistant/
literature-review-assistant/skills/literature-review-assistant/SKILL.md
```

Check that both `plugin.json` and `SKILL.md` appear in the expected locations.

Avoid accidentally creating a nested directory such as:

```text
literature-review-assistant/
└── literature-review-assistant/
    └── plugin.json
```

An extra level of nesting can prevent the system from recognizing the plugin manifest at the expected location.

---

# Part 6. Upload the Archive to ChatGPT

Now follow the interface shown in your screenshot.

## Step 1. Open the Plugins page

Go to:

[ChatGPT Plugins](https://chatgpt.com/plugins)

You should see the Plugins page with the search bar, installed plugins, and plugin categories.

## Step 2. Open the Add menu

At the upper-right corner of the page, click:

**Add**

In your screenshot, this is the dark button near the top-right corner.

The menu contains options including:

- Create plugin
- Upload plugin archive
- Add custom MCP server

These options represent different ways to create or connect plugin capabilities.

## Step 3. Select Upload plugin archive

Click:

**Upload plugin archive**

This is the correct option for the ZIP file you just created.

Do not select *Add custom MCP server* for the skill-only example. That option is intended for configuring an MCP server connection rather than uploading a packaged skill workflow.

## Step 4. Select your ZIP file

In the file picker, navigate to your Desktop and select:

```text
literature-review-assistant.zip
```

Confirm the selection.

ChatGPT should attempt to process the archive and validate its contents. The available upload flow, permissions, and subsequent steps can depend on your account and workspace configuration. OpenAI's current documentation also notes that workspace uploads can be restricted by role and administrator permissions. ([help.openai.com](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt))

## Step 5. Resolve any validation errors

If the archive is accepted, continue with whatever confirmation or installation steps appear in your interface.

If it fails, read the exact error message rather than immediately rebuilding the entire plugin. Errors can indicate whether the problem is the manifest, directory structure, skill metadata, or another part of the package.

Some useful troubleshooting steps appear in Part 9 below.

## Step 6. Find and use your plugin

After successful import, look for the plugin in the relevant plugin area.

Depending on the interface, it may appear under **Personal**, your workspace, or another applicable section.

If installation is required, complete that step.

Then open a new ChatGPT conversation and try a task related to the skill.

For example:

> Use the Literature Review Assistant workflow to develop a structured extraction template for studies investigating resilience indicators in dairy cattle.

Check whether ChatGPT applies your intended workflow. Modify `SKILL.md` if its output does not meet your requirements.

OpenAI recommends testing a plugin with representative tasks after creation and reviewing its outputs before sharing it. ([help.openai.com](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt?utm_source=chatgpt.com))

---

# Part 7. Optional: Add MCP Tools to Your Plugin

The example so far is a skill-based plugin. It provides reusable instructions, but it does not independently create an external search API, retrieve live database records, or deploy a server.

Suppose you want to expand it so that it can use tools from a scientific literature-search server.

In that case, you may need to add MCP configuration.

## 7.1. What does `mcp.json` do?

In the portable plugin format, `mcp.json` specifies the MCP servers that the plugin should use.

For example, an illustrative configuration could look like this:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "research-tools": {
      "type": "streamable-http",
      "url": "https://your-domain.example/mcp"
    }
  }
}
```

The URL above is a placeholder, not a working server.

The actual configuration must match the transport and endpoint supported by your MCP server. The `streamable-http` setting is appropriate for servers that implement that transport. ([developers.openai.com](https://developers.openai.com/plugins/build/plugins?utm_source=chatgpt.com))

Your directory would now look like this:

```text
literature-review-assistant/
│
├── plugin.json
├── mcp.json
│
└── skills/
    └── literature-review-assistant/
        └── SKILL.md
```

Recreate the ZIP after adding the file.

### An important distinction

Adding `mcp.json` does not automatically create a literature-search server.

You must already have an MCP server or build one, configure its endpoint, and ensure that the connection works in the environment where you intend to use the plugin.

For a local MCP server, availability can depend on the supported execution environment. OpenAI's documentation distinguishes between portable remote MCP configurations and compatibility layouts that can include local applications or other execution requirements. ([developers.openai.com](https://developers.openai.com/plugins/build/plugins?utm_source=chatgpt.com))

## 7.2. When should you use a separate custom MCP server?

If your primary objective is simply to connect ChatGPT to an existing remote MCP server, consider the separate option visible in your screenshot:

**Add → Add custom MCP server**

That is a different workflow from uploading a complete plugin archive.

Choose according to your objective:

| Your objective | Appropriate starting point |
|---|---|
| Package specialized instructions into a reusable workflow | Upload plugin archive |
| Create a literature-review workflow without an external server | Upload a skill-based plugin archive |
| Connect ChatGPT to an existing MCP server | Add custom MCP server |
| Package a workflow that uses MCP tools | Build a plugin with appropriate MCP configuration |
| Develop and distribute a complete plugin | Package it using a supported format, test it, and follow the applicable submission process |

---

# Part 8. An Alternative: Use ChatGPT to Create the Plugin

You do not necessarily need to write every file manually.

The Plugins interface in your screenshot also includes:

**Add → Create plugin**

OpenAI documents Plugin Creator as a way to develop plugins through a conversation. You can describe the workflow, add supporting materials, and work with ChatGPT to create and test the plugin. ([help.openai.com](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt?utm_source=chatgpt.com))

For example, you could start with a request like this:

> Create a plugin named Literature Review Assistant. It should help researchers develop review protocols, establish inclusion and exclusion criteria, extract information from scientific papers, compare methodologies, identify research gaps, and produce structured evidence tables.
>
> Create a skill that defines this workflow. Require traceable evidence, accurate citations, explicit treatment of missing information, and a clear distinction between reported findings and interpretation.
>
> Use a supported plugin format, validate the package structure, and explain how to export or package it for upload.

This is useful when you want ChatGPT to generate the initial files instead of creating them manually.

However, **you should still inspect the resulting files**. Check the manifest, skill instructions, directory structure, and any server configuration before relying on the plugin.

Plugin Creator is an alternative creation route; it does not remove the need for testing and validation. ([help.openai.com](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt?utm_source=chatgpt.com))

---

# Part 9. Troubleshooting Common Upload Errors

When a plugin archive is rejected, the underlying error usually provides a clue about what needs to be corrected.

OpenAI publishes a plugin submission error reference that identifies several structural and validation problems. The exact checks and messages you encounter depend on the particular upload and submission flow. ([developers.openai.com](https://developers.openai.com/plugins/deploy/submission-errors?utm_source=chatgpt.com))

| Problem | Likely cause | What to do |
|---|---|---|
| Plugin manifest missing | No recognized plugin manifest exists at the expected location. | Include a valid root `plugin.json` using the supported portable format. |
| Plugin manifest unreadable | The file is malformed or is not readable text. | Correct its contents and save it as UTF-8 text. |
| Malformed JSON | Missing quotation marks, invalid punctuation, or an extra comma. | Validate the file with `python3 -m json.tool plugin.json`. |
| Plugin root ambiguous | The archive contains multiple competing roots or unexpected directory nesting. | Repackage it so that one plugin is identifiable at the archive root or within one top-level directory. |
| Plugin files missing | The archive contains a manifest but no usable skill or other supported capability for the relevant workflow. | Add the intended skill under `skills/<skill-name>/SKILL.md`. |
| Skill metadata is invalid | The skill's metadata is missing required fields or is malformed. | Add valid `name` and `description` fields to the YAML front matter. |
| MCP configuration missing | The manifest refers to an MCP configuration file that does not exist or is in the wrong location. | Correct the manifest path and provide the matching file in the required format. |
| The plugin imports but does not perform its intended task | The skill instructions are incomplete, irrelevant, or unclear. | Improve the instructions and test them with representative requests. |
| The plugin imports but an external tool fails | The MCP server, endpoint, authentication, or permissions may be incorrect. | Verify the server connection and any required authorization. |

### Three particularly common mistakes

**Mistake 1: Using the wrong manifest format.**

The portable layout in this tutorial uses:

```text
plugin.json
```

at the root of the plugin directory.

Other supported layouts exist, but their configuration requirements differ. Do not take a manifest designed for one format, combine it indiscriminately with files from another format, and assume that the result will work.

**Mistake 2: Putting instructions in the wrong location.**

For the example in this tutorial, the file must be:

```text
skills/literature-review-assistant/SKILL.md
```

A file named `SKILL.md` placed arbitrarily at the root is not the structure you should use for this portable skill package.

**Mistake 3: Assuming a skill automatically provides external functionality.**

A skill provides instructions. It does not automatically create a working external API integration or make a local program accessible to ChatGPT.

For that, you need an appropriate supported tool or application integration. ([developers.openai.com](https://developers.openai.com/plugins/build/plugins?utm_source=chatgpt.com))

---

# Part 10. Final Checklist Before Uploading

Use this checklist to validate the example plugin.

| Check | Requirement | Status to aim for |
|---|---|---|
| 1 | The archive is a ZIP file. | Pass |
| 2 | The plugin has a single identifiable root. | Pass |
| 3 | `plugin.json` is at the root of that plugin. | Pass |
| 4 | `plugin.json` uses a supported format and valid JSON. | Pass |
| 5 | The manifest contains a sensible name, version, and description. | Pass |
| 6 | The skill exists under `skills/<skill-name>/SKILL.md`. | Pass |
| 7 | The skill has valid `name` and `description` metadata. | Pass |
| 8 | The ZIP does not contain unintended extra directories or unrelated files. | Pass |
| 9 | All required supporting files are present. | Pass |
| 10 | The uploaded plugin is tested with realistic requests. | Pass |

The most important structural requirement for the example is that the archive can be recognized as **one plugin containing a valid manifest and a usable skill**. The complete set of checks depends on the capabilities and upload or publication route you choose. ([developers.openai.com](https://developers.openai.com/plugins/build/plugins?utm_source=chatgpt.com))

## Official documentation

These are the main references for the format and workflow described above:

- [OpenAI: Package your plugin](https://developers.openai.com/plugins/build/plugins?utm_source=chatgpt.com) — plugin structure, manifests, skills, MCP configuration, and packaging.
- [OpenAI: Build skills](https://developers.openai.com/plugins/build/skills?trk=article-ssr-frontend-pulse_little-text-block&utm_source=chatgpt.com) — skill directories, `SKILL.md`, and metadata.
- [OpenAI: Plugin submission errors](https://developers.openai.com/plugins/deploy/submission-errors?utm_source=chatgpt.com) — manifest and archive validation errors.
- [OpenAI Help Center: Plugins in ChatGPT](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt?utm_source=chatgpt.com) — creating, using, and uploading plugins.

**My recommendation:** Start by uploading the two-file skill-based plugin from this tutorial. It is easier to validate and test than an MCP-enabled plugin. Once the workflow behaves as expected, you can expand it with reference files, templates, additional skills, or external tools.

---

## User

Export this conversation as markdown file .md
