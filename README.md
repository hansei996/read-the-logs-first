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

Manual (always works — the marketplace command depends on your Claude Code version): copy `skills/read-the-logs-first/SKILL.md` into your agent's skills directory.

## What it does

Stops the agent from proposing a fix before it has read the failure — quote the line, open the frame, name the cause, then change one thing and re-run the command.

## A real session, end to end

The old `Before` column here was a reconstruction, so it is gone. What follows is one
actual session against a real bug: [`examples/orders-demo`](./examples/orders-demo),
a small order-total CLI. Every line is reproducible, and the full transcript —
commands, exit codes, probes, diff — is in
[`examples/session-log.md`](./examples/session-log.md).

<table>
<tr><td width="50%">

**What the terminal printed**

Stdout was empty. Exit code 1. This is the whole of stderr, unedited:

</td><td width="50%">

**What the fix was based on**

The frame that threw, then the evidence that named the cause — not a hypothesis
about dependencies, versions, or architecture.

</td></tr>
</table>

```console
> node src/index.js

C:\Users\13553\Downloads\DSH_workspace\read-the-logs-first\examples\orders-demo\src\rates.js:16
  const rate = rates[currency];
                    ^

TypeError: Cannot read properties of null (reading 'USD')
    at convert (C:\Users\13553\Downloads\DSH_workspace\read-the-logs-first\examples\orders-demo\src\rates.js:16:21)
    at C:\Users\13553\Downloads\DSH_workspace\read-the-logs-first\examples\orders-demo\src\order.js:5:18
    at Array.reduce (<anonymous>)
    at totalUsdCents (C:\Users\13553\Downloads\DSH_workspace\read-the-logs-first\examples\orders-demo\src\order.js:4:22)
    at Object.<anonymous> (C:\Users\13553\Downloads\DSH_workspace\read-the-logs-first\examples\orders-demo\src\index.js:15:15)
    at Module._compile (node:internal/modules/cjs/loader:1830:14)
    at Object..js (node:internal/modules/cjs/loader:1961:10)
    at Module.load (node:internal/modules/cjs/loader:1553:32)
    at Module._load (node:internal/modules/cjs/loader:1355:12)
    at wrapModuleLoad (node:internal/modules/cjs/loader:255:19)

Node.js v24.15.0
```

**1. Quote it, then open the frame.** Column 21 of `src/rates.js:16` is the `[` in
`rates[currency]` — so `rates` itself is `null` when `convert()` runs.

**2. Read the callers in trace order.** `index.js:15` → `totalUsdCents` →
`convert`, and not one `await` between them. The whole chain is synchronous.

**3. Instrument, because the file alone cannot answer "when".** A probe prints the
order of events (`probes/order-vs-data.js`):

```console
> node probes\order-vs-data.js

A: before require
B: require returned
C: convert threw: Cannot read properties of null (reading 'USD')
```

A second probe calls the same function 50 ms later, after the load promise settles
(`probes/late-call.js`):

```console
> node probes\late-call.js

D: 50ms later, convert(100, 'USD') = 100
```

`100 * 1.0 = 100`. The file reads, the JSON parses, the math is right. Only the
ordering is wrong — which kills "the rates table must be corrupt".

**4. Name the cause, change one thing.** `loadRates()` is `async` and line 13 calls
it bare, so the promise is discarded and `rates` is still `null` on the first call.
`convert()` is synchronous and runs inside an `Array.reduce`, so the load has to be
synchronous too:

```diff
-async function loadRates() {
-  const raw = await fs.readFile(RATES_FILE, 'utf8');
+function loadRates() {
+  const raw = fs.readFileSync(RATES_FILE, 'utf8');
```

**5. Re-run the exact command, paste the output.** Exit code 0:

```console
> node src/index.js

A-1001	3580 USD-cents
A-1002	4000 USD-cents
A-1003	3258 USD-cents
```

`2500 + 1080 = 3580`, `4000`, `2286 + 972 = 3258` — matches the arithmetic against
`data/rates.json` by hand. One file changed. Nothing else touched.

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
