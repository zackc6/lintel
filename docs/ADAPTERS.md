# Adapters — data-plane plugins

An **adapter** is a compiler Lintel does not own. Year-1 it accepts a **Choreo Kernel AST**, runs `choreoir.check`, and (once a **sink** consumes the schedule) lowers on one GPU family. Returns an artifact + gate/oracle facts.

Year-1: **one** live adapter. Coverage: more `adapter_id`s, never one IR for all of them.

---

## Year-1 live

| `adapter_id` | Agent-facing type | Lowers with | Status |
|---|---|---|---|
| `@choreo.v0` | [Choreo](https://github.com/zackc6/choreo) Kernel AST (buffers, layout, partitions, Copy/Mma/Barrier/Pipeline) | `choreoir.check` then Triton printer (first sink) | **PoC live** |

Gate checks are Choreo Finding bands: `W`, `L`, `S`, `V`. After a printer exists, also `compile_ok`. Implementation = `choreoir` + vendor toolchain, not a new checker IR in this repo.

---

## Degenerate / Q3 stub

| `adapter_id` | Notes |
|---|---|
| `@triton.v0` | Degenerate L4: `num_warps` / `block_*` knobs. M2 kill-switch if Choreo has no device sink. |
| `@tile.v0` | NVIDIA Tile-ish; **no** compile in year-1 (Q3 empty stub) |
| `@hip.v0` | AMD; **no** compile in year-1 (Q3 empty stub) |

Stub = schema + `adapter_id` in `%k` + reject `unsupported`. Not a second performance path. Pick **one** of tile/hip for the Q3 stub.

---

## Later (not the SKU)

| `adapter_id` | When |
|---|---|
| `@cake.v0` | Public Cake compiler **or** funded customer. Wrap; do not fork as Lintel Cake. |
| `@tirx.v0` | Partner already in Apache TVM / TIRx. GPU **sink** (must consume `Pipeline.depth`). Wrap FFI + `tir_pipeline="tirx"`; new `%k`. Not year-1 live. |
| `@tilelang.ascend` | Partner already serves on Ascend **and** one NVIDIA cubin has landed. Second sink, not a second AST. Sketch: [examples/later/tilelang-ascend.sketch.md](../examples/later/tilelang-ascend.sketch.md). |
| `@helion.*` / CuTe / CUTLASS templates | If a partner already lives there |
| `@inductor` | Only if we ever propose **L3** schedules (year-1: pin `compiler_ver`, do not search Inductor) |

---

## Contract (all adapters)

1. **Input:** Kernel AST (required year-1 live) or degenerate schedule record / later kernel text.
2. **`adapter_gate`:** pass/fail + `{where}` + optional `hint` node/field + Finding JSON.
3. **Compile:** a **sink** that consumes roles/barriers/`Pipeline.depth`/spaces + vendor toolchain. Timeout → fail closed. A stencil that comments those fields is not compile. No sink → no cubin; still run check.
4. **Output:** artifact bytes + hashes for admit-record `artifact_hash`.
5. **Do not** put `model_id` or `Kernel.target` in the adapter input that feeds `%k`. Admission is `hw_id`.

Schema: [schemas/adapter-proposal.v0.schema.json](../schemas/adapter-proposal.v0.schema.json). Pros/cons: [CHOREO.md](CHOREO.md).
