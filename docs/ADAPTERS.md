# Adapters — data-plane plugins

An **adapter** is a compiler Lintel does not own. It accepts a **typed schedule** (year-1) or later kernel text, lowers on one GPU family, returns an artifact + gate/oracle facts.

Year-1: **one** live adapter. Coverage: more `adapter_id`s, never one IR for all of them.

---

## Year-1 live

| `adapter_id` | Agent-facing type | Lowers with | Status |
|---|---|---|---|
| `@triton.v0` | Schedule: `num_warps`, `num_stages`, `block_m/n/k` (Triton-legal) | Partner Triton / PyTorch Inductor | **PoC live** |

Gate checks (names are bands, Cake-style `{where}`): `smem`, `occupancy`, `tma_align`, `compile_ok`. Implementation = Triton/CUDA limits, not a new checker IR.

---

## Q3 stub (empty)

Exactly one of:

| `adapter_id` | Notes |
|---|---|
| `@tile.v0` | NVIDIA Tile-ish; **no** compile in year-1 |
| `@hip.v0` | AMD; **no** compile in year-1 |

Stub = schema + `adapter_id` in `%k` + reject `unsupported`. Not a second performance path.

---

## Later (not the SKU)

| `adapter_id` | When |
|---|---|
| `@cake.v0` | Public Cake compiler **or** funded customer. Wrap; do not fork as Lintel Cake. |
| `@helion.*` / CuTe / CUTLASS templates | If a partner already lives there |
| `@inductor` | Only if we ever propose **L3** schedules (year-1: pin `compiler_ver`, do not search Inductor) |

---

## Contract (all adapters)

1. **Input:** schedule record (required year-1) and/or kernel text (later).
2. **`adapter_gate`:** pass/fail + `{where}` + optional `hint` field name.
3. **Compile:** vendor toolchain. Timeout → fail closed.
4. **Output:** artifact bytes + hashes for admit-record `artifact_hash`.
5. **Do not** put model id in the adapter input that feeds `%k`.

Schema: [schemas/adapter-proposal.v0.schema.json](../schemas/adapter-proposal.v0.schema.json).
