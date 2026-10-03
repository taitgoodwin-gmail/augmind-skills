---
name: augmind-delivery-baseline
description: Use for substantial product, software, AI, website, workflow, or transformation delivery work that should follow AugMind's repeatable governed lifecycle across projects. Establishes delivery gates, source-of-truth rules, safe autonomy levels, task claiming/idempotency, concurrency, retries/circuit breakers, subagents/worktrees/cloud environments, verification, review, release controls, and evidence-based completion. Do not use for trivial one-step requests.
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

## Autonomous delivery control

Use this section whenever work is unattended, scheduled, delegated, parallelized, or expected to advance without continuous owner steering. Autonomy is an execution mode inside the eight gates, not a ninth gate.

### Autonomy levels

Use the lowest level that can accomplish the task:

- **OBSERVE** — read, reconcile, diagnose, and report. No persistent writes.
- **PREPARE** — update planning/evidence systems, create bounded branches/worktrees, prepare commits/PRs/previews, but do not merge or release.
- **EXECUTE** — make reversible implementation changes that are already authorized by accepted requirements/design and remain behind PR/review/release gates.
- **RELEASE** — merge, deploy, migrate, publish, or perform other externally consequential actions only when that authority is explicit and the hard release gates are active.

A scheduled task or agent does not gain authority merely because it can technically perform an action.

### Task state machine

For consequential software work, track the highest verified state rather than inferring completion from workflow status:

**READY → CLAIMED → BUILDING → VERIFIED → REVIEWED → PREVIEW VERIFIED → PRODUCTION VERIFIED → ACCEPTED**

Side states:

- **BLOCKED** — a prerequisite, dependency, access, or decision is unavailable.
- **FAILED** — the attempted change or verification produced a reproducible failure.
- **OWNER DECISION** — proceeding would materially change scope, promise, design direction, spend, privacy/security policy, external communication, or an irreversible/high-risk architecture choice.

Rules:
- Do not skip a state whose evidence is required for the next state.
- NOT RUN is never PASS.
- BLOCKED is not FAILED.
- Linear/GitHub workflow labels do not override the acceptance state.
- CI success is mechanical verification, not independent product/business acceptance.

### Task claiming and idempotency

Every autonomous write task needs one durable work key, normally the issue identifier (for example MIN-27).

Before creating or mutating anything:
1. Check whether the issue, branch/worktree, PR, deployment, comment, or evidence record already exists.
2. Reuse or update the existing artifact when it represents the same work.
3. Permit only one active write owner for one work key at a time.
4. Record the branch/PR/commit/deployment identifiers back in the existing execution source.
5. Never create a second workstream merely because a prior run ended or lost conversational context.

A retry must be safe to repeat. If an action cannot be made idempotent, require an explicit precondition check or owner approval before repeating it.

### Concurrency and isolation

Default to:
- read-heavy exploration, test analysis, security review, and summarization may run in parallel when independent;
- no more than **two concurrent write-heavy streams per repository** unless a written plan explains why more are safe;
- parallel writers must use separate worktrees or isolated cloud workspaces;
- two write streams must not own the same files, migration, release state, or external side effect;
- the lead agent owns reconciliation and may stop a stream when boundaries overlap.

Do not confuse more agents with more throughput. Prefer the smallest parallel set that shortens the critical path.

### Retry and circuit-breaker policy

Classify before retrying.

**Transient external/tool failure**
- Retry at most twice with bounded backoff when the action is safe and idempotent.
- Preserve the original error and each retry result.

**Deterministic build/test/requirement failure**
- Do not blindly retry.
- Diagnose, make one bounded corrective change, and rerun the relevant verification.

**Permission/configuration/decision blocker**
- Do not retry until the prerequisite changes.

**Recurring scheduled blocker**
- If the same material blocker prevents progress on two consecutive scheduled runs, stop attempting that action, mark it BLOCKED, continue independent work, and surface one concise exception.

Never run an unbounded repair loop.

### Failure classification

Record one primary class before deciding the next action:

1. **Environment** — runtime, dependency, CI, setup, or cloud-environment mismatch.
2. **Implementation** — product/code defect.
3. **Requirement** — built behavior conflicts with accepted requirement or acceptance case.
4. **External dependency** — provider/tool/service unavailable or changed.
5. **Permission/configuration** — missing access, secret, repository rule, agent runtime, or environment setting.
6. **Owner decision** — material choice cannot be delegated safely.

A failing CI environment is not evidence of a product defect until classified.

### Permission and approval envelope

Default autonomous actions inside accepted scope:
- read/reconcile repositories, requirements, Linear, Figma, CI, previews, logs, and deployment metadata;
- update existing execution/evidence records;
- create isolated branches/worktrees;
- implement bounded reversible changes against accepted requirements;
- run tests, static checks, builds, and approved preview deployments;
- open PRs and request/perform allowed review;
- repair ordinary test/CI defects that do not change product scope or security policy.

Require explicit owner authority before:
- changing product scope, customer promise, price/commercial terms, or approved design direction where alternatives matter;
- spending money or adding paid services;
- contacting customers/partners or sending external communications;
- changing privacy/security policy, production access policy, or secret handling;
- destructive data changes or migrations without a verified recovery path;
- merging/releasing when repository/release gates are not active;
- irreversible or materially risky architecture changes.

Use the narrowest filesystem, network, connector, and production permissions that still let the assigned role complete its task.

### Scheduled tasks, worktrees, and cloud environments

- For scheduled Git work in a local/remote project, use a dedicated background worktree so it cannot collide with an interactive checkout.
- For Codex Cloud, use a **published and tested** reusable environment before unattended write work; each new task should start in its isolated workspace from that environment.
- Do not claim an environment is reproducible until a fresh task has completed setup, build/tests, and the required start/browser checks.
- Keep production credentials and destructive permissions out of build/review agents unless their role explicitly requires them.
- A normal chat ending is not a persistent worker; only an active scheduled/ongoing/cloud execution mechanism continues later.

### Independent verification and review

Separate these roles when consequences justify it:
- **Builder** changes the system.
- **Verifier/QA** proves specified behavior and failure paths.
- **Reviewer** judges requirement, architecture, security, maintainability, and design fit.
- **Production verifier** checks the actual release/runtime.

The builder may run its own tests, but that does not become independent review. CI is independent mechanical evidence, not independent judgment. If a required independent reviewer cannot run, mark the review BLOCKED/NOT RUN rather than substituting the coordinator silently.

### Hard-gate principle

Convert important prose rules into enforceable controls whenever the platform supports it:
- protected default branch / ruleset;
- PR-before-merge;
- required status checks;
- resolved review conversations;
- least-privilege workflow permissions;
- dependency and security checks appropriate to the repository;
- test/build/validation scripts;
- environment/config validation;
- deployment identity and rollback/recovery checks.

Agent instructions explain behavior. Infrastructure prevents bypass.

### Autonomous run completion

Every unattended run should end with a compact ledger:
- work keys claimed;
- state transitions made;
- exact evidence created or checked;
- retries performed;
- blockers/circuit breakers;
- any owner decision required;
- next READY work.

If the run cannot prove a transition, leave the prior state unchanged.

## Completion statement

Never claim a stage or project is complete unless the observable exit check was actually verified. State what is verified, what remains unverified, and what gate comes next.
