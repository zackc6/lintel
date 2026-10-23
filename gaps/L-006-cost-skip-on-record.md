# L-006 — A cost skip leaves no trace on the admit record

**Gap.** Walk C (`docs/WHY.md`) skips the serving A/B when `worth_measure = false`, but `admit-record.v0` has nowhere to say *skipped vs spent*, and `budget.usd` is a constant, not a partner SLO.

**Carrier.** `examples/later/acme_attn_prefill.cost.lintel` lowered to an admit record that shows `cost: {decision: skip, F_prior: …, budget_source: slo}`.

**Change.** `admit-record.v1`: `cost` object with `decision ∈ {skip, spend}`, the prior `last_good.F` used, and `budget_source`. Budget stays on the policy, never on the model.

**Falsifier.** A skip that cannot be audited from the record alone, or a budget value that an agent slot can write. Survey item: P9 (always $/compile), P23 (tokens / Amdahl).

**Loop.** application

**Depends on.** none

**Status.** open
