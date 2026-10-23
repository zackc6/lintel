# L-013 — The controller-development module is sketched, not specified

**Gap.** `examples/later/controller-dev.sketch.lintel` exists; `docs/LATER.md` §7 lists the required/forbidden table and the four arms. There is no schema for a `promote` record, so the experiment cannot be written down even though running it is gated.

**Carrier.** A `promote` record over four arms (fixed policy, memory-only, frozen procedure, conventional search) on disjoint dev/holdout families, ending in `promote policy_id` or `reject`.

**Change.** `promote-record.v0` (new schema; no example may claim to have run it). `promote` publishes `policy_id` only; never `land`, never a cubin.

**Falsifier.** The record can be filled by a session log alone (then it is memory, not a controller). Survey item: T5, §5.2 step 6; gate in `docs/SURVEY_MATCH.md`.

**Loop.** controller

**Depends on.** L-003, L-011

**Status.** blocked (run only after the SURVEY_MATCH gate: repeated serving wins + one compiler change measured on a non-motivating workload; the *spec* may land earlier)
