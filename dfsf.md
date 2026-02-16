graph TD
    subgraph GitHub_Environment [GitHub Repository]
        A[Human Developer] -- Pushes Code --> B{Pull Request}
        B -- Triggers --> C[CI: PR Checks]
        C -- Status: Failure --> D[Self-Healing Workflow]
        L[GitHub App] -- Generates Token --> D
        D -- Pushes Fix Commit --> B
        B -- Re-triggers --> C
    end

    subgraph Automation_Logic [Self-Healing Job]
        D --> E{Safety Guards}
        E -- Is Draft? / Is Bot? / Has 'no-autofix'? --> F[STOP: Exit]
        E -- Pass --> G[Collect Failure Logs]
        G --> H[Claude Code AI]
        H -- Analyzes Logs & Code --> I[Apply Fixes]
        I -- Verify Locally --> J[Push Commit]
    end

    style D fill:#f96,stroke:#333,stroke-width:2px
    style H fill:#bbf,stroke:#333,stroke-width:2px
    style F fill:#f66,stroke:#333