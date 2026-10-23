# L-003 — The compiled workflow has no first-class key

**Gap.** The PoC freezes an ADG digest beside the admit record but nothing names it. `docs/LATER.md` §1 says `%w` (procedure + oracle bundle + F + budget) must be a key, distinct from `%k` and from `memory_id`; no schema has it.

**Carrier.** `examples/later/wf_acme_specialize.compile.lintel` compiled to an ADG whose digest appears as `%w` in the admit record and in `cache-key`.

**Change.** `cache-key.v1` with `w` (ADG digest) next to `k`; `lintel-ir.poc` gains a `compile` module header carrying the `%w` fields. Same `%w` ⇒ same ADG or hard fail.

**Falsifier.** Two modules with identical procedure, oracles, F and budget produce different `%w`, or `%w` changes when only `memory_id` changes. Survey item: T10 (workflow compile), T3.

**Loop.** application

**Depends on.** none

**Status.** open
