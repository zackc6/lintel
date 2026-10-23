# L-007 — Two sink families, one control plane — is `hw_id` enough?

**Gap.** The bench already freezes `gemm_tile` as NVIDIA cubin and as Ascend npu-bin. `docs/LATER.md` §5 says a second adapter / engine is a new `%k`, same IR. Nothing in `schemas/` states which pin fields differ between the two families or whether a `Kernel.target` leak into `%k` is rejected (`.cursor/skills/lintel/SKILL.md`: do not put `Kernel.target` in `%k`).

**Carrier.** Two admit records for the same region, `pins.hw_id ∈ {nvidia.h100, ascend.a2}`, same `graph_hash`, different `%k`; a third with `Kernel.target` copied into the key that must fail validation.

**Change.** `cache-key.v1` documents the exact field set (`graph`, `hw`, `compiler`, `adapter`, `policy_id`) and forbids kernel-level fields; `validate_contract.py` checks the forbidden set.

**Falsifier.** A legitimate pin field that both families need and the key cannot carry. Survey item: C4 (one language or several — hedged via adapters), P7.

**Loop.** application

**Depends on.** none

**Status.** open
