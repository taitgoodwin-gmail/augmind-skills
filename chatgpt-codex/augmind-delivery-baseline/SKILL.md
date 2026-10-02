---
name: augmind-delivery-baseline
description: Use for substantial product, software, AI, website, workflow, or transformation delivery work that should follow AugMind's repeatable governed lifecycle across projects. Establishes the current delivery gate, prompt structure, planning, build, verification, review, deployment, learning, tool use, subagent/worktree rules, and source-of-truth discipline. Do not use for trivial one-step requests.
---

# AugMind Delivery Baseline

This is the shared operating baseline for repeatable AugMind project delivery. Project-specific requirements and accepted decisions remain authoritative for *what* to build; this skill governs *how* to work unless a project has an explicit justified override.

Use current primary guidance before materially changing this workflow. Canonical OpenAI URLs are maintained in the root README of the `augmind-skills` repository.

## Core rule

**Update, don't multiply.** Before creating a new plan, requirements file, dashboard, handoff, or status document, identify the existing authoritative artifact and update it when safe. Create a new artifact only when a genuinely new function requires one.

For every substantial task:
1. Identify the current delivery gate.
2. State the intended observable outcome.
3. Use the minimum context and tools needed.
4. Work in the existing source of truth.
5. Verify the result before advancing the gate.
6. Record material decisions where the project already tracks them.

## The eight gates

### 1. FRAME — What are we trying to accomplish?
**Why:** Work drifts when the desired result, audience, constraints, and definition of done are implicit.

**Do**
- State the user/business outcome, not merely the activity.
- Identify authoritative inputs and existing sources of truth.
- Name constraints: scope, spend, publication, data, external contact, design, platform, deadlines, and approvals.
- Define an observable completion check.

**Agent mode:** Single lead agent by default.

**Exit check:** One unambiguous outcome and a testable definition of done exist.

**Official guidance**
- Prompting: https://learn.chatgpt.com/docs/prompting
- Projects: https://learn.chatgpt.com/docs/projects

### 2. CONTEXT — What do we already know?
**Why:** Re-researching and conflicting artifacts waste time and create false authority.

**Do**
- Retrieve current repo state, active issue(s), current requirements/decisions, and relevant prior work.
- Distinguish current, historical, proposed, and superseded material.
- Prefer current primary sources; preserve source dates and URLs.
- Reuse verified guidance rather than researching again unless freshness matters.

**Agent mode:** Single lead; delegate bounded inventory only when the source set is large and separable.

**Exit check:** The authoritative baseline is identified; contradictions and unknowns that could change the task are surfaced.

**Official guidance**
- Projects: https://learn.chatgpt.com/docs/projects
- Codex customization: https://learn.chatgpt.com/docs/customization/overview

### 3. PROMPT — What exactly are we asking AI to do?
**Why:** Clear task framing reduces rework without over-specifying implementation.

Use OpenAI's prompt components proportionately:
- **Goal** — the result needed.
- **Context** — only information that can change the result.
- **Output** — the required form and level of detail.
- **Boundaries** — what must stay unchanged; what requires approval.
- **Verification** — what must be checked before claiming completion.

Describe the result first. Describe a process only when the process itself matters.

**Agent mode:** Single lead agent.

**Exit check:** Someone unfamiliar with the thread could execute the prompt without guessing material intent.

**Official guidance**
- Prompting: https://learn.chatgpt.com/docs/prompting

### 4. PLAN — What is the smallest safe path?
**Why:** Large tasks become manageable when dependencies, decisions, and test points are explicit before implementation.

**Do**
- Break the work into small outcome-based chunks.
- Put dependencies before dependent work.
- Identify decisions that genuinely require the owner.
- Prefer reversible changes.
- Map each chunk to an existing issue when project tracking exists.

**Use subagents when**
- Workstreams are substantively independent and can be reconciled by a lead.
- Independent specialist review would materially improve the decision.
- Parallel codebase exploration will save meaningful time.

**Do not use subagents when**
- One agent can complete the task cleanly.
- Workstreams would edit the same files or require constant coordination.
- Extra agents add token/process overhead without independent value.

**Exit check:** The next executable chunk is clear, bounded, and independently verifiable.

**Official guidance**
- Subagents: https://learn.chatgpt.com/docs/agent-configuration/subagents
- Customization order: https://learn.chatgpt.com/docs/customization/overview

### 5. BUILD — Execute one bounded increment.
**Why:** Small increments make errors visible and keep design, scope, and code from diverging.

**Do**
- Implement against the accepted source, requirement, design target, or issue.
- Use tools through MCP/plugins when external systems are needed.
- Use a Git worktree for parallel coding streams that should not disturb the local checkout.
- Keep each worktree/agent to a clear ownership boundary.
- Preserve existing scope and accepted decisions unless new evidence justifies a change.

**Agent mode:** Lead + bounded implementation subagents only when Gate 4 justified them.

**Exit check:** The increment exists in the intended system and is ready for verification.

**Official guidance**
- Skills & Plugins: https://learn.chatgpt.com/docs/skills-and-plugins
- Worktrees: https://learn.chatgpt.com/docs/environments/git-worktrees
- Cloud environments: https://learn.chatgpt.com/docs/environments/cloud-environments

### 6. VERIFY — Did the thing actually work?
**Why:** Generated code, documents, designs, and deployments are not complete merely because creation succeeded.

**Do**
- Run the tests/checks relevant to the changed behavior.
- Test failure paths and boundaries when material.
- Verify the actual deployed/rendered/integrated result when deployment or UI changed.
- Separate "not tested" from "failed."
- Record evidence sufficient for another person to reproduce the check.

**Agent mode:** A separate QA/reviewer agent is useful when independence materially improves assurance; it does not substitute for real customer or external validation.

**Exit check:** Each acceptance criterion is PASS, FAIL, or BLOCKED with evidence.

**Official guidance**
- Code review: https://learn.chatgpt.com/docs/code-review
- GitHub integration: https://learn.chatgpt.com/docs/third-party/github

### 7. REVIEW — Should we accept this increment?
**Why:** Passing tests proves defined behavior, not that the change is the right product/design/business decision.

**Do**
- Review the diff/output against goal, constraints, UX/design target, security/privacy, and project requirements.
- Use Codex code review for code changes where applicable.
- Surface material tradeoffs and remaining uncertainty.
- Ask the owner only for decisions that cannot be safely delegated.

**Agent mode:** Independent product/design/security/red-team review when consequences justify it.

**Exit check:** Accepted, revised, or rejected with a clear reason; no ambiguous "looks done."

**Official guidance**
- Code review: https://learn.chatgpt.com/docs/code-review
- GitHub: https://learn.chatgpt.com/docs/third-party/github

### 8. SHIP & LEARN — Release safely and improve the baseline.
**Why:** A repeatable process closes the loop; shipping without evidence or learning creates recurring mistakes.

**Do**
- Deploy/release only within explicit authorization boundaries.
- Verify the release in its actual environment.
- Record the release identifier/version and rollback path where applicable.
- Compare the observed result with the original completion check.
- Feed reusable lessons into the existing skill/AGENTS/project guidance only when they are stable enough to generalize.

**Ongoing agents / Dots**
Use ongoing agents only for goals that genuinely require repeated autonomous monitoring or execution, and only when the capability is available and authorized. Do not replace a bounded task with a persistent agent merely because it exists.

**Exit check:** Release is verified, rollback is understood where relevant, and any reusable lesson is captured without spawning duplicate governance.

**Official guidance**
- Cloud environments: https://learn.chatgpt.com/docs/environments/cloud-environments
- Dots: https://learn.chatgpt.com/docs/dots
- Skills & Plugins: https://learn.chatgpt.com/docs/skills-and-plugins

## Shared source-of-truth pattern

Use the smallest useful set:
- **Repository + AGENTS.md:** durable code/project instructions and technical truth.
- **Issue tracker (e.g. Linear):** current execution status, ownership, dependencies, and next work.
- **Existing business/requirements source:** accepted business decisions and requirements.
- **Shared skill:** repeatable cross-project method.
- **Source index:** canonical external guidance URLs and dates checked.

Do not make dashboards, handoffs, meeting notes, emails, Figma frames, or AI chats authoritative merely because they are newer.

## Tool and agent decision rule

Before adding a tool or agent, ask:
1. Does it provide context or action we cannot get reliably from the current source?
2. Will it materially reduce time, errors, or owner effort?
3. Can its output be reconciled into the existing source of truth?
4. Is its authority boundary clear?

If not, keep the workflow simpler.

## Completion statement

Never claim a stage or project is complete unless the observable exit check was actually verified. State what is verified, what remains unverified, and what gate comes next.
