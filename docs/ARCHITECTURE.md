# Architecture (e2e stack + mechanisms)

The survey’s 1–3 year uncertainty is *which IR, which flag, which vendor surface* — not whether agents exist. Lintel is a **small control-plane IR + plugins**. Cake, DeepSeek Harness, and GEAK are **mechanisms**, not the product.

## E2E software stack

Two paths. Same cache key. The specialize path may use an LLM. The serve path must not.

```text
 MODEL / FRAMEWORK          torch.compile · exported graph
        │
        │  regions · fingerprints · Amdahl rank
        ▼
 fitness F = serving tokens/s (or TTFT) · quality parity · $/compile
        │
 ┌──────┴───────────────────────────────────────────────────────────┐
 │  LINTEL CONTROL PLANE                                            │
 │                                                                  │
 │   Lintel IR (cache_key / propose / gate / land|revert|reject)    │
 │      %k = cache_key(graph, hw, compiler, adapter, policy)        │
 │                                                                  │
 │   session log = interpretation trace     (DSH pattern)           │
 │   seams: llm · tools · sandbox · adapter · oracle · serving      │
 └──────┬───────────────────────────────┬───────────────────────────┘
        │ SPECIALIZE (CI / overnight)   │ SERVE (production)
        │ interpret Lintel IR           │ lookup %k
        │ LLM fills enum slots only     │
        ▼                               ▼
 admit record (lowering)          hit: artifact.digest
 land under %k                    miss / replay-fail:
        │                           last_good | classical
        ▼                               │
 adapter IR  Triton (yr1)               │  NO LLM
   Tile / HIP / Cake IR (later)         │
        │                               │
        ▼                               ▼
 classical lowering / vendor libs ──► SGLang xor vLLM ──► GPU
```

**Invariant.** If the controller, the LLM, or a plugin dies, `lookup(%k)` still serves the last freeze (or classical). That is the commercial sentence.

**Year-1 width.** One GPU family, one adapter, one serving engine. Default: NVIDIA + Triton + (SGLang xor vLLM). Home fleet is a kickoff **swap**, not a second live path.

## Mechanisms (what we take, where they sit)

| Mechanism | From | In this stack | We discard |
|---|---|---|---|
| Typed agent contract + **localized reject** | Cake | `propose` enum + `gate` `{where, seam, reason}` | Cake IR as the kernel language; 80M-token clean-start UX |
| Plugin **seams** + append-only session log | DeepSeek Harness | Runtime around Lintel IR; model-visible ⇒ logged | Coding-agent UX as the SKU; free tool-calling on the SLA path |
| Amdahl on a **warm** server + A/B + parity | GEAK v4 | `triage` + `gate serving_ab` + \(F\) | Instinct-only marketing; hero-kernel as “default agent compile” |
| Artifact-in-VCS / control file | CompileIQ-class | `land %p under %k` → customer git | Vendor-only ACF as the ABI |
| **Cache key + replay** | Survey T3 (missing as a product) | `%k = cache_key(...)`; same key ⇒ same terminator or hard fail | Silent retune on model swap |
| Lintel IR | This product | Control-plane IR; JSON record is a **lowering** | Mega-IR; “one agent IR for all vendors” |

Adapters (Triton / Tile / HIP / Cake IR) are **data-plane IRs**. They plug into `adapter`. They are not Lintel IR.

## Lintel IR objects (year-1 kernel)

Five things must be boring. Everything else is a plugin.

### 1. Cache key `%k` (address of the specialize job)

Canonical fields — **not** the kernel text, **not** the model id, **not** the enum:

```text
cache_key.v0 = hash( graph_hash, hw_id, compiler_ver, adapter_id, policy_id )
```

| In the key | Out of the key (on purpose) |
|---|---|
| Which region/graph | `model_id` (audit only) |
| Which HW + compiler + adapter | `enum_id` / proposal body (payload at `%k`) |
| Which **policy** (which gates, which \(F\)) | Commentary, SSA temps, token spend |

**Replay law.** Re-interpret under the same `%k`. If the terminator (`land`/`revert`/`reject`) or the landed digest changes, **hard fail — do not serve.** A model swap with the same policy is the same `%k`. A compiler bump is a new `%k` and must re-land.

Serve is `lookup(%k)`, not “run the agent again.”

### 2. Lintel IR plan (the program)

Linear block year 1. Agent fills enumerated slots. Agent does not add opcodes.

```text
%k  = cache_key @region, pins
%r  = triage @region
%p  = propose propose_schedule "<enum_id>"
%g  = gate <oracle> %p owner @team     // fail → {where, seam, reason}
%f  = fitness %g vs last_good
land %p, %f under %k or_else last_good
     | revert last_good under %k
     | reject {where, reason}
```

Spec and examples: [LINTEL_IR.md](LINTEL_IR.md). CFG / cost / T10 sketches (not GA): [LATER.md](LATER.md).

### 3. Admit record (lowering / merge ticket)

Closed module → versioned JSON in customer git. Humans review this, not the chat. [ADMIT_RECORD.md](ADMIT_RECORD.md).

### 4. Seams (DSH pattern, compiler-shaped)

| Seam | Year-1 provider | Later, no rewrite |
|---|---|---|
| `llm` | One frontier + one small specialist | Any OpenAI-class / local |
| `tools` | `propose` / `verify` / `bench` / `profile` | MCP-class |
| `session` | Append-only log (sqlite ok) | Customer object store |
| `sandbox` | Container / Landlock | Air-gap runner |
| `adapter` | Triton | Tile, HIP, Helion, Cake-class, Argus-class |
| `oracle` | Golden + numerical + shape-grid | Alive2, SMT, FlashInfer-Bench `apply()`, GEAK A/B |
| `serving` | SGLang **xor** vLLM | The other engine |

### 5. Localized reject (Cake idea, portable)

A failed `gate` is not a bit. It names **where** and **which seam**. Recurring failures become a new oracle plugin or a tighter enum (test-gated). That is T5-lite — not silicon codesign.

## Two paths in one picture

```text
 SPECIALIZE                          SERVE
 ──────────                          ─────
 Lintel IR                           lookup(%k)
   │                                   │
   ├─ %k = cache_key                   ├─ hit  → artifact.digest
   ├─ propose enum                     ├─ miss → last_good | classical
   ├─ gate* (owned)                    └─ replay-fail → do not serve new
   ├─ fitness F
   └─ land | revert | reject
         │
         ▼
   admit record + session trace
   artifact stored at %k
```

FSM (SLA): `triage → propose → gate → measure → fitness → land | revert`. Same states as Lintel IR ops. Lab mode may be looser; it cannot `land` without the SLA plan.

## How this survives survey-driven change

| If this settles in 2027–28 | Lintel change |
|---|---|
| **C3-A** free rewrite wins a public suite | Widen enums *behind* gates; keep Lintel IR |
| **C3-B** constrained actions hold | Keep narrow enums; sell that |
| **C4** Tile / Cake IR / Argus fragment | New `adapter` enum; same `%k` schema |
| **C2** someone publishes default-path p50 | Report partner traces in that format |
| **C5** vendors name ACF workflows | Integrate; we stay the admit/freeze layer |
| **C6-A** no classical fallback | **Do not follow** |
| Cake or Argus open-source | Provider, not a rewrite |
| DSH plugin ABI wins | Oracles + Lintel IR interpreter as `dsh-plugin`s; T10 ADG freeze is [LATER.md](LATER.md) |

Wrong adapter is recoverable. Wrong “we are the compiler” story is not. `%k` + Lintel IR are the Q1 bets.

## Repo layout (what 10 people grow)

This plan repo is `docs/` + `schemas/` + `examples/`. The tree below is the product repo they grow.

```text
schemas/                 # lintel-ir, admit-record, cache-key, session
examples/lintel-ir/      # text + JSON programs (v0)
examples/later/          # CFG / cost / T10 sketches — not SLA
examples/admit-record*   # lowerings
src/lintel/              # hash %k, replay law, FSM, seams
adapters/                # year-1 triton/   later tile/ hip/ cake_ir/
oracles/ serving/ cli/
docs/
```

## Kickoff

Week-1 pins (in `%k` or audit): GPU family, serving engine, op family. Changing them later is a new provider or a new `%k`, not a fork.

## Non-goals

- One universal cost model for L1–L7. A pinned \(F\)+budget `cost` op is year 2 ([LATER.md](LATER.md)), not v0.
- One mega-IR / Cake IR as the SKU.
- Always-on frontier model at every customer compile.
- Serving a proposal before \(F\)-admit.
- Putting `model_id` or free text into `%k`.
