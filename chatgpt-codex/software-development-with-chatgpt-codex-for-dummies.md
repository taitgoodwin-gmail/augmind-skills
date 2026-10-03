# Software Development with ChatGPT Codex for Dummies

**Working document — AugMind**
**Official-source audit:** 2 October 2026 (OpenAI + GitHub); targeted clause refresh and Linear sources checked 3 October 2026.

This is the plain-English operator companion to the formal [AugMind Delivery Baseline](./augmind-delivery-baseline/SKILL.md). It explains what to do, in what order, which tool owns what, and what “done” really means. It is intentionally practical and should improve as the tools, guidance, and our own delivery evidence improve.

## Start here — one small piece of real work

1. **Find the accepted outcome and current evidence.** Read the repo instructions, existing requirement and active issue; identify the next unresolved gate ([Steps 1–3](#step-1--start-with-the-outcome-not-the-tool)).
2. **Name one testable slice.** State its requirement ID, expected behavior, boundaries and verification. Use the existing design target and issue where applicable ([Steps 4–7](#step-4--separate-functional-requirements-from-technicalnfr-requirements)).
3. **Build and check that slice on a working branch.** Record the exact commit, test results and anything NOT RUN; get the review appropriate to the change ([Steps 8–11](#step-8--build-through-bounded-changes)).
4. **Advance only as far as the evidence and authority allow.** Preview, production and owner acceptance are distinct. Finish with the next unresolved gate ([Steps 12–14](#step-12--ship-then-verify-the-release)).

For a concrete walkthrough, read [the Levarum example](#worked-example--save-a-levarum-enquiry-before-confirming-success). Before unattended work, use the [activation and ownership checklist](#activation-and-ownership-proof).

### How to read the source labels

- **Official guidance** links to vendor documentation for the stated capability or advice. It does not make the entire surrounding section an official vendor method.
- **AugMind operating policy** identifies our choices in the [formal baseline](./augmind-delivery-baseline/SKILL.md): gates, ownership, acceptance and operating defaults.
- **Project lesson** identifies dated experience from a specific project. Its evidence and limits matter before reusing it elsewhere.

These labels describe provenance, not OpenAI certification or endorsement. The guide translates the existing method; it does not introduce a new governance service.

## The 30-second version

**AugMind operating policy:** this chain applies the baseline’s eight gates and source-of-truth pattern.

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

**AugMind operating policy:** the delivery-lead role and priority order apply the baseline’s Frame, Plan and Review gates.

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

**Official guidance:** [OpenAI prompting](https://learn.chatgpt.com/docs/prompting) supports a clear goal, context, output, boundaries and verification. **AugMind operating policy:** name this the Frame gate.

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

**Official guidance:** [customization](https://learn.chatgpt.com/docs/customization/overview) and [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) explain instruction layers. **AugMind operating policy:** the baseline’s Context gate and source-of-truth pattern define which project artifact owns each decision.

Before making a new plan, PRD, dashboard, handoff, or tracker:
1. inspect the repo instructions and current branch;
2. inspect the active Linear project/issues;
3. inspect the current requirements/decisions;
4. inspect the approved design target if one exists;
5. identify what is current, proposed, historical, or superseded.

Default rule: **update, don’t multiply.**

## Step 3 — Write requirements so another person or agent can verify them

**Official guidance:** [prompting](https://learn.chatgpt.com/docs/prompting) includes context and verification. **AugMind operating policy:** the requirement fields and evidence statuses below are our practical format, not an OpenAI-mandated PRD schema.

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

**AugMind operating policy:** apply the baseline’s observable outcome and Verify exit check to both behavior and technical constraints. Select the relevant families below from project risk; this is not a vendor-mandated checklist.

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

**AugMind operating policy:** the baseline’s source-of-truth pattern keeps accepted requirements authoritative for scope. **Project lesson:** [Levarum’s dated design comparison](https://github.com/taitgoodwin-gmail/Levarum/blob/8a29675c7ab684d88ef7a876180ccadd5411eb61/docs/verification.md#figma-comparison) records implementation differences and outstanding owner review; a design link alone proves neither parity nor approval.

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

**Official guidance:** Linear [cycles](https://linear.app/docs/use-cycles) are repeating timeboxes not tied to releases; [project milestones](https://linear.app/docs/project-milestones) group issues into project stages (checked 3 October 2026). **AugMind operating policy:** mapping the requirement universe to milestones and admitting only ready work to cycles is our planning choice.

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

**Official guidance:** [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) and [worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees) support bounded parallel work and isolation. **AugMind operating policy:** the Plan gate decides whether that added coordination is useful.

Before code:
- name the current requirement IDs;
- name the expected outcome;
- identify dependencies and blockers;
- identify which tasks can truly run independently;
- define how verification will happen;
- identify owner decisions that cannot safely be delegated.

Use subagents/worktrees when the work is genuinely independent. Do not add agents merely because parallelism is available.

## Step 8 — Build through bounded changes

**Official guidance:** [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [skills/plugins](https://learn.chatgpt.com/docs/skills-and-plugins) and [worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees) describe reusable instructions and isolated work. **AugMind operating policy:** reconcile each change to the accepted requirement, design and issue.

Codex should implement against:
- the requirement;
- the approved design target where relevant;
- the repo’s AGENTS.md;
- the shared skill/baseline;
- the active Linear issue.

Keep changes small enough that a reviewer can understand what changed and why.

Parallel coding streams should use separate worktrees or equivalent isolated environments when they could collide.

## Step 9 — Verify before review

**AugMind operating policy:** the baseline’s Verify gate requires evidence for the changed behavior. **Project lesson:** the [Levarum example](#worked-example--save-a-levarum-enquiry-before-confirming-success) shows why synthetic CI results cannot close hosted private-data or acceptance gates.

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

**Official guidance:** [Codex GitHub review](https://learn.chatgpt.com/docs/third-party/github) is a separate diff review with repository-specific rules. **AugMind operating policy:** our Review gate additionally judges product/design fit and acceptance; those broader judgments need an explicit review scope.

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

**Official guidance:** GitHub documents [branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches), [rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets), [PR reviews](https://docs.github.com/en/pull-requests/reference/pull-request-reviews), [Actions security](https://docs.github.com/en/actions/reference/security/secure-use) and [dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review). **AugMind operating policy:** choose proportionate controls without deadlocking solo work.

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

**Solo operation:** zero required PR approvals is acceptable under AugMind’s no-deadlock rule when an independent approver is unavailable. Record the actual review evidence and remaining acceptance gate; do not call a self-review independent approval. This is not permission to change repository settings or bypass existing rules.

### CI reality check — learned on MindLeverX

**Project lesson:** these are MindLeverX-specific setup observations, not universal installation requirements. Recheck the target repo before copying them.

Do not copy a generic CI recipe and assume it is correct.

- CI must reproduce the **real project prerequisites**, not generic ecosystem habits. MindLeverX intentionally had no npm lockfile/runtime install step, so `npm ci` was the wrong assumption.
- Tests that depend on a separate runtime must install that runtime explicitly. MindLeverX PDF tests needed the pinned Python `reportlab` requirement in CI.
- A failing CI setup is not evidence that the product is broken until the failure is classified. Fix the environment/setup gap first when that is the cause.
- GitHub Dependency Review requires Dependency Graph to be enabled for the repository. Do not install a permanently failing “security check” and call that good governance.
- After a CI change passes on a PR, verify the **post-merge push to main** also passes.
- Only make a check “required” after it has actually run successfully and is appropriate for the repo.

## Step 12 — Ship, then verify the release

**AugMind operating policy:** the baseline’s Ship & Learn gate requires authorized release and evidence in the target environment. A preview or READY deployment alone does not satisfy this checklist.

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

**AugMind operating policy:** this plain-English acceptance ladder summarizes evidence maturity. The formal baseline’s task state machine governs autonomous transitions; neither ladder is an OpenAI mandate.

Use an acceptance ladder such as:

**Not started → Partial → Built → Tested → Production verified → Accepted**

Workflow status and acceptance state are different.

A Linear issue can be **Done** for a bounded technical slice while the larger requirement is still only **Partial**.

## Step 14 — What the owner should actually have to decide

**AugMind operating policy:** these decisions apply the baseline’s permission and approval envelope. **Official guidance:** [OpenAI approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security) explains platform permissions; it does not define AugMind’s business authority.

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

**Official guidance:** [model selection](https://learn.chatgpt.com/docs/model-selection); choose for task complexity, quality, time and cost.

- Use faster/default effort for routine retrieval, formatting, small edits and well-bounded changes.
- Use stronger reasoning for architecture, requirements reconciliation, difficult debugging, security review, cross-system planning and consequential decisions.
- Switch because the task needs it, not because “more thinking” is automatically better.
- Record a model/effort assumption only when it materially affects reproducibility, quality, time or cost.

### ChatGPT Work

**Official guidance:** [ChatGPT Work](https://learn.chatgpt.com/docs/get-started-with-work); confirm the active execution surface before promising continued work.

Use Work for substantial multi-step work that benefits from persistent execution across files/apps/browser tasks. It is closer to handing off a body of work than asking one question.

Do not confuse Work with ordinary chat: a normal chat response ends when the turn ends unless an explicit ongoing/scheduled capability is running.

### Codex cloud environments

**Official guidance:** [cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments). **AugMind operating policy:** publish and test a reusable environment before unattended cloud write work. That local policy is not a prerequisite for automatic Codex GitHub code review, which uses the connected-repository review setup.

Use a reusable cloud environment when coding work needs an isolated, repeatable environment that can be resumed across devices or sessions. Keep environment setup explicit enough that another developer or agent can reproduce it.

### Subagents

**Official guidance:** [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents). **Project lesson:** the dated MindLeverX runtime blocker below is specific to that attempted delegation.

Use subagents for genuinely independent specialist work: e.g. security review, UX review, architecture exploration, or parallel codebase investigation.

The lead agent remains responsible for reconciliation. Five agents disagreeing does not equal a decision.

**Delegation reality check learned on MindLeverX:** a tool can expose an “agent” or delegate field without the workspace actually being configured to run coding sessions. Before promising independent agent work, test that the agent runtime is enabled and has the repository/tool access the task needs. On 2 October 2026, Linear agent delegation was blocked because coding sessions with GitHub code access were not enabled. We recorded the review as queued rather than pretending it ran.

Independence must be real: CI is an independent mechanical check, but it is not an independent product/security judgment; a second pass by the same coordinator is useful review, but it is not an independent reviewer.

### Git worktrees

**Official guidance:** [Git worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees).

Use worktrees when multiple coding streams should progress without colliding in one working directory. Give each stream a bounded ownership area and reconcile through Git/review.

### Code review

**Official guidance:** [Codex GitHub review](https://learn.chatgpt.com/docs/third-party/github) focuses its findings on P0/P1 risks and follows applicable `AGENTS.md` review rules. Automatic review needs repository connection and review configuration; it does not require a user-created cloud environment.

**AugMind operating policy:** use a separate review after build/verification. Explicitly scope broader product, UX, maintainability and requirement review when needed; a quiet P0/P1 review does not prove those checks ran or grant product acceptance.

### Dots / ongoing agents

**Official guidance:** [Dots](https://learn.chatgpt.com/docs/dots). **AugMind operating policy:** choose ongoing execution only for an authorized recurring responsibility.

Use an ongoing agent only for a responsibility that truly needs repeated autonomous work. Do not turn every project into a persistent agent.

### Plugins and MCP

**Official guidance:** [skills/plugins](https://learn.chatgpt.com/docs/skills-and-plugins) and [customization](https://learn.chatgpt.com/docs/customization/overview). **AugMind operating policy:** apply the tool decision rule below.

Use connected tools when they provide authoritative context or a needed action: Linear for work state, GitHub for code/review, Figma for design, Vercel for deployment, etc.

Before adding a tool:
1. Does it give context/action we cannot reliably get already?
2. Does it reduce errors, time or owner effort?
3. Can its result be reconciled into the source of truth?
4. Are its permissions/authority clear?

### Official-doc refresh

**Official guidance:** [Docs MCP](https://learn.chatgpt.com/learn/docs-mcp). **AugMind operating policy:** preserve source dates and resolve changes in the existing source index.

For changing OpenAI behavior, commands, models or access:
- check current official guidance;
- prefer the current linked docs over an older newsletter/screenshot/chat memory;
- use Docs MCP when available for current guidance inside Codex;
- do not claim a feature is active merely because it exists in documentation.

## Step 15 — Continuous improvement without process bloat

**Official guidance:** [building skills](https://learn.chatgpt.com/docs/build-skills) covers reusable skill authoring and testing. **AugMind operating policy:** Ship & Learn and “update, don’t multiply” determine when a lesson belongs in shared guidance.

After meaningful work, ask:
- What caused rework?
- What was repeatedly unclear?
- What manual step can safely disappear?
- What test caught a real problem?
- What source-of-truth conflict happened?
- What owner action could be eliminated next time?

Only generalize a lesson into AGENTS.md or a shared skill after it has proven reusable. Avoid turning every one-off correction into permanent process.

## Autopilot mode — how to automate without losing control

**AugMind operating policy:** this section summarizes the [baseline’s autonomous delivery control](./augmind-delivery-baseline/SKILL.md#autonomous-delivery-control). The two-retry limit, two write-heavy streams, two-run circuit breaker and named state ladder are local defaults, not OpenAI mandates. **Official guidance:** [approvals/security](https://learn.chatgpt.com/docs/agent-approvals-security) and [worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees) explain supporting platform boundaries and isolation.

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

### Activation and ownership proof

Use the existing issue/run record or handoff; do not create a new tracker. Before claiming the method is active for a run, record:

- **Loaded source/version:** the baseline actually read (path or URL plus commit/blob or installed package version), applicable `AGENTS.md` and project requirements. A shared-skill link in a repo proves a reference exists, not that every run loaded it. If it was not read, say so.
- **Work key and owner:** the existing issue/task key, one active write owner, current branch/worktree and starting commit; reconcile any prior run before writing.
- **Authority and next gate:** current verified state, allowed actions, owner decisions and the next exit check. Verify tools/runtime access before promising execution.
- **Evidence and handoff:** resulting commit/CI/preview identifiers, what actually ran, NOT RUN/BLOCKED items, review author/result and next responsible owner. Do not infer independent review or product acceptance from CI.

This is proof of using the existing baseline, not a new approval layer. Record only what is material to the run; never put credentials or private customer records in the ledger.

## Worked example — save a Levarum enquiry before confirming success

**Project lesson — evidence snapshot, checked 3 October 2026.** The outcome is simple: a visitor sends an enquiry, gets a truthful receipt after a private durable save, and can retry an uncertain save without losing the draft. This example traces existing work; it does not authorize another live submission or declare the MVP accepted.

**Exact scope:** working branch `codex/design-assessment-fixes-20261001`, commit [`8a29675c7ab684d88ef7a876180ccadd5411eb61`](https://github.com/taitgoodwin-gmail/Levarum/commit/8a29675c7ab684d88ef7a876180ccadd5411eb61). At this check it is not merged into `main` (`04a7927d728cd97e5c7ad39bab7cd749157dd6f3`). The links below are pinned to the example commit so later branch changes cannot silently rewrite the evidence.

| Link in the chain | Concrete source and meaning |
|---|---|
| Requirement | [docs/REQUIREMENTS.md, R04 and public contracts](https://github.com/taitgoodwin-gmail/Levarum/blob/8a29675c7ab684d88ef7a876180ccadd5411eb61/docs/REQUIREMENTS.md): acknowledge only after durable private save; preserve input on failure and request identity on unchanged retry. R07 keeps a call request distinct from a booking. The proposed MVP contract is still an owner-review proposal. |
| UX | [ContactRequest.tsx](https://github.com/taitgoodwin-gmail/Levarum/blob/8a29675c7ab684d88ef7a876180ccadd5411eb61/src/prospect/ContactRequest.tsx) displays the receipt only after successful submission and says a requested call is not booked. [useSubmission.ts](https://github.com/taitgoodwin-gmail/Levarum/blob/8a29675c7ab684d88ef7a876180ccadd5411eb61/src/prospect/useSubmission.ts) requires `saved:true`, retains retry identity for unchanged content and surfaces uncertainty. This is implemented behavior, not a new claim of Figma approval. |
| Code | [api/leads.ts](https://github.com/taitgoodwin-gmail/Levarum/blob/8a29675c7ab684d88ef7a876180ccadd5411eb61/api/leads.ts) awaits the save before acknowledging; notification failure does not negate a saved enquiry. [server/private-save.ts](https://github.com/taitgoodwin-gmail/Levarum/blob/8a29675c7ab684d88ef7a876180ccadd5411eb61/server/private-save.ts) reconciles an uncertain write only by reading the exact private key and matching supplied fields. Its 12-second write and five-second read budgets bound saver waiting, not the total request or an uncooperative provider operation. |
| Failure tests | [tests/leads.test.mjs](https://github.com/taitgoodwin-gmail/Levarum/blob/8a29675c7ab684d88ef7a876180ccadd5411eb61/tests/leads.test.mjs) checks pending/failed saves and notification failure. [tests/private-save.test.mjs](https://github.com/taitgoodwin-gmail/Levarum/blob/8a29675c7ab684d88ef7a876180ccadd5411eb61/tests/private-save.test.mjs) covers stalled read bodies and writes that ignore cancellation. [Browser failure/retry cases](https://github.com/taitgoodwin-gmail/Levarum/blob/8a29675c7ab684d88ef7a876180ccadd5411eb61/tests/browser/release-acceptance.mjs) check retained input, missing success and stable retry identity with mocked responses. |
| Commit and CI | [Run 37066436277](https://github.com/taitgoodwin-gmail/Levarum/actions/runs/37066436277) checked out this exact SHA: 50 unit/model tests passed, build/boundary checks passed and 11 synthetic browser suites passed. Both `check` and `browser-qa` completed successfully. The [workflow](https://github.com/taitgoodwin-gmail/Levarum/blob/8a29675c7ab684d88ef7a876180ccadd5411eb61/.github/workflows/check.yml) disables live submissions; these are mechanical checks, not a hosted private-data test. |
| Preview | The prior handoff associates [this preview](https://levarum-g1pzud5ue-mind-lever-gmail.vercel.app) with the checkpoint and reports READY metadata only. This guide edit did not open the preview or revalidate deployment identity/runtime. READY does not prove the enquiry reached private storage or that an owner can retrieve it. |
| Existing evidence | [docs/verification.md, public save deadlines checkpoint](https://github.com/taitgoodwin-gmail/Levarum/blob/8a29675c7ab684d88ef7a876180ccadd5411eb61/docs/verification.md#public-save-deadlines-and-contract-reconciliation--2026-10-02) links before/after regressions and browser receipts. Historical hosted passes elsewhere in that file belong to their older checkpoints. |

**How to read the result:** the recorded synthetic checks are PASS. Fresh hosted provider-stall, private-storage/readback, owner authentication/recovery, real assistive-technology and production-pilot checks are **NOT RUN at this checkpoint**. Product/owner acceptance is **not established**. CI and preview metadata do not promote this slice to PREVIEW VERIFIED, PRODUCTION VERIFIED or ACCEPTED; report the narrower mechanical evidence and leave the unresolved gates open.

**Next handoff:** the responsible project owner must resolve the existing live-verification/release and acceptance gates within authorized scope. Reuse the existing requirement and verification records. No app tests, live POSTs, customer-data reads or deployment/access changes were performed to write this example.

## The tool ownership map

**AugMind operating policy:** these are working ownership conventions from the baseline, not exclusive vendor capabilities.

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

**AugMind operating policy:** use the baseline’s completion statement and the evidence for this specific increment.

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
- https://docs.github.com/en/pull-requests/reference/pull-request-reviews
- https://docs.github.com/en/actions/reference/security/secure-use
- https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review

Linear (Step 6, checked 3 October 2026):
- https://linear.app/docs/use-cycles
- https://linear.app/docs/project-milestones

## Working-document rule

This guide is expected to change.

When guidance or actual delivery evidence changes:
1. verify the current official source;
2. distinguish new product capability from new advice;
3. test the workflow on real work where practical;
4. update this guide and/or the formal baseline only where the lesson is reusable;
5. preserve material historical reasoning in Git rather than silently rewriting history.
