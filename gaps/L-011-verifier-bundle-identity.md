# L-011 — An intra-session verifier bundle has no identity

**Gap.** `docs/LATER.md` §8: extra `check` rules grown as data must be hashed beside `compiler_ver` inside `%k`; a longer retrieval corpus is `memory_id` only; a next-slot rule is a new `policy_id`. No schema field classifies a bundle, so the three cannot be told apart in a record.

**Carrier.** Three admit records that differ only in which bundle kind changed; exactly one changes `%k`.

**Change.** `pins.verifier_bundle: {hash, kind ∈ {compiler, memory, controller}}`; only `kind: compiler` enters `cache-key`.

**Falsifier.** A bundle that is both a check rule and a next-slot rule (the classification is not a partition). Survey item: T5 (two clocks), kill switch "evolves during compilation without naming the artifact and the clock".

**Loop.** compiler (identity of a compiler change)

**Depends on.** L-007

**Status.** open
