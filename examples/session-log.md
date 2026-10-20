# Session log — one real debug session, verbatim

Captured on Windows, Node `v24.15.0`. Every console block below is the actual
output of the command above it, copied out of the terminal. Nothing is retyped,
reordered, or reconstructed.

`>` marks the command I typed. Everything after that line is untouched program
output. Exit codes are recorded as the shell reported them.

Reproduce everything here:

```console
$ cd examples/orders-demo
```

---

## 1. The command that failed

I was asked to make this little orders CLI total each order in USD cents.

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

stdout was empty. Exit code: **1**. The whole thing above went to stderr.

## 2. Open the failing frame before touching anything

The trace points at `src/rates.js:16`. Line 16, column 21:

```console
> type src\rates.js

const fs = require('node:fs/promises');
const path = require('node:path');

const RATES_FILE = path.join(__dirname, '..', 'data', 'rates.json');

let rates = null;

async function loadRates() {
  const raw = await fs.readFile(RATES_FILE, 'utf8');
  rates = JSON.parse(raw);
}

loadRates();

function convert(amountCents, currency) {
  const rate = rates[currency];
  return Math.round(amountCents * rate);
}

module.exports = { convert };
```

Column 21 of line 16 is the `[` in `rates[currency]` — so the thing being read
from is `rates`, and `rates` is `null` at the moment `convert()` runs. But line 6
sets `rates = null` and line 13 calls `loadRates()`, which assigns it. Reading the
file tells me nothing about *when* that assignment lands. That is the question.

## 3. The callers, in trace order

```console
> type src\order.js

const { convert } = require('./rates');

function totalUsdCents(order) {
  return order.items.reduce((sum, item) => {
    return sum + convert(item.amountCents, item.currency);
  }, 0);
}

module.exports = { totalUsdCents };
```

```console
> type src\index.js

const fs = require('fs');
const path = require('path');
const { totalUsdCents } = require('./order');

const ORDERS_FILE = path.join(__dirname, '..', 'data', 'orders.jsonl');

const lines = fs
  .readFileSync(ORDERS_FILE, 'utf8')
  .split('\n')
  .filter((line) => line.trim().length > 0);

const orders = lines.map((line) => JSON.parse(line));

for (const order of orders) {
  const usd = totalUsdCents(order);
  console.log(`${order.id}\t${usd} USD-cents`);
}
```

`index.js:15` calls `totalUsdCents`, which reduces with `convert`, which throws.
The whole chain is synchronous — there is no `await` anywhere between line 15 of
`index.js` and line 16 of `rates.js`.

## 4. Instrument instead of guessing

Hypothesis: `loadRates()` at `rates.js:13` is `async`, so it returns a pending
promise and `rates` is still `null` when `require('./rates')` finishes. Test it by
printing the order of events — probe committed at `probes/order-vs-data.js`.

```console
> node probes\order-vs-data.js

A: before require
B: require returned
C: convert threw: Cannot read properties of null (reading 'USD')
```

`B` before `C` rules out a parse problem: `require` returns, and the very first
call throws. Good. But it does not yet prove the data is fine — maybe the JSON is
bad and `rates` would *never* be set.

Second probe, same module, same function, called 50 ms later so the pending
promise has settled (`probes/late-call.js`):

```console
> node probes\late-call.js

D: 50ms later, convert(100, 'USD') = 100
```

`convert(100, 'USD')` returns `100` — correct, `100 * 1.0`. So the file reads, the
JSON parses, the rates table is right and the math is right. The only defect is
ordering: the load is asynchronous and nothing waits for it.

## 5. Root cause

`src/rates.js` was switched to `node:fs/promises`, so `loadRates()` became
`async` and line 13's bare `loadRates()` discards the promise. The module's
public API, `convert()`, is synchronous and is called from inside an
`Array.reduce`, so `rates` is still `null` on the first call. A stack trace with
three synchronous frames was enough to kill the "async is faster" instinct.

## 6. The change — exactly one

Make the load synchronous, because the consumer it must satisfy is synchronous.
No other file is touched.

```console
> git diff -- src/rates.js

diff --git a/examples/orders-demo/src/rates.js b/examples/orders-demo/src/rates.js
index c2f3a53..72bbd69 100644
--- a/examples/orders-demo/src/rates.js
+++ b/examples/orders-demo/src/rates.js
@@ -1,12 +1,12 @@
-const fs = require('node:fs/promises');
+const fs = require('node:fs');
 const path = require('node:path');
 
 const RATES_FILE = path.join(__dirname, '..', 'data', 'rates.json');
 
 let rates = null;
 
-async function loadRates() {
-  const raw = await fs.readFile(RATES_FILE, 'utf8');
+function loadRates() {
+  const raw = fs.readFileSync(RATES_FILE, 'utf8');
   rates = JSON.parse(raw);
 }
 
```

## 7. Re-run the exact same command

```console
> node src/index.js

A-1001	3580 USD-cents
A-1002	4000 USD-cents
A-1003	3258 USD-cents
```

Exit code: **0**.

## 8. Re-run the probe that caught it

```console
> node probes\order-vs-data.js

A: before require
B: require returned
C: convert returned
```

`C: convert returned` where it used to say `C: convert threw`. The probe that
proved the bug now proves the fix.

## 9. The file after the fix

```console
> type src\rates.js

const fs = require('node:fs');
const path = require('node:path');

const RATES_FILE = path.join(__dirname, '..', 'data', 'rates.json');

let rates = null;

function loadRates() {
  const raw = fs.readFileSync(RATES_FILE, 'utf8');
  rates = JSON.parse(raw);
}

loadRates();

function convert(amountCents, currency) {
  const rate = rates[currency];
  return Math.round(amountCents * rate);
}

module.exports = { convert };
```

## 10. Did the numbers come out right?

Hand arithmetic against `data/rates.json` (`USD 1.0`, `EUR 1.08`, `GBP 1.27`):

| order | items | hand total | output |
| --- | --- | --- | --- |
| A-1001 | 2500 USD + 1000 EUR | `2500 + 1080 = 3580` | `3580 USD-cents` |
| A-1002 | 4000 USD | `4000` | `4000 USD-cents` |
| A-1003 | 1800 GBP + 900 EUR | `2286 + 972 = 3258` | `3258 USD-cents` |

Output matches the arithmetic. The fix changed behaviour in one place and broke
nothing else.

## 11. What I did *not* do

- I did not make `convert()` async and push `await` up through `order.js` and
  `index.js`. That is a three-file change to fix a one-line defect, and it would
  have been chosen before proving the call chain was synchronous.
- I did not touch `data/rates.json`, `order.js`, or `index.js`. The probes show
  the bug was never in them.

## 12. Reproducing the failure from a clean checkout

The buggy version of `src/rates.js` is still in git history. Find the commit
that introduced the demo:

```console
> git log --oneline -- examples/orders-demo

f7944b1 examples: add reproducible buggy demo project
```

Check that commit out, run `node src/index.js`, and you get the trace from
section 1 again — identical apart from your own checkout path.
