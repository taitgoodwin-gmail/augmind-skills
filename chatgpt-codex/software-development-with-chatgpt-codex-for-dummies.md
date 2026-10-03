# Software Development with ChatGPT Codex for Dummies

**Working document — AugMind**
**Last checked against current OpenAI + GitHub guidance:** 2 October 2026

This is the plain-English operator companion to the formal [AugMind Delivery Baseline](./augmind-delivery-baseline/SKILL.md). It explains what to do, in what order, which tool owns what, and what “done” really means. It is intentionally practical and should improve as the tools, guidance, and our own delivery evidence improve.

## The 30-second version

Use one chain:

**Need → journey → requirement → design target → implementation issue → code → test → production verification → acceptance → learning**

Do not let ChatGPT, Codex, Figma, Linear, GitHub, and Vercel each become a separate source of truth.

- **Requirements say what must be true.**
- **Figma says what the approved experience should look like.**
- **Linear says what we are working on and where it stands.**
- **GitHub says what the code and durable technical instructions actually are.**
- **Codex builds and reviews bounded changes.**
- **Vercel/production says what is actually running.**
- **The browser and real user journey decide whether it really works.**

If those disagree, stop the silent drift and deliberately update the correct source.

## Who is “in charge”?

For substantial work, ChatGPT acts as **delivery lead / product manager first** and uses engineering, UX, QA, security, DevOps, commercial, and red-team lenses as needed.

The priority order is:
1. unblock the critical path to working software;
2. deliver or validate customer value;
3. make sure the requirement is ready enough to build without guessing;
4. respect dependencies;
5. reduce security, data, architecture, and irreversible-release risk;
6. prefer the smallest complete testable slice;
7. run genuinely independent work in parallel;
8. require observable evidence before advancing status.

## Step 1 — Start with the outcome, not the tool

Bad:
> Make a dashboard.

Better:
> An owner can see the three things needing action today, understand why, and reach the underlying evidence in under one minute.

Before work starts, answer:
- Who is the user?
- What outcome must happen?
- What must not change?
- What decision or evidence is authoritative?
- How will we know it worked?

This is the **Frame** gate.

## Step 2 — Find the current source of truth before creating anything

Before making a new plan, PRD, dashboard, handoff, or tracker:
1. inspect the repo instructions and current branch;
2. inspect the active Linear project/issues;
3. inspect the current requirements/decisions;
4. inspect the approved design target if one exists;
5. identify what is current, proposed, historical, or superseded.

Default rule: **update, don’t multiply.**

## Step 3 — Write requirements so another person or agent can verify them

There is no magic OpenAI PRD template. Codex needs clear behavior, relevant context, boundaries, and verification.

A useful requirement has:
- stable ID;
- short title;
- behavior/outcome;
- dependencies;
- acceptance test(s);
- unresolved decision(s), if any;
- authority/provenance;
- status.

For consequential work, link a discrete executable case with:
- fixed prerequisites/input/version;
- numbered actions;
- expected observable result;
- PASS / FAIL / BLOCKED rules;
- actual evidence;
- cleanup;
- what was not tested.

**NOT RUN is not PASS.**
**BLOCKED is not FAIL.**

## Step 4 — Separate functional requirements from technical/NFR requirements

Functional requirement:
> The user can request a report.

Technical/NFR requirement:
> A successful report request is persisted durably before success is returned, retries do not duplicate fulfillment, failure is observable, and sensitive data is not exposed.

Typical technical requirement families:
- security and authorization;
- tenant/data isolation;
- persistence and integrity;
- retry/idempotency/recovery;
- retention/deletion;
- interface/API compatibility;
- schema migration;
- configuration validation;
- performance/timeouts;
- observability/alerting;
- rate/abuse controls;
- dependency/artifact integrity;
- accessibility;
- deployment verification/rollback;
- backup/disaster recovery.

Do not invent arbitrary numerical SLOs just to make a requirement look technical. Derive thresholds from the user journey, risk, economics, or an applicable external standard.

## Step 5 — Use design to discover requirements, but then reconcile them

It is fine to start with a prototype. A design can expose requirements you did not know you needed.

After discovery:
1. write or update the requirement;
2. identify the user journey;
3. select one approved Figma file/frame when visual behavior matters;
4. link that design target to the requirement;
5. identify the implementation issue and tests.

**Figma is the approved visual target, not the product scope authority.**

Do not have ChatGPT, Codex, Claude, and Figma independently redesign the same thing at the same time.

## Step 6 — Put the full universe in milestones; put only ready work in cycles

Linear concepts:
- **Project:** the outcome/deliverable.
- **Milestone:** a meaningful stage of that outcome.
- **Issue:** an executable unit of work.
- **Cycle:** a repeating near-term execution window. A cycle is not a release.

Do not dump the entire requirement catalog into one sprint/cycle.

Use milestones to harmonize the whole requirement universe. Put only the ready, dependency-resolved issues into the current or next cycle.

Each cycle should have one plain-English goal, for example:
> Close the pilot-definition gate so accepted evidence collection can begin.

## Step 7 — Plan the smallest safe increment

Before code:
- name the current requirement IDs;
- name the expected outcome;
- identify dependencies and blockers;
- identify which tasks can truly run independently;
- define how verification will happen;
- identify owner decisions that cannot safely be delegated.

Use subagents/worktrees when the work is genuinely independent. Do not add agents merely because parallelism is available.

## Step 8 — Build through bounded changes

Codex should implement against:
- the requirement;
- the approved design target where relevant;
- the repo’s AGENTS.md;
- the shared skill/baseline;
- the active Linear issue.

Keep changes small enough that a reviewer can understand what changed and why.

Parallel coding streams should use separate worktrees or equivalent isolated environments when they could collide.

## Step 9 — Verify before review

Verification asks:
> Did it behave as specified?

Run:
- targeted tests;
- regression tests;
- negative/failure-path tests where material;
- accessibility/device checks where relevant;
- build/static checks;
- deployed/runtime checks where applicable.

For UI, inspect the actual rendered experience.
For integrations, test the actual boundary.
For production claims, verify production.

“Tests passed” does not mean “MVP accepted.”

## Step 10 — Review separately from verification

Review asks:
> Even if it works, is this the right change?

Review against:
- user outcome;
- requirement;
- approved design;
- privacy/security;
- technical architecture;
- maintainability;
- business/commercial boundary;
- scope.

Use Codex/GitHub review as a separate pass when code changes are consequential.

Where independence matters, the builder should not be the only reviewer.

## Step 11 — GitHub safety rails

For important repositories, follow current GitHub guidance proportionately:
- work through branches/PRs rather than uncontrolled direct changes to the protected default branch;
- protect the default branch/ruleset;
- require relevant status checks before merge;
- require review where the team has an independent reviewer available and that requirement will not deadlock solo operation;
- resolve review conversations before merge where appropriate;
- keep CI permissions minimal;
- review dependency changes;
- pin third-party GitHub Actions to full commit SHAs when feasible for stronger supply-chain integrity;
- preserve a clear source-to-artifact and release identity.

A repository rule is a **delivery control**, not automatically a product requirement.

### CI reality check — learned on MindLeverX

Do not copy a generic CI recipe and assume it is correct.

- CI must reproduce the **real project prerequisites**, not generic ecosystem habits. MindLeverX intentionally had no npm lockfile/runtime install step, so `npm ci` was the wrong assumption.
- Tests that depend on a separate runtime must install that runtime explicitly. MindLeverX PDF tests needed the pinned Python `reportlab` requirement in CI.
- A failing CI setup is not evidence that the product is broken until the failure is classified. Fix the environment/setup gap first when that is the cause.
- GitHub Dependency Review requires Dependency Graph to be enabled for the repository. Do not install a permanently failing “security check” and call that good governance.
- After a CI change passes on a PR, verify the **post-merge push to main** also passes.
- Only make a check “required” after it has actually run successfully and is appropriate for the repo.

## Step 12 — Ship, then verify the release

Before calling something shipped:
1. confirm the exact commit/artifact;
2. confirm the target environment;
3. confirm required environment/config values;
4. deploy;
5. verify the real URL/application;
6. verify private paths/data stay private;
7. verify the core journey;
8. record the release identifier;
9. know the rollback/recovery path.

The browser/runtime is the truth when code and docs disagree.

## Step 13 — Acceptance is a separate state

Use an acceptance ladder such as:

**Not started → Partial → Built → Tested → Production verified → Accepted**

Workflow status and acceptance state are different.

A Linear issue can be **Done** for a bounded technical slice while the larger requirement is still only **Partial**.

## Step 14 — What the owner should actually have to decide

The owner should not project-manage the tools.

Bring the owner only decisions that materially change:
- product scope;
- customer promise;
- price/commercial terms;
- design direction where alternatives matter;
- spend;
- publication/release;
- external outreach;
- privacy/security policy;
- irreversible or high-risk architecture choices.

Everything else should be prepared, verified, and presented with a recommendation and evidence.

## Newer OpenAI capabilities — use the right one, don’t use all of them

These capabilities can materially improve delivery, but they are **tools, not process stages**. Availability can vary by plan, workspace, rollout, region, and surface; verify current access before designing the workflow around one.

### Model and reasoning-effort choice
- Use faster/default effort for routine retrieval, formatting, small edits and well-bounded changes.
- Use stronger reasoning for architecture, requirements reconciliation, difficult debugging, security review, cross-system planning and consequential decisions.
- Switch because the task needs it, not because “more thinking” is automatically better.
- Record a model/effort assumption only when it materially affects reproducibility, quality, time or cost.

### ChatGPT Work
Use Work for substantial multi-step work that benefits from persistent execution across files/apps/browser tasks. It is closer to handing off a body of work than asking one question.

Do not confuse Work with ordinary chat: a normal chat response ends when the turn ends unless an explicit ongoing/scheduled capability is running.

### Codex cloud environments
Use a reusable cloud environment when coding work needs an isolated, repeatable environment that can be resumed across devices or sessions. Keep environment setup explicit enough that another developer or agent can reproduce it.

### Subagents
Use subagents for genuinely independent specialist work: e.g. security review, UX review, architecture exploration, or parallel codebase investigation.

The lead agent remains responsible for reconciliation. Five agents disagreeing does not equal a decision.

**Delegation reality check learned on MindLeverX:** a tool can expose an “agent” or delegate field without the workspace actually being configured to run coding sessions. Before promising independent agent work, test that the agent runtime is enabled and has the repository/tool access the task needs. On 2 October 2026, Linear agent delegation was blocked because coding sessions with GitHub code access were not enabled. We recorded the review as queued rather than pretending it ran.

Independence must be real: CI is an independent mechanical check, but it is not an independent product/security judgment; a second pass by the same coordinator is useful review, but it is not an independent reviewer.

### Git worktrees
Use worktrees when multiple coding streams should progress without colliding in one working directory. Give each stream a bounded ownership area and reconcile through Git/review.

### Code review
Treat Codex/GitHub review as a separate gate after build/verification. Review should look for correctness, regressions, security, maintainability and requirement mismatch—not merely restate that tests passed.

### Dots / ongoing agents
Use an ongoing agent only for a responsibility that truly needs repeated autonomous work. Do not turn every project into a persistent agent.

### Plugins and MCP
Use connected tools when they provide authoritative context or a needed action: Linear for work state, GitHub for code/review, Figma for design, Vercel for deployment, etc.

Before adding a tool:
1. Does it give context/action we cannot reliably get already?
2. Does it reduce errors, time or owner effort?
3. Can its result be reconciled into the source of truth?
4. Are its permissions/authority clear?

### Official-doc refresh
For changing OpenAI behavior, commands, models or access:
- check current official guidance;
- prefer the current linked docs over an older newsletter/screenshot/chat memory;
- use Docs MCP when available for current guidance inside Codex;
- do not claim a feature is active merely because it exists in documentation.

## Step 15 — Continuous improvement without process bloat

After meaningful work, ask:
- What caused rework?
- What was repeatedly unclear?
- What manual step can safely disappear?
- What test caught a real problem?
- What source-of-truth conflict happened?
- What owner action could be eliminated next time?

Only generalize a lesson into AGENTS.md or a shared skill after it has proven reusable. Avoid turning every one-off correction into permanent process.

## Autopilot mode — how to automate without losing control

When work is scheduled, delegated, or expected to advance without continuous owner steering, use the formal autonomy contract in the AugMind Delivery Baseline. The short version:

- **One durable work key** per autonomous task, normally the Linear issue ID.
- **One active writer per work key.** A new run reuses the existing branch/PR/evidence rather than creating a competing stream.
- **Two write-heavy streams per repository by default.** Read-heavy QA/review can parallelize more freely.
- **Every writer is isolated** in its own worktree or cloud workspace.
- **Retry transient failures only twice.** Repeated deterministic or permission failures become BLOCKED; no endless repair loops.
- **Classify failures before fixing them:** environment, implementation, requirement, external dependency, permission/configuration, or owner decision.
- **Use the state ladder:** READY → CLAIMED → BUILDING → VERIFIED → REVIEWED → PREVIEW VERIFIED → PRODUCTION VERIFIED → ACCEPTED.
- **Hard gates beat prompts:** protected main, required CI, review, environment validation, deployment identity, and recovery checks should prevent bypass.
- **Normal autonomous work stops at PR/preview** unless merge/release authority is explicit and the repository/release gates are active.
- **A scheduled task does not inherit authority** to spend, contact customers, change product scope, weaken security/privacy, or perform destructive production changes.

### What should happen automatically

Inside accepted scope, the system should be able to reconcile state, claim ready work, create isolated branches/worktrees, implement bounded reversible changes, run tests/builds, open PRs, update Linear/evidence, verify previews, and diagnose ordinary CI/test failures.

### What should interrupt the owner

Interrupt only for material scope/customer-promise changes, pricing/commercial terms, meaningful design alternatives, spend, external communication, privacy/security policy, destructive data changes without verified recovery, or irreversible/high-risk architecture choices.

### When the automation should stop itself

Stop the affected action when the same material blocker survives two scheduled runs, when a required independent reviewer cannot run, when the task would need broader permissions than its role, or when the system cannot prove the state transition it is trying to claim. Continue unrelated safe work instead of stopping the whole project.

## The tool ownership map

| Tool | Primary job | Do not use it as |
|---|---|---|
| ChatGPT | Delivery leadership, synthesis, decisions, tool orchestration | Invisible background worker after a reply ends |
| Codex | Coding, repository analysis, implementation, code review | Product-scope authority |
| Figma | Approved visual/interaction target | Requirements database |
| Linear | Execution control, milestones, cycles, dependencies, status | Canonical technical contract |
| GitHub | Code, durable repo instructions, PR/review history, technical truth | Product roadmap |
| Vercel | Deployment/runtime evidence | Requirements authority |
| Browser/production | Final observable runtime truth | Substitute for missing requirements |

## The core completion checklist

Before saying “done,” answer:
- Which requirement(s) did this satisfy?
- Which design target did it implement, if any?
- What changed in code?
- What tests ran?
- What failed or remains NOT RUN?
- Was the deployed result verified?
- Is owner/customer acceptance required?
- What is the next unresolved gate?

## Current official guidance sources

OpenAI:
- https://learn.chatgpt.com/docs/prompting
- https://learn.chatgpt.com/docs/model-selection
- https://learn.chatgpt.com/docs/customization/overview
- https://learn.chatgpt.com/docs/agent-configuration/agents-md
- https://learn.chatgpt.com/docs/skills-and-plugins
- https://learn.chatgpt.com/docs/build-skills
- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://learn.chatgpt.com/docs/environments/git-worktrees
- https://learn.chatgpt.com/docs/third-party/github
- https://learn.chatgpt.com/docs/agent-approvals-security

GitHub:
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews
- https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions
- https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-dependency-review

## Working-document rule

This guide is expected to change.

When guidance or actual delivery evidence changes:
1. verify the current official source;
2. distinguish new product capability from new advice;
3. test the workflow on real work where practical;
4. update this guide and/or the formal baseline only where the lesson is reusable;
5. preserve material historical reasoning in Git rather than silently rewriting history.
