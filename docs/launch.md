# Launch copy

Repo: https://github.com/hansei996/read-the-logs-first
All copy below is ready to post. Nothing here contains a number we cannot point at: no user counts, no download counts, no benchmark claims. The README's Before/After block is explicitly labelled *illustrative, reconstructed* and is **not** quoted anywhere in this file — do not paste it into a launch post until it is replaced with a real transcript.

Voice note: the whole pitch is one sentence — *the agent reads the failure before it edits*. Every channel below keeps that as the first claim and adds no feature that does not exist.

---

## 1. Show HN

### Title — primary (74 chars, cap 80)
```text
Show HN: read-the-logs-first – make your coding agent read the error first
```

### Title — backup (72 chars)
```text
Show HN: A skill that forces coding agents to read the stack trace first
```

### Body

```text
I got tired of watching coding agents answer a stack trace with "this is probably a dependency issue" and a three-file refactor. The failure had a line number in it and the agent never opened it.

read-the-logs-first is a SKILL.md that any agent reading AGENTS.md or a skills directory can pick up. It imposes an order on debugging: quote the failure verbatim, open the failing frame, name the cause with evidence, then make one change and re-run the exact command.

The ten rules, abbreviated:
1. Read the whole error, not the first line.
2. Quote the failure verbatim in the reply.
3. Open the frame at file:line before editing.
4. Separate error from symptom.
5. Every hypothesis carries a trace line: "X fails because Y (trace line N)".
6. One change at a time.
7. Re-run the exact reproducing command and paste the output.
8. Logs truncated or missing? Ask for the exact lines instead of guessing.
9. No speculative tooling.
10. Two failed fixes = stop, add one instrument, say what it distinguishes between.

It also fixes the output shape (Failure / Frame / Cause / Fix / Verify) so a reply is checkable instead of persuasive.

What it is not: a debugger, an MCP server, or a model. It is a text file of rules plus install instructions, MIT, and it works with Claude Code, Codex, Cursor, Gemini CLI and anything else that reads a SKILL.md. Rules 2 and 3 are the load-bearing ones — the README says so, so people can trim the rest.

Install is one line, pasted into the agent:

  Install the read-the-logs-first skill from https://github.com/hansei996/read-the-logs-first — follow AGENTS.md.

What I actually want from you: rule 8 asks the agent to stop and request the missing lines. In my use it fixed the guessing, but I keep wondering whether it makes the agent too chatty in setups where the log is already in context. Rule 10 has the same tradeoff. Tell me which rule you would delete first.
```

Notes: HN frowns on "Show HN" posts that read as marketing — the last paragraph is the discussion hook, keep it. Do not add "upvotes appreciated".

---

## 2. Reddit — r/ClaudeAI

### Title — primary
```text
My agent "fixed" bugs it had never read, so I wrote 10 rules it has to follow first
```

### Title — backup
```text
A skill that makes Claude read the stack trace before it touches your code
```

### Body

```text
The pattern I kept hitting: something throws, I paste the traceback, and the reply starts with "this is probably a dependency mismatch" and ends with four files changed. The traceback has a file and a line number in it. The agent never opened that line.

Being helpful is what the model is trained to do, and "produce a fix fast" is what helpful looks like. So the fix gets aimed at whatever is cheapest to change, not at the frame that threw.

So I wrote the rules down as a skill instead of arguing with the model every time.

What it actually changes:
- it has to paste the failing line verbatim before proposing anything
- it has to open the frame at file:line and say what value was wrong there
- one change at a time, smallest edit that could falsify the hypothesis
- re-run the exact same command afterwards and paste the output, no "this should work now"
- if the log is truncated, it asks for the specific missing lines instead of inferring them
- two failed fixes and it stops guessing and proposes one piece of instrumentation

There are 10 rules and an output template (Failure / Frame / Cause / Fix / Verify). It is a plain SKILL.md — no MCP server, no API key, no debugger. It works in Claude Code, and also in Codex / Cursor / Gemini CLI, since it is just instructions.

Install, pick one:

Claude Code plugin:
  claude plugin marketplace add hansei996/read-the-logs-first
  claude plugin install read-the-logs-first@read-the-logs-first

Or paste this into the agent:
  Install the read-the-logs-first skill from https://github.com/hansei996/read-the-logs-first — follow AGENTS.md.

Repo: https://github.com/hansei996/read-the-logs-first (MIT)

Two things I am unsure about and would like opinions on:
1. Rule 8 makes it ask for missing logs instead of guessing. Good for my workflow, possibly annoying if you already have the full log in context. Did you loosen it or keep it?
2. Rule 10 is a hard stop after two failed fixes. Some agents take that as permission to stop working. Too strict?

If you try it, the honest test is one real bug where you already have a traceback — you will see immediately whether the reply opens the frame or jumps to a theory.
```

Notes: keep it in first person, no bold headers and no emoji — r/ClaudeAI downvotes anything that looks like a landing page. Keep the install lines as code, not as a screenshot.

---

## 3. X / Twitter (limit 280)

### Post — primary
```text
Your agent answers a stack trace with "this is probably a dependency issue" and a three-file refactor.

read-the-logs-first makes it quote the failing line and open the failing frame before editing.

Ten rules, one SKILL.md, MIT.
https://github.com/hansei996/read-the-logs-first
```

### Post — backup
```text
A debugging rule I now enforce on my agent: no fix until it has quoted the failing line and opened that frame.

Wrote it up as a 10-rule skill (SKILL.md, MIT, works in Claude Code / Codex / Cursor / Gemini CLI):
https://github.com/hansei996/read-the-logs-first
```

Notes: both fit in one tweet; do not attach the README table as an image (that is the illustrative transcript). If you want a thread, reply 2 = the ten rules as a plain list, reply 3 = the output shape.

---

## 4. 中文 — 掘金 / V2EX 通用版（200 字内）

### 标题 — 主选
```text
让 AI 先读日志再改代码：给编码 Agent 的 10 条调试铁律
```

### 标题 — 备选
```text
你的 Agent 在读报错之前就开始动手了
```

### 正文

```text
Agent 看到报错先说“可能是版本问题”，然后大改三个文件让你再试。可报错里带着行号，它一次都没打开过。

read-the-logs-first 是一个 SKILL.md：先逐字引用报错、打开出错的那一帧、用证据说因果，再只改一处、重跑原命令。10 条规则，MIT，各主流 CLI 通用。

https://github.com/hansei996/read-the-logs-first
```

Notes: 正文 196 字符（含裸 URL；中文 83 字），未超过 200 字上限。规则 2/3 的强调保留在正文里，其余规则按需删。V2EX 版把第一段换成“分享创造”风格即可，标题用备选。不要写「已有 N 人使用」这类数字。

---

## Pre-flight checklist before anything is posted

- [ ] README still says *(illustrative transcripts, reconstructed — not screen recordings)* — do not quote that block in any post until it is replaced with a real run.
- [ ] ```claude plugin marketplace add hansei996/read-the-logs-first``` actually resolves (the marketplace manifest must be live, otherwise drop that install block from the Reddit post).
- [ ] Every install line copied from the README, not retyped.
- [ ] No post claims a user count, star count, or time saving.
- [ ] Post one channel per day, and answer the first three comments before posting the next one — a launch that cannot answer comments is wasted.
