# augmind-skills

AugMind skill packages and installation guides, organized separately for Claude and ChatGPT/Codex.

## Reusable delivery baseline

The cross-project execution method lives at `chatgpt-codex/augmind-delivery-baseline/SKILL.md`.

Use it for substantial product, software, AI, website, workflow, or transformation delivery work. It defines eight gates — Frame → Context → Prompt → Plan → Build → Verify → Review → Ship & Learn — plus tool, subagent, worktree, verification, and source-of-truth rules.

For the plain-English operator companion, use [Software Development with ChatGPT Codex for Dummies](chatgpt-codex/software-development-with-chatgpt-codex-for-dummies.md). It is a working document that translates the formal baseline into day-to-day tool ownership, sequencing, acceptance, and delivery practices.

Project repositories should keep only their project-specific overlay in `AGENTS.md`; do not duplicate the full baseline into every repo.

## Official guidance source index

Use current primary documentation before changing a reusable workflow. Record the date checked, preserve the canonical URL, and prefer the current docs over newsletter wording when they differ.

**Last checked:** 2026-10-02

### Core OpenAI delivery guidance

| Topic | Canonical source | Why it matters |
|---|---|---|
| Projects and chats | https://learn.chatgpt.com/docs/projects | Keep ongoing work and shared context together; separate chats by distinct outcome. |
| Prompting | https://learn.chatgpt.com/docs/prompting | Prompt structure: goal, context, output, boundaries; Codex prompts should include verification. |
| Model selection | https://learn.chatgpt.com/docs/model-selection | Choose model/reasoning level based on complexity, latency, cost, and quality. |
| Codex customization | https://learn.chatgpt.com/docs/customization/overview | Layer AGENTS.md, skills/plugins, MCP, and subagents. |
| AGENTS.md | https://learn.chatgpt.com/docs/agent-configuration/agents-md | Durable global and repository instructions loaded before Codex work. |
| Skills & Plugins | https://learn.chatgpt.com/docs/skills-and-plugins | Reusable workflows; explicit or implicit skill invocation. |
| Build skills | https://learn.chatgpt.com/docs/build-skills | Author, test, install, and share reusable skills. |
| Subagents | https://learn.chatgpt.com/docs/agent-configuration/subagents | Parallelize independent work; avoid unnecessary write conflicts and token overhead. |
| Codex CLI | https://learn.chatgpt.com/docs/codex/cli | Install, run, resume, review, and automate Codex locally. |
| Developer commands | https://learn.chatgpt.com/docs/developer-commands | Current slash-command reference, including /plan, /goal, /worktree, /review, /agent and /subagents. |
| Git worktrees | https://learn.chatgpt.com/docs/environments/git-worktrees | Run parallel Codex chats without colliding in the same working tree. |
| Cloud environments | https://learn.chatgpt.com/docs/environments/cloud-environments | Reusable isolated Codex Cloud environments across desktop, web, and mobile. |
| GitHub code review | https://learn.chatgpt.com/docs/third-party/github | Review PRs, enable automatic reviews, and use AGENTS.md review rules. |
| Agent approvals & security | https://learn.chatgpt.com/docs/agent-approvals-security | Sandboxing, approvals, network controls, and secure local execution. |
| Docs MCP | https://learn.chatgpt.com/learn/docs-mcp | Connect Codex to OpenAI's current official docs so guidance can be refreshed during work. |
| ChatGPT Voice | https://learn.chatgpt.com/docs/features/voice | Talk through and steer Chat, Work, and Codex tasks. |

### DevDay 2026 email audit

Source email: **“DevDay 2026: What’s new for developers”**, received 2026-10-02. All substantive destinations below were reviewed against current official documentation.

| Email destination | Canonical current page | Reusable implication |
|---|---|---|
| Explore what launched / Read more in recap | https://learn.chatgpt.com/docs/whats-new/devday-2026 | DevDay feature map and launch links. |
| Codex in the cloud — Learn more | https://learn.chatgpt.com/docs/environments/cloud-environments | Use reusable cloud environments for work that should continue across devices. |
| Codex CLI — Install the new CLI | https://learn.chatgpt.com/docs/codex/cli | Local coding, review, scripting, and repeatable workflows. |
| Code review — Try code review | https://learn.chatgpt.com/docs/third-party/github | Add a review gate before merge/deploy; automatic reviews can be enabled. |
| Dots — eligible markets / Meet dots | https://learn.chatgpt.com/docs/dots | Ongoing agent responsibility when rollout, plan, region, and workspace permit. |
| Pro $500 plan | https://learn.chatgpt.com/docs/pricing | Current plan/feature availability; verify before recommending paid capability. |
| Ultrafast — build guide | https://developers.openai.com/api/docs/guides/ultrafast-mode | Low-latency Astra API/Codex workflows where access and economics justify it. |
| GPT-6.1 Sol — Learn more | https://developers.openai.com/api/docs/models/gpt-6.1-sol | Near-Astra performance at lower cost for complex coding/professional work. |
| ChatGPT Space — Explore Space | https://learn.chatgpt.com/docs/space | Shared Pages/files/team knowledge and collaboration. |
| ChatGPT logo | https://chatgpt.com/ | Product home; no delivery-method rule. |
| Privacy | https://openai.com/policies/row-privacy-policy/ | Privacy baseline. |
| Terms | https://openai.com/policies/row-terms-of-use/ | Consumer Terms of Use baseline. |

**Administrative link intentionally not opened:** the email's Unsubscribe link can change subscription state. It is not a methodology source.

### DevDay notes that require current-doc reconciliation

- The email says work can be tracked in /agents. Current Codex documentation uses /agent or /subagents to inspect/switch spawned agent threads. Use the current command reference rather than newsletter shorthand.
- Dots, Ultrafast, GPT-6.1 Sol, Space, and other rollout-sensitive capabilities must be rechecked before a project assumes availability.
- A newsletter announcement is discovery evidence, not the final operating instruction. Follow the linked current documentation for implementation.
