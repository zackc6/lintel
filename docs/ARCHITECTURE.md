# Architecture (e2e stack + mechanisms)

The survey’s 1–3 year uncertainty is *which IR, which flag, which vendor surface* — not whether agents exist. Lintel is a **small control-plane IR + plugins**. Cake, DeepSeek Harness, and GEAK are **mechanisms**, not the product. Why this IR exists and how the Acme walks hit L1–L7: [WHY.md](WHY.md). Data-plane PoC (Choreo Kernel AST, Triton printer): [DATA_PLANE.md](DATA_PLANE.md), [CHOREO.md](CHOREO.md). LLM role / stratum pins: [LLM_IR.md](LLM_IR.md). Independent IR survey (not that paper): [LLM_ORIENTED_IR.md](LLM_ORIENTED_IR.md).

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
 │   Lintel IR (CFG · cost · cache_key · land|revert|reject)       │
 │      %k = cache_key(graph, hw, compiler, adapter, policy)        │
 │                                                                  │
 │   session log = interpretation trace     (DSH pattern)           │
 │   seams: llm · tools · sandbox · adapter · oracle · serving      │
 └──────┬───────────────────────────────┬───────────────────────────┘
        │ SPECIALIZE (CI / overnight)   │ SERVE (production)
        │ compile → ADG; walk ADG      │ lookup %k
        │ LLM fills enum slots only     │
        ▼                               ▼
 admit record (lowering)          hit: artifact.digest
 land under %k                    miss / replay-fail:
        │                           last_good | classical
        ▼                               │
 adapter IR  Choreo Kernel AST (yr1) │  NO LLM
   Triton printer / Tile / HIP / Cake  │
        │                               │
        ▼                               ▼
 classical lowering / vendor libs ──► SGLang xor vLLM ──► GPU
```

**Invariant.** If the controller, the LLM, or a plugin dies, `lookup(%k)` still serves the last freeze (or classical). That is the commercial sentence.

**Year-1 width.** One GPU family, one adapter, one serving engine. Default: NVIDIA + **Choreo** (Triton printer) + (SGLang xor vLLM). Home fleet is a kickoff **sink swap**, not a second live face.

## Lintel IR vs survey L1–L7

Survey [§5.1.2](https://github.com/zackc6/ai-compiler-survey/blob/main/docs/SURVEY.md): L1–L7 are **data-plane bands**. Agents sit **above** them via tools. Lintel IR is that control plane. It is **not** L8 and **not** a replacement for any band. One cost model across L1–L7 stays a non-goal.

```text
  L1  Framework graph     torch.compile / exported module
  L2  Portable graph IR   graph_hash in %k (StableHLO-class when present)
  L3  Mid-IR / dialects   Inductor / MLIR / HLO — classical, not proposed in PoC
  L4  Kernel DSL          adapter: Choreo Kernel AST (yr1) · Triton printer · Tile / HIP / Cake IR (later wrap)
  L5  Backend / ISA       PTX / SASS — classical lowering of L4
  L6  Runtime / serving   SGLang xor vLLM · CUDA Graphs · lookup(%k)
  L7* Fleet / cluster     out of PoC; later placement plugin, not a FleetIR SKU
  L0* CPU / LLVM          job (b) — out
        │
        │  control plane talks *to* bands through seams
        ▼
  Lintel IR  triage / propose / gate / cost / land   ← this product
  ADG walk   (specialize)          lookup(%k) (serve)
```

Worked example: [examples/poc/acme_attn_prefill.poc.lintel](../examples/poc/acme_attn_prefill.poc.lintel). Same `%k`. Each op touches one band (or none — control only). Step-by-step walks (land / revert / cost skip / cold / replay): [WHY.md](WHY.md).

| PoC op | Band | What happens | What Lintel IR does **not** do |
|---|---|---|---|
| `region` + `graph = sha256:bbcd57…` | **L1→L2** | Fingerprint of the captured attn-prefill subgraph | Rewrite the torch graph; invent a portable IR |
| `triage` · `cond %r.hot` | **L1** (cut) + Amdahl | Skip cold regions (`^cold` → `revert`) | Fuse ops at L3; change the export boundary |
| `pins.compiler` / `adapter = @choreo.v0` | **L3/L4 pin** | Which classical stack must replay (`choreoir` + sink) | Run InstCombine / Inductor passes |
| `%p0 = propose … kernel choreo.attn.d3.w4` | **L4** | Fill an allowlisted Choreo Kernel AST | Emit CUDA, free Triton source, or Cake IR |
| `gate adapter` `{where: L}` | **L4 pre-codegen** | `choreoir.check` localized Finding | A new checker IR inside Lintel |
| `gate golden` / `gate numerical` | **L4 after L5 lower** | Oracle on the cubin the adapter produced | Legalize PTX; allocate registers |
| `cost … budget.usd = 50` | **control** (survey: economics are not a band) | Skip L6 A/B if it cannot pay back | A universal L1–L7 analytical model |
| `gate serving_ab` · `fitness F = tokens/s × parity` | **L6** | Warm-server A/B + output parity | Own CUDA Graphs / KV cache / the engine |
| `land %p0 under %k` | **L6 freeze** | `store[%k] = digest`; serve is `lookup(%k)` | Re-run Lintel IR on the hot path |
| *(not in PoC)* `place` | **L7** | Later plugin ([LATER.md](LATER.md) coverage) | Ship FleetIR |

**C4** (Triton vs Tile vs Cake IR) is an **L4 sink** fight. Year 1 picks one L4 **face** (Choreo) and one printer. A second DSL is a new `adapter_id` or printer (new `%k`), not a new Lintel IR.

**T5-lite** (recurring fail → new check) may later name an **L5** `where` (`ptx.barrier`). That grows an oracle plugin. It does not grow an ISA dialect in this company.

**L0 / job (b)** (Magellan / MLGO) never appears in Lintel IR.

## Mechanisms (what we take, where they sit)

| Mechanism | From | In this stack | We discard |
|---|---|---|---|
| Typed agent contract + **localized reject** | Cake / Choreo | `propose` **Kernel AST** + `gate adapter` `{where, hint}` + `gate` `{where, seam, reason}` | Cake IR as the kernel language; Choreo-the-company |
| Plugin **seams** + append-only session log | DeepSeek Harness | Runtime around Lintel IR; model-visible ⇒ logged | Coding-agent UX as the SKU; free tool-calling on the SLA path |
| Amdahl on a **warm** server + A/B + parity | GEAK v4 | `triage` + `gate serving_ab` + \(F\) | Instinct-only marketing; hero-kernel as “default agent compile” |
| Artifact-in-VCS / control file | CompileIQ-class | `land %p under %k` → customer git | Vendor-only ACF as the ABI |
| **Cache key + replay** | Survey T3 (missing as a product) | `%k = cache_key(...)`; same key ⇒ same terminator or hard fail | Silent retune on model swap |
| Lintel IR | This product | Control-plane IR; JSON record is a **lowering** | Mega-IR; “one agent IR for all vendors” |

Adapters (Choreo face / Triton printer / Tile / HIP / Cake IR) are **data-plane IRs**. They plug into `adapter`. They are not Lintel IR. Year-1 live adapter contract: [ADAPTERS.md](ADAPTERS.md).

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

Linear block is a **degenerate** CFG. Year-1 executable: [POC.md](POC.md). Coverage: [LATER.md](LATER.md).

```text
%k  = cache_key @region, pins
%r  = triage @region
%p  = propose propose_kernel "<slot>"          // Choreo Kernel AST
%s  = gate adapter %p owner @team      // fail → {where: L, hint: c0}
%g  = gate <oracle> %p owner @team     // fail → {where, seam, reason}
%f  = fitness %g vs last_good
land %p, %f under %k or_else last_good
     | revert last_good under %k
     | reject {where, reason}
```

Spec and examples: [LINTEL_IR.md](LINTEL_IR.md). PoC (CFG + cost + ADG): [POC.md](POC.md). Coverage: [LATER.md](LATER.md).

### 3. Admit record (lowering / merge ticket)

Closed module → versioned JSON in customer git. Humans review this, not the chat. [ADMIT_RECORD.md](ADMIT_RECORD.md).

### 4. Seams (DSH pattern, compiler-shaped)

| Seam | Year-1 provider | Later, no rewrite |
|---|---|---|
| `llm` | One frontier + one small specialist | Any OpenAI-class / local |
| `tools` | `propose` / `verify` / `bench` / `profile` | MCP-class |
| `session` | Append-only log (sqlite ok) | Customer object store |
| `sandbox` | Container / Landlock | Air-gap runner |
| `adapter` | Choreo Kernel AST + `{where: W\|L\|S\|V}` | Tile, HIP, Helion, Cake-class wrap; Triton knobs as degenerate |
| `oracle` | Golden + numerical + shape-grid | Alive2, SMT, FlashInfer-Bench `apply()`, GEAK A/B |
| `serving` | SGLang **xor** vLLM | The other engine |

### 5. Localized reject (Cake idea, portable)

A failed `gate` is not a bit. It names **where** and **which seam**. Adapter fails name a **node hint** (`c0`). Recurring failures become a new `choreoir.check` rule or a tighter allowlist (test-gated). That is T5-lite — not silicon codesign.

## Two paths in one picture

```text
 SPECIALIZE                          SERVE
 ──────────                          ─────
 Lintel IR                           lookup(%k)
   │                                   │
   ├─ %k = cache_key                   ├─ hit  → artifact.digest
   ├─ cond (hot / ok / worth_measure)  ├─ miss → last_good | classical
   ├─ propose schedule (allowlisted)   └─ replay-fail → do not serve new
   ├─ gate adapter {where}
   ├─ gate* (owned)
   ├─ cost (same F + budget)
   ├─ fitness F
   └─ land | revert | reject
         │
         ▼
   admit record + session trace
   artifact stored at %k
```

FSM (SLA): walk the PoC ADG (`cond` on hot / ok / worth_measure) → `land | revert`. Lab mode may be looser; it cannot `land` without the SLA graph.

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
| DSH plugin ABI wins | Oracles + ADG interpreter as `dsh-plugin`s; `%w` freeze is [LATER.md](LATER.md) |

Wrong adapter is recoverable. Wrong “we are the compiler” story is not. `%k` + Lintel IR are the Q1 bets.

## Repo layout (product tree they grow)

This plan repo is `docs/` + `schemas/` + `examples/`. The tree below is the product repo they grow.

```text
schemas/                 # lintel-ir, adapter-proposal, admit-record, cache-key, session
examples/lintel-ir/      # degenerate linear modules (opaque enum_id)
examples/poc/            # CFG + cost + ADG + Choreo Kernel AST (year-1 executable)
examples/later/          # coverage after PoC (%w, richer graphs, degenerate Triton knobs)
src/lintel/              # hash %k, replay law, FSM, seams
adapters/                # year-1 triton/   later tile/ hip/ cake_ir/
oracles/ serving/ cli/
docs/                    # WHY, POC, DATA_PLANE, ADAPTERS, …
```

## Kickoff

Week-1 pins (in `%k` or audit): GPU family, serving engine, op family. Changing them later is a new provider or a new `%k`, not a fork.

## Non-goals

- One universal cost model for L1–L7. PoC `cost` is the same pinned \(F\) + a budget ([POC.md](POC.md)).
- One mega-IR / Cake IR as the SKU.
- Always-on frontier model at every customer compile.
- Serving a proposal before \(F\)-admit.
- Putting `model_id` or free text into `%k`.
