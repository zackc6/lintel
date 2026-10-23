# L-001 — `artifact.kind` cannot name what the sinks emit

**Gap.** `schemas/admit-record.v0.schema.json` restricts `artifact.kind` to `{triton_kernel, acf, schedule_ir, none}` — none of which names what the sinks emit (`source`, `cubin`, `npu-bin`). The bench's freeze records (agentic-compiler `cases/accept/*`, NVIDIA cubin and Ascend npu-bin) fail validation on exactly that field (agentic-compiler `docs/DRIFT.md`, DRIFT-1).

**Carrier.** A bench freeze record for `gemm_tile` on `ascend-a2` (`artifact.kind: npu-bin`) placed under `examples/`; it must validate.

**Change.** `admit-record.v1` beside `v0`: `artifact.kind` ∈ {`source`, `cubin`, `npu-bin`} plus whatever `v0` had. Choreo owns artifact kinds (`AGENTS.md`), so the enum values are taken from `docs/LINTEL_CONSUME.md` verbatim; Lintel owns only the field name.

**Falsifier.** Choreo's consume-check reports a new mismatch, or the bench's drift test still fails after the submodule bump. Survey item: P14 (pins in admit records).

**Loop.** application (record shape); the fix is a contract field, not a loop change

**Depends on.** none

**Status.** open
