---
name: read-the-logs-first
description: Use when debugging a failure, a broken test or CI run, or when the user pastes a traceback. Gives the agent two things it would otherwise guess at - a deterministic way to pick the failing frame out of a traceback, and where each runtime actually writes its logs - then rules for changing one thing at a time.
license: MIT
---

# Read the logs first

Do not edit code until you have the failing frame in front of you, chosen by evidence rather than guessed from the first line of the exception.

## Pick the frame by rule, not by eye

A traceback lists every frame; only some belong to the code you are allowed to change. Apply this rule:

- **Python** tracebacks print outermost-first, so the innermost *user* frame is the **last** one.
- **Node / V8** stacks print innermost-first, so it is the **first** one.
- Skip frames under `site-packages`, `dist-packages`, `node_modules`, `node:internal`, `node:internal`, and the stdlib (`/lib/python*`).

A ten-line extractor that encodes exactly this is bundled at `tools/extract_frame.py` (stdin in, `file:line` + source line out, exit 2 instead of guessing). If the tool is not in the checkout, the rule above is the whole algorithm — apply it by hand.

## Where the logs actually are

Most "I cannot see the error" cases are a wrong location, not a missing log.

| Runtime | Where to look |
|---|---|
| pytest | `-l -vv` keeps locals; `--tb=long`; output goes to the terminal unless captured (`-s` disables capture) |
| Python logging | `basicConfig()` writes to **stderr**, not stdout |
| Node / V8 | stderr; the frame is the first `at ...` line inside your repo |
| Docker | `docker logs <c>` (stdout+stderr); `docker inspect` shows exit 137 for OOM |
| systemd | `journalctl -u <svc> -n 200 --no-pager` |
| GitHub Actions | the **step log**, not the annotation — annotations truncate at the first error |
| nginx / apache | `error.log`, never `access.log`; a status code alone never carries the reason |

## Rules

1. **Read the whole trace**, not the first line of the exception.
2. **Name the frame by the rule above**, and quote its `file:line` and source line verbatim in your reply.
3. **Open that frame before editing.** If there is no user frame, say so and stop instead of guessing.
4. **Separate error from symptom:** name the frame that raised *and* the call site that supplied the bad value.
5. **Every hypothesis carries a line reference:** `X fails because Y (file:line)`. No line = it is a guess, label it.
6. **Check the location before concluding the log is missing** — use the table above.
7. **One change at a time**: the smallest edit that can falsify the hypothesis. No drive-by refactors during a hunt.
8. **Re-run the exact reproducing command** and paste the output. "Should work now" is not a result.
9. **Truncated logs: ask for the missing part precisely** (`frames 4-8`, `the 20 lines before the crash`). Never fill gaps with guesses.
10. **Two failed fixes: stop guessing.** Propose one instrumentation step (one log line, one minimal repro) and say what it distinguishes.

## Output shape

```
Failure: <verbatim line>
Frame:   <file:line>  (<source line>)
Cause:   <what was wrong there> (evidence: <trace line / code line>)
Fix:     <smallest change>
Verify:  <command> -> <actual output>
```
