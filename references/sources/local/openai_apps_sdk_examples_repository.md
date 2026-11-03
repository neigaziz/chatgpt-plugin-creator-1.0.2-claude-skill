# OpenAI Apps SDK Examples Gallery

> **Repository:** `openai/openai-apps-sdk-examples`  
> **Original repository URL:** https://github.com/openai/openai-apps-sdk-examples  
> **Default branch:** `main`  
> **Source file:** [README.md](https://github.com/openai/openai-apps-sdk-examples/blob/main/README.md)  
> **License:** MIT ([LICENSE](https://github.com/openai/openai-apps-sdk-examples/blob/main/LICENSE))

This Markdown export reproduces the repository's README and adds direct links to the repository and its important directories. It documents the project as described by the README; it is not a copy of every source file in the repository.

---

# Overview

This repository showcases example UI components for the [OpenAI Apps SDK](https://developers.openai.com/apps-sdk), along with example Model Context Protocol (MCP) servers that expose collections of components as tools. It is intended as a starting point and source of inspiration for building apps for ChatGPT.

## Browser compatibility note

The source README notes that Chrome users who recently updated to version 142 may need to disable the `local-network-access` flag to see widget UI:

1. Open `chrome://flags/`.
2. Find `#local-network-access-check`.
3. Set it to **Disabled**.
4. Restart Chrome for the change to take effect.

See the [Chrome 142 local network access release notes](https://developer.chrome.com/release-notes/142#local_network_access_restrictions).

## MCP and Apps SDK overview

The Model Context Protocol (MCP) is an open specification for connecting large language model clients to external tools, data, and user interfaces. An MCP server exposes tools that a model can call during a conversation. The server returns results according to tool contracts, and those results can include additional metadata—such as inline HTML—that the Apps SDK uses to render rich UI components (widgets) alongside assistant messages.

Within the Apps SDK, MCP keeps the server, model, and UI in sync. By standardising the wire format, authentication, and metadata, it lets ChatGPT reason about a connector in a consistent way.

A minimal MCP integration for the Apps SDK implements three capabilities:

1. **List tools.** The server advertises its supported tools, including JSON Schema input/output contracts and optional annotations (for example, `readOnlyHint`).
2. **Call tools.** When a model selects a tool, it issues a `call_tool` request with arguments matching the user's intent. The server executes the action and returns structured content the model can parse.
3. **Return widgets.** Alongside structured content, the server can return embedded resources in response metadata so the Apps SDK can render the interface inline in ChatGPT.

MCP is transport-agnostic. The README says these examples support both Server-Sent Events and streaming HTTP. The demo MCP servers illustrate how tools can render widgets by combining structured payloads with `_meta.ui.resourceUri` metadata.

## Repository structure

The README describes these principal paths:

| Path | Purpose |
|---|---|
| [`src/`](https://github.com/openai/openai-apps-sdk-examples/tree/main/src) | Source for each widget example. |
| `assets/` | Generated HTML, JavaScript, and CSS bundles after the build step. |
| [`shopping_cart_python/`](https://github.com/openai/openai-apps-sdk-examples/tree/main/shopping_cart_python) | Python MCP server demonstrating how `_meta["widgetSessionId"]` keeps `widgetState` in sync across turns for a shopping-cart widget. |
| [`pizzaz_server_node/`](https://github.com/openai/openai-apps-sdk-examples/tree/main/pizzaz_server_node) | MCP server implemented with the official TypeScript SDK. |
| [`pizzaz_server_python/`](https://github.com/openai/openai-apps-sdk-examples/tree/main/pizzaz_server_python) | Python MCP server returning the Pizzaz widgets. |
| [`solar-system_server_python/`](https://github.com/openai/openai-apps-sdk-examples/tree/main/solar-system_server_python) | Python MCP server for the 3D solar system widget. |
| [`kitchen_sink_server_node/`](https://github.com/openai/openai-apps-sdk-examples/tree/main/kitchen_sink_server_node) | Node MCP server for the kitchen-sink-lite widget. |
| [`kitchen_sink_server_python/`](https://github.com/openai/openai-apps-sdk-examples/tree/main/kitchen_sink_server_python) | Python MCP server for the kitchen-sink-lite widget. |
| [`authenticated_server_python/`](https://github.com/openai/openai-apps-sdk-examples/tree/main/authenticated_server_python) | Python MCP server demonstrating authenticated tool calls. |
| [`build-all.mts`](https://github.com/openai/openai-apps-sdk-examples/blob/main/build-all.mts) | Vite build orchestrator producing hashed bundles for widget entry points. |

The current repository root also contains examples and project files such as `mcp_app_basics_node/`, `cards_against_ai_server_node/`, `package.json`, `pnpm-lock.yaml`, `pnpm-workspace.yaml`, `vite.config.mts`, and TypeScript configuration files. Browse the [repository root](https://github.com/openai/openai-apps-sdk-examples/tree/main) for the complete current listing.

## Example applications

### Pizzaz

Pizzaz contains multiple components demonstrating several view and interaction types, including:

- List view.
- Carousel view.
- Map view.
- An interactive “Pizzaz shop” flow.
- A checkout page.

The example uses the [Apps SDK UI library](https://github.com/openai/apps-sdk-ui) for common components such as images, buttons, and badges.

### Kitchen sink lite

Kitchen sink lite demonstrates the `window.openai` surface working together. It:

- Reads host state such as `toolInput`, `toolOutput`, `displayMode`, `theme`, and `widgetState`.
- Writes host state using `setWidgetState`.
- Calls another MCP tool from the widget using `callTool`.
- Uses host helpers such as `requestDisplayMode`, `openExternal`, and `sendFollowUpMessage`.

Use it as a reference for connecting UI components to MCP tool responses and host APIs with the Apps SDK UI components.

## Prerequisites

- Node.js 18 or later.
- pnpm (recommended), or npm/yarn.
- Python 3.10 or later for the Python MCP servers.
- `pre-commit` for formatting.

## Installation

Clone the repository and install workspace dependencies:

```bash
git clone https://github.com/openai/openai-apps-sdk-examples.git
cd openai-apps-sdk-examples
pnpm install
pre-commit install
```

If using npm or yarn, install the root dependencies with your preferred package manager and adapt the commands below accordingly.

## Build the component gallery

The components are bundled into standalone assets served by the MCP servers as reusable UI resources:

```bash
pnpm run build
```

This command runs `build-all.mts` and produces versioned `.html`, `.js`, and `.css` files inside `assets/`. Each widget is wrapped with the CSS it needs so that bundles can be hosted directly or shipped with a custom server.

For local component development, start the Vite development server:

```bash
pnpm run dev
```

## Serve the static assets

The MCP servers expect bundled HTML, JavaScript, and CSS to be served by the local static file server. After each build, start the asset server before launching MCP processes:

```bash
pnpm run serve
```

Assets are exposed at `http://localhost:4444` with CORS enabled so local tooling, including MCP inspectors, can fetch them.

**Python Pizzaz note:** The Python Pizzaz server caches widget HTML with `functools.lru_cache`. If assets are rebuilt or manually edited, restart the MCP server so it loads the updated markup.

## Run the MCP servers

The repository includes several demonstration MCP servers:

- **Pizzaz (Node and Python):** pizza-inspired collection of tools and components.
- **Solar system (Python):** 3D solar system viewer.
- **Authenticated (Python):** tools requiring different levels of OAuth.
- **Kitchen sink lite (Node and Python):** widget/server pairing demonstrating tool output, widget state, `callTool`, and host helpers.
- **Shopping cart (Python):** shopping cart widget demonstrating how `widgetSessionId` preserves state between tool calls.

### Pizzaz Node server

```bash
cd pizzaz_server_node
pnpm start
```

### Pizzaz Python server

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r pizzaz_server_python/requirements.txt
uvicorn pizzaz_server_python.main:app --port 8000
```

### Authenticated Python server

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r authenticated_server_python/requirements.txt
uvicorn authenticated_python_server.main:app --port 8000
```

### Solar system Python server

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r solar-system_server_python/requirements.txt
uvicorn solar_system_server_python.main:app --port 8000
```

### Kitchen sink lite Node server

```bash
pnpm --filter kitchen-sink-mcp-node start
```

### Kitchen sink lite Python server

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r kitchen_sink_server_python/requirements.txt
uvicorn kitchen_sink_server_python.main:app --port 8000
```

### Shopping cart Python server

This example demonstrates how `_meta["widgetSessionId"]` can carry `widgetState` between tool calls so that the model and widget share the same shopping cart. The widget merges tool responses with previous `widgetState`, and UI actions (such as incrementing quantities) feed back into the shared state so that the assistant sees the latest cart.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r shopping_cart_python/requirements.txt
uvicorn shopping_cart_python.main:app --port 8000
```

For production, persist the cart server-side. See the [shopping cart README](https://github.com/openai/openai-apps-sdk-examples/blob/main/shopping_cart_python/README.md). The demo focuses on the mechanics of keeping state through `widgetSessionId`.

The same Python virtual environment can be reused for all Python servers: install dependencies once, then run the desired entry point.

## Test in ChatGPT

To add these apps to ChatGPT:

1. Enable [developer mode](https://platform.openai.com/docs/guides/developer-mode).
2. Add your apps in **Settings → Connectors**.

To add a local server without deploying it, use a tunnelling service such as [ngrok](https://ngrok.com/) to expose the local server to the internet.

Once an MCP server is running, expose port 8000:

```bash
ngrok http 8000
```

ngrok provides a public URL that can be used to add the local server to ChatGPT under Settings → Connectors. The MCP endpoint will have a form similar to:

```text
https://<custom_endpoint>.ngrok-free.app/mcp
```

### Python MCP SDK host/origin protection

The README notes that the Python MCP SDK enforces DNS rebinding protection. When tunnelling (for example, with ngrok), allow the tunnel host before starting the Python server:

```bash
export MCP_ALLOWED_HOSTS="<custom_endpoint>.ngrok-free.app"
export MCP_ALLOWED_ORIGINS="https://<custom_endpoint>.ngrok-free.app"
```

After adding a connector, it can be used in ChatGPT conversations. Add the app to the conversation context by selecting it in the **More** options. Then invoke its tools by asking a relevant question. For example, the README suggests asking the Pizzaz app: “What are the best pizzas in town?”

![Screenshot showing how to add an app to ChatGPT conversation context](https://github.com/user-attachments/assets/26852b36-7f9e-4f48-a515-aebd87173399)

## Next steps

- **Customise widget data:** Edit handlers in `pizzaz_server_node/src`, `pizzaz_server_python/main.py`, or the solar system server to fetch data from your own systems.
- **Create components:** Add new entries to `src/`; the build script picks them up automatically.

## Deploy the MCP server

The MCP server can be deployed to a cloud environment of your choice. Configure these environment variables:

```bash
BASE_URL=https://your-server.com
API_BASE_URL=https://your-api.example.com
```

`BASE_URL` is used to generate widget HTML that serves static assets from the hosted URL. `API_BASE_URL` is used by client widgets to construct fully qualified API URLs (for example, the Cards Against AI game event stream).

## Contributing

Contributions are welcome through issues and pull requests. The README notes that not every suggestion is guaranteed to be reviewed.

## License

The project is licensed under the MIT License. See the [LICENSE file](https://github.com/openai/openai-apps-sdk-examples/blob/main/LICENSE).

---

## Source and related links

- **Original repository URL:** https://github.com/openai/openai-apps-sdk-examples
- [Original README](https://github.com/openai/openai-apps-sdk-examples/blob/main/README.md)
- [Apps SDK documentation](https://developers.openai.com/apps-sdk)
- [Apps SDK UI library](https://github.com/openai/apps-sdk-ui)
- [Developer mode documentation](https://platform.openai.com/docs/guides/developer-mode)
- [Chrome 142 local network access notes](https://developer.chrome.com/release-notes/142#local_network_access_restrictions)
- [ngrok](https://ngrok.com/)

## Export notes

- Repository information and README content were retrieved from the public `main` branch.
- This file preserves the README's main written content and commands, with formatting and explanatory headings adjusted for standalone reading.
- It is a documentation export, not a full source-code mirror. The repository's source files, assets, commit history, and other documentation remain available at the original repository URL above.
- Commands and paths are reproduced from the source README. Check the live repository for updates before executing them, because the repository can change over time.
