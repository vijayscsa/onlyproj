# Creating Agents using Claude Code CLI

## Slide 1 — Title
**Creating Agents using Claude Code CLI**
Build repeatable agents with skills, tools, and project rules

Speaker notes: This deck shows how to turn Claude Code from a chat session into a constrained agent that plans, uses tools, and stops when the job is done.

## Slide 2 — What an agent is here
**An agent is a loop with a goal, tools, and a stop rule**
- Not a new model — same Claude, different control surface
- Goal is stated in the prompt or CLAUDE.md
- Tools are the actions it may take
- Skills supply procedures only when relevant
- The session ends when the stop condition is met

Speaker notes: Contrast this with a normal chat where the user drives every step. An agent is allowed to act across multiple tool calls inside limits you set.

## Slide 3 — Core building blocks
**Five pieces make a Claude Code agent**
- CLAUDE.md — persistent project rules
- Skills — SKILL.md workflows loaded on demand
- Tools — read, edit, bash, and any allowed extras
- Permissions — what it may run without asking
- Stop condition — done, blocked, or needs a human

Speaker notes: You do not need all five on day one. CLAUDE.md plus a tight tool allow-list is enough for a first agent.

## Slide 4 — Project setup checklist
**Set the workspace before the first agent run**
- Install Claude Code and sign in
- Add the skills marketplace and document-skills if you need files
- Create CLAUDE.md with goal, constraints, and output paths
- Decide allowed tools and deny dangerous commands
- Put example inputs in a known folder

Speaker notes: A clean folder with one CLAUDE.md beats a long prompt you retype every session.

## Slide 5 — The agent loop
**Plan, act, check, then continue or stop**
1. Plan the next concrete step
2. Use one tool or skill
3. Read the result
4. Continue only if the goal is unfinished
5. Stop and report when the stop condition hits

Speaker notes: Skills are not always in context. Claude loads a skill when the task matches its description.

## Slide 6 — Skills vs project rules
**Use each control for a different job**
- CLAUDE.md — always-on rules for this repo
- Skill — reusable procedure, loaded only when relevant
- Plugin — packaged set of skills
- Prompt — one-run goal and inputs

Speaker notes: Do not dump every workflow into CLAUDE.md. Keep permanent policy there and put procedures in skills.

## Slide 7 — Constrain the tools
**An agent is only as safe as its allow-list**
- Allow read and edit in the project
- Allow bash only for named commands
- Deny network or package installs unless required
- Require a human for deletes, force-push, and secrets
- Log outputs to a folder you can review

Speaker notes: Start narrow. Add a tool only after a run fails because it was missing.

## Slide 8 — Example: research agent
**A file-writing research agent**
- Goal: summarize a topic into notes.md and sources.md
- Tools: read, write, web search if enabled
- Rules: cite sources, no invented links, max 8 sections
- Stop: both files exist and a short summary is printed
- Output: ./outputs/research/

Speaker notes: This is the simplest useful agent. It has a visible done state.

## Slide 9 — Example: coding agent
**A test-driven coding agent**
- Goal: implement the change and keep tests green
- Tools: read, edit, bash for test and git status
- Rules: do not commit unless asked, do not change unrelated files
- Stop: tests pass or a blocker is reported
- Output: diff plus a short run log

Speaker notes: The stop condition is a command result, not the model saying it is finished.

## Slide 10 — Debugging a bad run
**When the agent drifts, tighten the loop**
- Paste the failing command output back in
- Restate the stop condition in one line
- Remove unused tools for that run
- Ask it to plan only, then approve the plan
- Split one large goal into two sessions

Speaker notes: Most failures are vague goals or too many permissions, not a missing feature.

## Slide 11 — Failure modes
**These are the usual breaks**
- Keeps editing after the task is done
- Invents files or APIs it did not read
- Runs broad shell commands
- Loads the wrong skill
- Hides a blocker inside a long summary

Speaker notes: Fix with a written stop rule, an allow-list, and a required final checklist.

## Slide 12 — Starter layout
**A minimal agent folder**
- CLAUDE.md — goal, tools, stop rule
- .claude/skills/ — optional local skills
- inputs/ — source material
- outputs/ — files the agent must produce
- prompts/run.md — the exact kickoff prompt

Speaker notes: Commit CLAUDE.md and skills. Do not commit secrets or large generated binaries.

## Slide 13 — Build one today
**Five steps for the first agent**
1. Write a one-sentence goal
2. Name the output files
3. Allow only the tools that goal needs
4. Add a stop condition
5. Run once, then edit CLAUDE.md from the failure

Speaker notes: Ship the smallest agent that produces a file you can open.

## Slide 14 — Summary
**Agents are constrained loops, not open chat**
- Rules live in CLAUDE.md
- Procedures live in skills
- Tools are an allow-list
- Done means the stop condition passed
- Review the files, not only the summary

Speaker notes: Close by pointing at the research-agent example as the thing to copy first.







Use the pptx skill. Read agents-outline.md and create a 14-slide PowerPoint from it.

Rules:
- One slide per "## Slide" section
- Use the bold line as the slide title
- Use the bullets as slide body
- Put "Speaker notes" into the speaker notes, not on the slide
- Professional theme, short bullets, no extra slides
- Save as creating-agents-claude-code.pptx in the current directory
