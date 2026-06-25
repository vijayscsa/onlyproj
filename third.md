**Best Project Folder Structure for Agentic AI Applications using Claude Code CLI (2026 Latest)**

This structure is synthesized from Anthropic’s official documentation (especially the `.claude` directory explorer and Skills/Plugins/Hooks guides), recent Anthropic engineering posts on **harness design** and long-running agents, and top community patterns from engineers heavily using Claude Code for agentic systems.

It optimizes for:
- **Skills** (dynamic, on-demand workflows with `SKILL.md`)
- **Plugins** (bundled skills + hooks + MCP + agents)
- **Harness engineering** (the full system around the agent: memory, permissions, hooks, tools, observability)
- **Loop engineering** (agent loops with scheduling, sub-agents, parallel execution via worktrees/batch, context management, and hooks)

### Recommended Root Structure

```bash
agentic-ai-app/                          # Your agentic application project
├── CLAUDE.md                            # Core project memory (committed)
├── CLAUDE.local.md                      # Personal notes (gitignore)
├── .mcp.json                            # MCP server connections (tools/APIs)
├── .worktreeinclude                     # (Optional) Control worktree behavior
│
├── .claude/                             # ← The "Harness Control Center" (commit most of this)
│   ├── settings.json                    # Permissions, hooks config, tool allowlists (committed)
│   ├── settings.local.json              # Personal permission overrides (gitignore)
│   │
│   ├── rules/                           # Modular, path-scoped instructions (highly recommended)
│   │   ├── architecture.md
│   │   ├── testing.md
│   │   ├── agent-loop-patterns.md
│   │   ├── security.md
│   │   └── frontend/                    # Scoped rules
│   │       └── component-conventions.md
│   │
│   ├── skills/                          # Reusable agent skills (SKILL.md + supporting files)
│   │   ├── feature-development/         # e.g., grill-me → PRD → issues → TDD
│   │   │   └── SKILL.md
│   │   ├── code-review/
│   │   │   └── SKILL.md + checklist.md
│   │   ├── tdd/
│   │   │   └── SKILL.md
│   │   ├── agent-orchestrator/          # For multi-agent loops
│   │   │   └── SKILL.md + scripts/
│   │   ├── harness-design/              # Meta-skill for improving your own harness
│   │   └── deploy-staging/
│   │       └── SKILL.md
│   │
│   ├── agents/                          # Specialized sub-agent personas/definitions
│   │   ├── planner.md
│   │   ├── implementer.md
│   │   ├── reviewer.md
│   │   ├── security-auditor.md
│   │   └── researcher.md
│   │
│   ├── hooks/                           # Deterministic shell scripts (lifecycle events)
│   │   ├── pre-tool-use/
│   │   ├── post-edit.sh                 # e.g., auto-format, lint
│   │   ├── stop.sh                      # e.g., update memory/docs
│   │   └── startup.sh
│   │
│   ├── workflows/                       # Dynamic workflows / loop configurations
│   │   └── long-running-feature.md
│   │
│   ├── docs/                            # Reference material loaded by skills/agents
│   │   ├── architecture-decisions/
│   │   └── harness-patterns.md
│   │
│   └── plugins/                         # Local plugin bundles (optional)
│       └── my-team-plugin/
│           ├── plugin.json
│           ├── skills/
│           └── hooks/
│
├── src/                                 # Your actual agentic application code
│   ├── agents/
│   ├── skills/                          # (If your app exposes its own skills)
│   ├── harness/
│   ├── tools/
│   ├── memory/
│   ├── loops/
│   └── ...
│
├── tests/
├── docs/                                # Human-readable docs + architecture
├── scripts/                             # Utility scripts
└── ...
```

### Global (Personal) Layer — `~/.claude/`

This lives in your home directory and applies across **all** projects:

```bash
~/.claude/
├── CLAUDE.md
├── settings.json
├── rules/
├── skills/          # Your personal reusable skills (e.g., mattpocock-style)
├── agents/
├── plugins/         # Installed plugins live here
└── projects/        # Auto-memory / session history (optional)
```

**Key Principle**:  
Project-level (`.claude/`) wins over global when there are conflicts. Commit team-shared harness components; keep personal ones in `~/.claude/`.

### Why This Structure Is Optimal (Anthropic Engineer-Aligned)

| Component          | Purpose in Agentic Systems                          | Key Benefit for Harness/Loop Engineering          | Commit?     |
|--------------------|-----------------------------------------------------|---------------------------------------------------|-------------|
| **CLAUDE.md**      | High-level project memory & routing                 | Consistent context across sessions                | Yes        |
| **.claude/rules/** | Modular, path-scoped instructions                   | Prevents context bloat; precise loading           | Yes        |
| **.claude/skills/**| Reusable, dynamically loaded procedures             | Core of agentic workflows (on-demand expertise)   | Yes        |
| **.claude/agents/**| Sub-agent personas                                  | Parallelism & specialization in loops             | Yes        |
| **.claude/hooks/** | Deterministic pre/post actions                      | Reliability, enforcement, automation              | Yes        |
| **settings.json**  | Permissions + hook wiring                           | Safety & governance layer of the harness          | Yes        |
| **.mcp.json**      | External tool connections                           | Extends agent capabilities beyond local tools     | Yes        |
| **Plugins**        | Packaged bundles (skills + hooks + MCP + agents)    | Easy sharing & distribution of harness pieces     | Optional   |

### Additional Best Practices for Agentic Apps

1. **Harness Engineering Focus**:
   - Treat `.claude/` as your **agent harness configuration**.
   - Use `rules/` + `CLAUDE.md` for memory layer.
   - Use `hooks/` + `settings.json` for permissions & deterministic behavior.
   - Use `skills/` + `agents/` for the intelligence layer.

2. **Loop Engineering**:
   - Design recurring loops using `/loop` + hooks.
   - Use sub-agents + worktrees for parallel execution.
   - Skills like `agent-orchestrator` can manage supervisor → worker patterns.

3. **Monorepo Support**:
   - You can have nested `.claude/skills/` inside subfolders (e.g., `apps/web/.claude/skills/`).
   - Use qualified names like `/apps/web:deploy`.

4. **Development Workflow Tips**:
   - Start with `/init` to generate a good `CLAUDE.md`.
   - Use the **skill-creator** skill/plugin to help build new skills.
   - Keep `CLAUDE.md` relatively short — make it a **router** that points to `rules/` and `docs/`.
   - Version control the entire `.claude/` folder (except `settings.local.json`).

This structure gives you maximum leverage of Claude Code’s latest capabilities while keeping the project clean, shareable with your team, and scalable as your agentic application grows in complexity.

Would you like me to expand on any specific part (e.g., example contents for `CLAUDE.md`, a sample `SKILL.md`, hook examples, or how to structure the actual `src/` for a production agentic app)? Or tailor this for a specific type of agentic application (e.g., multi-agent system, RAG agent, autonomous coding agent)?
