# L-009 — A failed replay has no record shape

**Gap.** Walk E (`docs/WHY.md`): re-walking the same ADG after a model swap must reproduce the terminator and digest or hard-fail. `docs/POC.md` item 4 requires it; no schema says what a replay failure *is* (not a `reject`, not a `revert`).

**Carrier.** `examples/admit-record.json` replayed under a different `pins.model` with (a) identical outcome and (b) a divergent digest; (b) lowers to a replay-failure record that names both digests.

**Change.** `admit-record.v1`: `replay` object `{of: %k, expected_digest, got_digest, outcome ∈ {held, diverged}}`; `diverged` is a fourth terminal that never writes `store[%k]`.

**Falsifier.** A divergence that the record attributes to the model when the compiler pin also changed (then it is a new `%k`, not a replay). Survey item: T3, P12 (golden replay); kill switch "replay after model swap is flaky → no GA" (`docs/RISKS.md`).

**Loop.** application

**Depends on.** none

**Status.** open
