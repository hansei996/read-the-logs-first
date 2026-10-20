# read-the-logs-first

> **It reads the stack trace before it touches your code.**

A skill for any coding agent. Kills guess-and-check debugging: no fix gets proposed until the agent has quoted the exact failing line, opened the failing frame, and named the cause.

Works with Claude Code, Codex, Cursor, Gemini CLI, DeepSeek Harness — any agent that loads a `SKILL.md` / `AGENTS.md`.

## Install

Paste this into your agent:

```text
Install the read-the-logs-first skill from https://github.com/hansei996/read-the-logs-first — follow AGENTS.md.
```

Claude Code plugin style:

```bash
claude plugin marketplace add hansei996/read-the-logs-first
claude plugin install read-the-logs-first@read-the-logs-first
```

Manual: copy `skills/read-the-logs-first/SKILL.md` into your agent's skills directory.

## What it does

Stops the agent from proposing a fix before it has read the failure — quote the line, open the frame, name the cause, then change one thing and re-run the command.

## Before / after

*(illustrative transcripts, reconstructed — not screen recordings)*

<table>
<tr><td width="50%">

**Before**

> This is probably a dependency issue. Your `jsonwebtoken` version may be outdated, and the middleware looks fragile too. Let me refactor the auth flow: I've updated `package.json`, rewritten `verifyToken`, and adjusted `src/middleware.ts`. Try running it again and let me know if the error persists. Hope this helps!

</td><td width="50%">

**After**

> `TypeError: Cannot read properties of undefined (reading 'sub')` — `src/auth.ts:47:22`
>
> Frame at `src/auth.ts:47`: `jwt.verify(token, SECRET).sub` returns undefined because `SECRET` is `undefined` in this process — `process.env.JWT_SECRET` is never loaded here (no dotenv import in `src/index.ts`).
>
> 1. Add `import 'dotenv/config'` as the first line of `src/index.ts`
> 2. Re-run `npm run dev`
>
> Verify: `curl -s -X POST localhost:3000/login -d '{"user":"a"}'` → expect `{"token":"..."}`, not a 500.

</td></tr>
</table>

## The rules

10 rules, full text in [SKILL.md](./skills/read-the-logs-first/SKILL.md).

1. Read the whole error, not the first line.
2. Quote the failure verbatim.
3. Open the failing frame before editing.
4. Separate error from symptom.
5. Every hypothesis carries a trace line.
6. One change at a time.
7. Re-run the exact command, paste the output.
8. Logs missing? Ask for the exact lines, don't guess.
9. No speculative tooling.
10. Two failed fixes = stop guessing, instrument instead.

## Tune it

Fork it and edit `skills/read-the-logs-first/SKILL.md`. Rule 8 and rule 10 are the two most people loosen (some agents ask too eagerly); rules 2 and 3 are the load-bearing ones — drop them and the skill stops working.

## Why this exists

Agents are trained to be helpful, and helpfulness reads as "produce a fix fast". Fast is the enemy: the cheapest fix is the one aimed at the line that actually threw. This skill buys one extra read before the first edit.

## License

MIT