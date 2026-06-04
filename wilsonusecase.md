**Market Trends and Latest Innovations (as of June 2026)**

The AI-powered analytics and incident management space is exploding with **agentic AI** and **chat-native interfaces** replacing traditional static dashboards. ServiceNow itself has opened its full platform to external AI agents (via MCP and NowAssist integrations), enabling custom tools like yours to pull or analyze exported incident data seamlessly. Key trends include:

- **Chat-first BI over dashboards**: Engineers prefer natural-language chatbots for incident queries (e.g., “Show me high-priority incidents assigned to Network team last month with resolution trends”) instead of clicking through filters. Tools like Streamlit + LLM chat are the fastest way to ship these internally.

- **Claude Code CLI dominance for rapid data apps**: Creators on X and blogs are using Claude Code CLI (Anthropic’s terminal agent) + structured files (CLAUDE.md + skills) to build full production-grade Streamlit apps in hours. This includes pandas analysis, Plotly charts, AgGrid tables, and Claude API-powered chatbots. Skills and Plan Mode reduce hallucinations and ensure professional, consistent output.

- **ServiceNow-specific innovation**: Real-world examples show Claude analyzing ServiceNow exports directly (filters by date/priority/group, auto-generated React/HTML dashboards, pattern detection). MCP connectors exist for live ServiceNow access, but for a worksheet-based app like yours, file-upload + in-memory RAG is the gold standard.

- **Professional dashboard expectations**: Dark/light themes, responsive layouts, custom CSS, sidebar filters, tabbed views (Overview | Charts | Incidents | AI Chat), export buttons, and zero-config deployment. Streamlit 1.3x+ with Plotly + Streamlit-AgGrid delivers “enterprise polish” in <500 lines.

This project is perfectly timed — you can ship a best-in-class tool faster than ever using Claude Code CLI’s framework.

**Exact Sequence of Steps to Build Your Professional ServiceNow Incidents Dashboard Using Claude Code CLI’s Standard Framework**

Follow this battle-tested workflow shared across top X creators and Anthropic docs. It uses the exact files you mentioned (CLAUDE.md, SKILLS.md / skills/, Plan.md / Plan Mode) plus the modern .claude/ structure that prevents context bloat and ensures consistency.

### Phase 0: Setup (5 minutes)
1. Install/verify Claude Code CLI (if not done):  
   `npm install -g @anthropic-ai/claude-code` (or use the native binary).  
   Run `claude --version` and log in with your Anthropic account (Pro/Max recommended for long contexts).

2. Create a clean project folder:  
   `mkdir servicenow-incident-dashboard && cd servicenow-incident-dashboard`

3. Initialize git: `git init`

### Phase 1: Create the Claude Framework Files (10-15 minutes)
Start Claude Code in the folder:  
`claude`

Then run these one by one (Claude will create the files for you):

**Step 1 – Create CLAUDE.md** (your project’s permanent memory)  
Prompt Claude:  
`/plan Create CLAUDE.md in the root with these exact sections:  
1. Project Overview (professional Streamlit dashboard for analyzing ServiceNow Incidents worksheet – columns include Incident Number, Opened/Closed Date, Assignment Group, Priority, State, Category, Description, etc.)  
2. Target User (IT Ops/ServiceNow admins who want beautiful visuals + AI chatbot)  
3. Tech Stack & Versions (Python 3.11+, Streamlit 1.42+, pandas, plotly, streamlit-aggrid, openpyxl, anthropic SDK)  
4. UI/Design Rules (very professional, clean, ServiceNow-inspired blue accents, dark/light theme support, sidebar filters, tabbed layout, responsive, custom CSS for polish)  
5. Coding Conventions & Security (no secrets in code, .env for API keys, type hints, error handling)  
6. Project Structure (list all expected files/folders)  
7. Success Criteria (runs on localhost:8501, handles Excel/CSV upload, beautiful charts by assignment group/priority/trends, AI chatbot that analyzes the full dataframe via Claude API)  
Keep it under 180 lines. Use clear markdown.`  

Claude will generate and save it. Review with `cat CLAUDE.md` and approve.

**Step 2 – Create skills/ folder and key SKILL.md files** (reusable expertise)  
Create these skills (they load only when needed, keeping context clean):  
- `/skill create-streamlit-dashboard` (professional UI patterns, custom CSS, tabs, filters)  
- `/skill data-analysis-viz` (best Plotly charts for incidents: bar by Assignment Group, line trends over time, priority pie, MTTR calculations, etc.)  
- `/skill ai-chatbot-rag` (load dataframe to session state, in-context analysis with Claude API, safe pandas query generation)  
- `/skill professional-polish` (CSS, themes, loading spinners, export buttons)  

Prompt:  
`Create a skills/ folder with SKILL.md files for the four skills above. Use proper YAML frontmatter (name, description, when to use). Make instructions extremely detailed and reusable.`

**Step 3 – (Optional but powerful) Create AGENTS.md or .claude/agents/**  
For parallel work: one agent for UI, one for data viz, one for chatbot logic.

**Step 4 – Create .env.example** (for ANTHROPIC_API_KEY) and .gitignore.

### Phase 2: Build the App Iteratively (30-60 minutes total)
Now the fun part — Claude does the heavy lifting.

**Step 5 – High-level Plan**  
In Claude Code:  
`/plan Build the complete Streamlit app. Start with requirements.txt, then app.py. Follow CLAUDE.md strictly. Use the skills I just created. First create the file structure, then implement step-by-step.`

Claude will output a detailed plan. Approve it.

**Step 6 – Let Claude execute**  
- Say: “Execute the plan. Create requirements.txt first.”  
- Then: “Continue – create app.py with upload, data preview, sidebar filters, tabbed dashboard (Overview, Charts, Raw Data, AI Chatbot).”  
- Use skills inline: “Use /skill create-streamlit-dashboard and /skill data-analysis-viz”  
- For the chatbot: “Implement the AI Chatbot using the anthropic SDK + the dataframe in session state. Support natural language queries like ‘What’s the average resolution time for P1 incidents in Networking group?’”

**Step 7 – Test & Polish Loop** (repeat as needed)  
- Run locally: `streamlit run app.py` (or ask Claude: “Run streamlit run app.py and show me any errors”)  
- Use `!streamlit run app.py` inside Claude Code for instant feedback.  
- Fix with: “Review the current app.py against CLAUDE.md and professional-polish skill. Make it beautiful.”  
- Add features iteratively: date range picker, assignment group multiselect, export CSV/Excel, dark mode toggle.

**Step 8 – Final Validation**  
- Prompt: “Run a full code review using all skills. Ensure it looks very professional and works with sample ServiceNow incident data.”  
- Commit: `git add . && git commit -m "Initial professional ServiceNow dashboard with AI chatbot"`

**Step 9 – (Advanced) Add extras**  
- MCP connector for live ServiceNow (if you want to go beyond worksheets)  
- Deploy button (Streamlit Community Cloud or Docker)  
- Persistent memory skill so the chatbot remembers previous questions in the session

### Expected Outcome
You’ll end up with a single `app.py` that:
- Uploads your ServiceNow Excel/CSV
- Shows a gorgeous, filterable dashboard (charts by Assignment Group, priority heatmaps, trend lines, KPIs)
- Includes a professional AI Chatbot tab that truly understands your data (powered by Claude)
- Runs perfectly at http://localhost:8501

This exact workflow is what top creators use to ship polished tools in one session. Total time: 1–2 hours once the framework files are set.

Start with Step 1 right now in your terminal (`claude` → create CLAUDE.md).  
Drop the first file here if you want me to review it before you proceed — happy to help refine prompts or the CLAUDE.md content.

You’ve got this — this dashboard will save your team dozens of hours per week. Let’s build it! 🚀
