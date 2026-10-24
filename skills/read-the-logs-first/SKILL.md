---
name: read-the-logs-first
description: Use when debugging a failure, a broken test or CI run, or when the user pastes a traceback. Gives the agent the two things it would otherwise guess at - a deterministic failing-frame extractor and a table of where each runtime actually writes its logs - then the rules for changing one thing at a time.
license: MIT
---

# Read the logs first

Do not edit code until you have the failing frame in front of you, taken from evidence rather than guessed from the first line of the exception.

## Step 0 - extract the frame, do not eyeball it

```bash
pytest 2>&1 | python tools/extract_frame.py
```

It prints `file:line` plus the source line of the **innermost frame that belongs to user code** (Python: last user frame; Node: first user frame; stdlib, `site-packages`, `node_modules` and `node:internal` are skipped). If it exits 2, there was no user frame - say so and stop instead of guessing.

## Where the logs actually are

Most "I cannot see the error" cases are a wrong log location, not a missing log.

| Runtime | Where to look |
|---|---|
| pytest | `-l -vv` keeps the locals; `--tb=long`; full output is in the terminal, not in a file |
| Python logging | `logging.basicConfig()` writes to **stderr**; `pytest -s` to stop capture |
| Node / V8 | stderr, not stdout; the frame is the first `at ...` line inside your repo |
| Docker | `docker logs <c>` is the container stdout+stderr; `docker inspect` for OOM exit 137 |
| systemd | `journalctl -u <svc> -n 200 --no-pager` |
| GitHub Actions | the step log, not the annotation; annotations truncate at the first error |
| nginx / apache | `error.log` (not `access.log`); the status code alone never contains the reason |

## Rules

1. **Run the extractor, then read the whole trace** - not the first line of the exception.
2. **Quote the extracted `file:line` and its source line verbatim** in your reply. No paraphrase.
3. **Open that frame before editing.** If the extractor found no user frame, say so and stop.
4. **Separate error from symptom.** Name the frame that raised *and* the call site that supplied the bad value.
5. **Every hypothesis carries evidence:** `X fails because Y (file:line)`. No line = it is a guess, label it.
6. **Check the log location before concluding the log is missing** - use the table above.
7. **One change at a time.** Smallest edit that can falsify the hypothesis. No drive-by refactors while hunting a bug.
8. **Re-run the exact reproducing command** and paste the output. "Should work now" is not a result.
9. **Truncated logs: ask for the exact missing part** (`frames 4-8`, `the 20 lines before the crash`). Do not fill gaps with guesses.
10. **Two failed fixes: stop guessing.** Propose one instrumentation step (one log line, one minimal repro) and say what it distinguishes.

## Output shape

```
Failure: <verbatim line>
Frame:   <file:line>  (<source line>)
Cause:   <what was wrong there> (evidence: <trace line / code line>)
Fix:     <smallest change>
Verify:  <command> -> <actual output>
```

## Anti-patterns this kills

- "It might be a version mismatch - try upgrading X."
- "The log is missing" (when it went to stderr, or to the step log, or to journalctl).
- Editing three files, then asking whether it works now.
