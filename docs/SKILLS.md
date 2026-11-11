# Skills inventory (Phase 0, CLAUDE.md §10.1)

Taken from the skill listing of the session on 2026-11-11. Skills are loaded only when their phase starts.

## Used in this project

| Skill | What it does | Phase | Decision |
|---|---|---|---|
| `mattpocock-skills:grilling` | Interviews the user one question at a time to settle open decisions | 0 (D1–D7) | use |
| `mattpocock-skills:domain-modeling` | Keeps a shared glossary of domain terms | 0→all (`CONTEXT.md`) | use |
| `mattpocock-skills:tdd` / `superpowers:test-driven-development` | Failing test first, then code | 1, 2a (ingest, normaliser, re-join checker, coverage checker) | use (`superpowers:` version; same discipline) |
| `superpowers:systematic-debugging` / `mattpocock-skills:diagnosing-bugs` | Root-cause debugging, no guess-and-patch | any | use when a check fails unexpectedly |
| `superpowers:verification-before-completion` | No "done" claim without the command output | every gate | use |
| `code-review` (built-in) / `mattpocock-skills:code-review` | Reviews a diff for correctness | 1, 2a, every script change before commit | use |
| `review-council` agents (`correctness-reviewer`, `test-evidence-reviewer`, …) | Multi-reviewer review | 2a (re-join checker, crosswalk) | use |
| `product-management:write-spec` | Turns a phase into a written spec | 1, 2a, 3 | use for Phase 3 spec; Phases 1–2a are specified enough by CLAUDE.md |
| `superpowers:writing-plans` / `superpowers:executing-plans` | Plan file + tracked execution | 1–3 | use (tickets live in `progress/state.json` + plan files; no external tracker) |
| `agentic-council:handover` / `agent-handoff:*` | Session handoff notes | session ends | use, writing to `progress/HANDOFF.md` |
| `superpowers:dispatching-parallel-agents`, `superpowers:subagent-driven-development` | Generator / reviewer sub-agents | 3 (Stage C) | use then (content generation and review, §10.3) |
| `anthropic-skills:skill-creator` | Packages a project skill | after pilot | use to make `ramayana-content-review` |
| `coding-skills:unicode-pitfalls` | NFC, combining marks, grapheme pitfalls | 1 (normaliser) | use |
| `mattpocock-skills:wizard` | One-time repo setup (tracker, labels, domain docs) | 0 | **skip for now**: no GitHub remote yet (D6), so no issue tracker to configure; rerun once the repo exists |
| `website-design:review-page`, `design:accessibility-review` | Page review / a11y | 1 (site check) | use lightly; the design is fixed (no redesign) |
| `run` (built-in) | Launch and drive the site | 1 | use for preview verification |

## Not used (grouped by plugin)

| Plugin / skills | Reason to skip |
|---|---|
| `research-superpowers:*` | Academic literature/wiki workflow; this is a text-edition build |
| `agentic-council:*` personas (finance, people, revenue councils, crypto, embedded, …) | Off-domain; the review-council agents cover code review |
| `hzblj-skills:*` | React / Next.js / React Native / monorepo conventions; the site is vanilla JS by rule (§1) |
| `datarobot-*`, `huggingface-skills:*`, `clickhouse`, `atlan`, `data:*`, `informatica-*` | ML / data-platform tooling not used here (Dharmamitra is called as a Python package) |
| `figma:*`, `design-superpowers:*`, `website-design:landing-page`, `8b-ai-website-builder:site`, `artifact-*` | Would redesign or host elsewhere; §1 forbids redesign |
| `finance-*`, `doubleverify:*`, `product-management:*` (except write-spec), `productivity:*` | Off-domain |
| `writing-skills:*`, `humanizer` | English prose styles; content here is Sanskrit with fixed rules (§5) |
| `microsoft-docs:*`, `unreal-engine-*`, `nvidia-skills:*`, `pdf-viewer:*`, `miro:*` | Off-domain |
| `coding-skills:*` (other than unicode-pitfalls) | Database / distributed-systems topics not present |
| `arena`, `research-desk:*`, `learn*`, `ai-mentor` | Not needed; may use `arena` later for disputed padaccheda only if the user asks |
| `loop`, `schedule`, `update-config`, `keybindings-help`, `fewer-permission-prompts` | Harness configuration, not project work |
