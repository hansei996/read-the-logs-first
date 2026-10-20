# Awesome-list placement pack

Target repo: **https://github.com/hansei996/read-the-logs-first**
Research date: **2026-10-20** (all stars / last-commit dates read on that date; line numbers drift — re-anchor with the `grep` shown per entry before opening anything).

Discovery method: GitHub search API (`/search/repositories`, 8 queries, 7 s apart) + per-repo `commits.atom` for last-commit dates + `raw.githubusercontent.com/<repo>/HEAD/README.md` and `/CONTRIBUTING.md` for the rules quoted below. Nothing here is from memory.

## Status board

| # | List | Stars | Last commit | Accepts | Verdict |
|---|------|-------|-------------|---------|---------|
| 1 | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 77,491 | 2026-07-24 | PR | **Submit first** |
| 2 | [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | 56,082 | 2026-10-20 | issue form only | Wait to 2026-11-03 (14-day rule) |
| 3 | [github/awesome-copilot](https://github.com/github/awesome-copilot) | 40,224 | 2026-10-19 | PR (vendored folder) | Later — needs vendoring |
| 4 | [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 36,053 | 2026-10-19 | PR | Blocked by "no brand-new skills" |
| 5 | [e2b-dev/awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents) | 30,537 | 2026-08-21 | PR / form | Skip — agents, not skills |
| 6 | [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | 15,479 | 2026-04-28 | PR | Submit second (social proof wanted) |
| 7 | [BehiSecc/awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills) | 10,277 | 2026-09-21 | PR | **Submit first** (no star gate) |
| 8 | [heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills) | 6,294 | 2026-10-15 | PR (auto-checked) | Blocked — needs 20★ |
| 9 | [Prat011/awesome-llm-skills](https://github.com/Prat011/awesome-llm-skills) | 1,809 | 2026-07-14 | PR | Submit third |
| 10 | [bradAGI/awesome-cli-coding-agents](https://github.com/bradAGI/awesome-cli-coding-agents) | 1,383 | 2026-10-19 | PR | Skip — agents/harnesses only |

All ten are active (every last commit is inside the last 12 months), so none is excluded on the activity rule. The gate that actually bites is the "brand-new / no social proof" rule on #4 and the 100★-or-14-day rule on #2.

---

## 1. ComposioHQ/awesome-claude-skills — 77,491★ — last commit 2026-07-24

Rule (CONTRIBUTING.md, "Skill Requirements"):
> "All skills must: 1. **Solve a real problem** - Based on actual usage, not theoretical applications."

Rule (CONTRIBUTING.md, "Adding Your Skill to README"):
> "- [Skill Name](./skill-name/) - One-sentence description. Inspired by [Person/Source]." followed by "3. Follow the existing format exactly - no emojis, consistent punctuation."

Where: section **`### Development & Code Tools`** (README L118 in the 2026-10-20 snapshot, right after `## Skills`). Entries are case-insensitive alphabetical, so it lands in the R's — find the boundary with:

```bash
grep -n '^- \[' README.md | sed -n '/Development & Code Tools/,/^[0-9]*:- \[S/p'
```

Paste this line:

```markdown
- [read-the-logs-first](https://github.com/hansei996/read-the-logs-first) - Forces the agent to quote the failing line and open the failing frame before it proposes a fix.
```

PR title: `Add read-the-logs-first skill`. Note their guideline "Follow the existing format exactly" — the external-repo link form (not `./skill-name/`) is already used in that section, e.g. `- [aws-skills](https://github.com/zxkane/aws-skills) - ...`, so linking out is legal here.

---

## 2. hesreallyhim/awesome-claude-code — 56,082★ — last commit 2026-10-20

Rule (CONTRIBUTING.md, "GROUND RULES"):
> "Any resource that is recommended must either: (i) Be at least 14 days old (14 days since first commit on default branch) AND show signs of active development ... OR (ii) Have at least 100 stars."

Rule (CONTRIBUTING.md, "How to Recommend a Resource"):
> "**NOTE: ALL RECOMMENDATIONS MUST BE MADE USING THE WEB UI ISSUE FORM TEMPLATE, OR YOU RISK BEING RESTRICTED FROM INTERACTING WITH THIS REPOSITORY TEMP[orarily]**" — and "Do not open a PR. Just fill out the form."

**This one is not a PR at all.** PRs are actively discouraged and issue-form submissions via `gh` are explicitly impossible ("It is **not** possible to submit a resource recommendation using the `gh` CLI."). A human must fill in https://github.com/hesreallyhim/awesome-claude-code/issues/new?template=recommend-resource.yml

Where: section **`## Skills`** (README L621). Entries there are multi-line blocks with two `shields.io` badge images — **do not hand-write that markdown.** Their bot generates it from the form.

What you paste: form fields only.

```text
Name: read-the-logs-first
URL: https://github.com/hansei996/read-the-logs-first
Description: A skill that makes the agent read the full error, quote the failing line, and open the failing frame before it edits code. Ten rules; no fix is proposed without a trace line.
```

Their style rule applies to that description: "Resource descriptions should be written as _descriptions_ - not a sales pitch. Don't address the reader." Keep it flat, as written above.

**Timing:** the repo has one commit dated today, so branch (i) fails until **2026-11-03**. Re-submit after that date with at least a couple of later commits so "signs of active development" holds. Branch (ii) (100★) is unrealistic short-term. Optional perk once accepted: the "Mentioned in Awesome Claude Code" badge is pre-written in their CONTRIBUTING.md.

---

## 3. github/awesome-copilot — 40,224★ — last commit 2026-10-19

Rule (CONTRIBUTING.md, "What We Accept"):
> "We welcome contributions covering any technology, framework, or development practice that helps developers work more effectively with GitHub Copilot." — list includes "Development methodologies and best practices".

Rule (CONTRIBUTING.md, "Adding Skills"):
> "Skills are self-contained folders in the `skills/` directory that include a `SKILL.md` file (with front matter) and optional bundled assets." — "1. **Create a new skill folder**: Run `npm run skill:create -- --name <skill-name> --description \"<skill description>\"`" ... "4. **Validate and update docs**: Run `npm run skill:validate` and then `npm run build` to update the generated README tables"

Where: there is **no README line to edit.** You add `skills/read-the-logs-first/SKILL.md` to their repo; the tables are generated by `npm run build` into `docs/README.skills.md`. So the "insertion position" is a vendored folder, and their repo becomes a second home for the skill.

What you paste — the folder name and the front-matter description:

```text
folder: skills/read-the-logs-first/
front-matter description: Force the agent to read the full error, log, or stack trace and open the failing frame before editing code.
```

Cost: vendoring + `npm run skill:validate` + `npm run build` with Node. Deferred until the other lists land.

---

## 4. VoltAgent/awesome-agent-skills — 36,053★ — last commit 2026-10-19

Rule (CONTRIBUTING.md, "Entry Format"):
> "- **[author/skill-name](https://github.com/author/repo/path)** - Short description of what it does"

Rule (CONTRIBUTING.md, "Requirements"):
> "Skill must have real community usage. We focus on community-adopted, proven skills. Brand new skills that were just created are not accepted. Give your skill time to mature and gain users before submitting."

Also: "Description must be short, 10 words or fewer." and PR title `Add skill: author/skill-name`.

Where: **Community Skills → "Development and Testing"** `<details>` block (README L1595 opens it; append as the last `- **[...]**` line before that block's `</details>`). Line 1877 reinforces the gate: "Please don't submit skills you created 3 hours ago."

Paste this line (10 words of description, exactly at their limit):

```markdown
- **[hansei996/read-the-logs-first](https://github.com/hansei996/read-the-logs-first)** - Read the error and the failing frame before editing code
```

**Verdict: do not open this PR today.** With 0★ and a 1-day-old repo it violates the stated rule and burns the one clean first impression at 36k★. Queue it behind a few days of real usage.

---

## 5. e2b-dev/awesome-ai-agents — 30,537★ — last commit 2026-08-21

Rule (README, "Have anything to add?"):
> "Create a pull request or fill in this [form](https://forms.gle/UXQFCogLYrPFvfoUA). Please keep the alphabetical order and in the correct category."

Where: entries are heavyweight per-project H2 blocks (`## [Name](url)` then `### Category`, `### Description`, `### Links` — e.g. README L73, L80, L83, L92).

**Verdict: skip.** The list is about autonomous *agents and apps*, not skills or rules; our SKILL.md is not a product in their taxonomy, and the block format asks for Category/Features/Stack metadata we do not have. An entry would read as off-topic.

---

## 6. travisvn/awesome-claude-skills — 15,479★ — last commit 2026-04-28

Rule (CONTRIBUTING.md, note at the top):
> "Given the growth in assisted skill development, a new requirement of \"social proof\" has been added to skill submissions."

Rule (CONTRIBUTING.md, "Formatting"):
> "- **[Name](link)** - Clear, concise description of what it does"

Where: **`### Individual Skills`** table (README L113–L130), one row. The table is not alphabetical — newest rows are appended at the bottom, right before `_More community skills coming soon! Submit a PR to add your skill._`

Paste this row:

```markdown
| **[read-the-logs-first](https://github.com/hansei996/read-the-logs-first)** | Debugging discipline: quote the failing line and open the failing frame before editing |
```

**Verdict: submit, but second wave** — the "social proof" requirement is new and undefined in the file ("a new requirement of social proof"), so it will likely be judged on stars/usage. Land the no-gate lists first, then come back.

---

## 7. BehiSecc/awesome-claude-skills — 10,277★ — last commit 2026-09-21

Rule (README, "## 🤝 Contribution"):
> "If you have suggestions, improvements, or new resources to add: 1. Fork this repo 2. Make your changes 3. Submit a Pull Request"

Where: **`## 🛠 Development & Code Tools`** (README L42; entries run L43+ with no blank lines between them). No stated star minimum, no social-proof clause — this is the lowest-friction entry in the set. Append at the end of that section, immediately before the next `## ` heading.

Paste this line:

```markdown
- [read-the-logs-first](https://github.com/hansei996/read-the-logs-first) - Forces the agent to quote the failing line and open the failing frame before it edits code.
```

Matches the house style exactly: `- [name](url) - Sentence with a full stop.`

---

## 8. heilcheng/awesome-agent-skills — 6,294★ — last commit 2026-10-15

Rule (CONTRIBUTING.md, "How Can You Contribute?"):
> "In short: a public GitHub repo with a `SKILL.md`, at least 20 stars, older than 14 days, not already listed, one line appended to an existing category in `README.md`, nothing else changed."

Rule (CONTRIBUTING.md, "The PR Process"):
> "An automated check comments on every PR; fix what it reports in the same PR."

Where: **Community Skills → "Development and Testing"** (that subheading sits under `## Community Skills`, README L503). Append one line at the end of the matching category.

Paste this line (their stated cap: "Description under 100 characters"):

```markdown
- [hansei996/read-the-logs-first](https://github.com/hansei996/read-the-logs-first) - Makes the agent read the error and the failing frame before it edits code.
```

**Verdict: blocked until 20★ and 14 days.** Two hard numeric gates, auto-checked. Calendar date: **2026-11-03** is the earliest possible.

---

## 9. Prat011/awesome-llm-skills — 1,809★ — last commit 2026-07-14

Rule (CONTRIBUTING.md, "Skill Requirements"):
> "5. **Be tested** - Verify the skill works across Claude Code, Codex, Gemini CLI."

Rule (CONTRIBUTING.md, "Adding Your Skill to README"):
> "- [Skill Name](./skill-name/) - One-sentence description. Inspired by [Person/Source]." followed by "2. Add your skill in alphabetical order within the category"

Where: **`### Development & Code Tools`** (README L130 under `## Skills`), alphabetical, so it lands among the R's. External links are already used in that section (L132 links `anthropics/skills` directly).

Paste this line:

```markdown
- [read-the-logs-first](https://github.com/hansei996/read-the-logs-first) - Forces the agent to quote the failing line and open the failing frame before it proposes a fix.
```

Note their "Be tested across Claude Code, Codex, Gemini CLI" bar — our README already claims all three, which is what this PR will be checked against.

---

## 10. bradAGI/awesome-cli-coding-agents — 1,383★ — last commit 2026-10-19

Rule (README, "## Contributing", L1020) — the list documents its own sort order at L720:
> "Sandboxes, routers, browser/terminal automation, and extension tools. Sorted by GitHub stars."

Entry format (L722): `- **[Headroom](https://github.com/headroomlabs-ai/headroom)** `⭐ 76.1k` — Context-compression layer for coding agents`

**Verdict: skip.** Every section is sorted by stars, so a 0★ entry would sit dead last; more importantly the list is about terminal-native *agents, harnesses and infrastructure*, not rules a skill imposes on an agent. Off-taxonomy.

---

## Execution order (when the lead green-lights PRs)

1. **#7 BehiSecc** — no gates, has an explicit PR path. Lowest rejection risk, real backlink.
2. **#1 ComposioHQ** — big audience, plain PR, format is one line.
3. **#9 Prat011** — small but zero-friction once "tested across" is true.
4. **#6 travisvn** — after some stars accumulate, because of the new social-proof bar.
5. **#2 hesreallyhim + #8 heilcheng** — both open on **2026-11-03** (14-day rules); #2 is a form, not a PR.
6. **#4 VoltAgent** — only once there is visible community usage.
7. **#3 github/awesome-copilot** — vendoring work, do last.

Rules to respect in every submission: **one resource per PR** (hesreallyhim states it explicitly, and it is the safe assumption everywhere), never reformat untouched lines, and never submit the same repo to two lists from the same day-old account in a burst — that pattern reads as spam.
