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

## Step 15 — Continuous improvement without process bloat

After meaningful work, ask:
- What caused rework?
- What was repeatedly unclear?
- What manual step can safely disappear?
- What test caught a real problem?
- What source-of-truth conflict happened?
- What owner action could be eliminated next time?

Only generalize a lesson into AGENTS.md or a shared skill after it has proven reusable. Avoid turning every one-off correction into permanent process.

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
