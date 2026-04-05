**The MCP server you're looking for for Apptio is the open-source Cloudability MCP Server (specifically built for Apptio Cloudability / IBM Cloudability, the core cloud cost management product under Apptio).**

MCP = **Model Context Protocol** — an open standard that turns external APIs (like Apptio’s) into secure, discoverable “tools” that AI agents/chatbots can call directly. This lets you build natural-language data queries (e.g., “Show me last month’s Kubernetes costs by namespace and team” or “Explain this cost spike and forecast next quarter”) without writing custom API code every time.

### Why this one fits your use case
- You have an **approved Apptio API key** → the server supports it natively (legacy Basic Auth with your API key; modern environments also support Bearer `apptio-opentoken`).
- It exposes rich, production-ready tools for exactly the data you’d query in a chatbot: cost reports, Kubernetes/container cost allocation, budgets/alerts, forecasts, billing accounts, etc.
- Runs locally (or you can deploy it anywhere) and connects to any MCP-compatible AI client (Claude Desktop, Cursor, VS Code + Continue, custom agents, etc.).
- Apptio itself does **not** currently offer a public hosted MCP server (their internal MCP is only for the built-in “Conversational Insights” feature inside TBM Studio / Cloudability UI and uses session auth, not API keys).

### Quick setup (5–10 minutes)
1. Clone the repo:  
   ```bash
   git clone https://github.com/eelzinaty/cloudability-mcp-server.git
   cd cloudability-mcp-server
   ```

2. Install dependencies (Python 3.12+ recommended, uses `uv`):  
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv sync
   ```

3. Copy and edit the environment file:  
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your details:  
   ```
   CLOUDABILITY_API_URL=https://api.cloudability.com/v3          # or api-eu.cloudability.com/v3, api-au..., etc.
   CLOUDABILITY_ENVIRONMENT_ID=your-environment-id-here         # optional for legacy API-key mode
   CLOUDABILITY_DEFAULT_VIEW_ID=0                               # optional
   ```

4. Run the server:  
   ```bash
   uv run python run_server.py
   ```
   (It starts a local MCP server — usually on `http://localhost:8000` or similar; the exact port is logged.)

5. Connect to your AI chatbot/tool  
   In your MCP client (Claude Desktop, Cursor, etc.), add it as a custom MCP server. Example config (adjust path):  
   ```json
   {
     "mcpServers": {
       "cloudability": {
         "command": "uv",
         "args": ["run", "python", "main.py"],
         "cwd": "/path/to/cloudability-mcp-server",
         "env": {
           "CLOUDABILITY_API_URL": "https://api.cloudability.com/v3"
         }
       }
     }
   }
   ```
   When the AI tool prompts for auth, use your **approved API key** (Basic Auth: `Basic your-api-key:` — the server handles it).

### What you can query once connected
The AI agent automatically discovers these tools:
- Cost reports (with 15+ dimensions, 8+ metrics, filters, grouping, saved views)
- Kubernetes/container cost allocation & resource usage
- Budget creation, modification, alerts
- Spending forecasts & current-month estimates
- Billing accounts, legacy usage data, etc.

All calls respect Cloudability rate limits and your account permissions.

### Alternatives / notes
- If you’re using **Apptio Targetprocess** (the agile/project side) instead of Cloudability, there are separate MCP servers (e.g., aaronsb/apptio-target-process-mcp or punkpeye/apptio-target-process-mcp).
- Want it hosted 24/7? Deploy the repo on Render, Fly.io, Railway, a VPS, or Kubernetes — it’s container-friendly.
- Need help with a specific chatbot framework (LangChain, CrewAI, custom Claude tool, etc.)? Just share more details about your stack and I can give exact integration steps.

This is the cleanest, most complete way to turn your Apptio data into an AI-enabled query chatbot right now. Let me know if you hit any snags during setup!
