# Architecture (built to change)

The survey’s 1–3 year uncertainty is **not** “will agents exist.” It is *which IR, which default flag, which vendor surface*. Lintel is therefore a **small kernel + replaceable plugins**. DeepSeek Harness is the runtime *pattern*. Cake is the *contract* pattern on one L4 surface. Neither is the monolith.

## Picture

```text
                         fitness F (customer-named front)
                                   │
                    ┌──────────────▼──────────────┐
                    │     E2E search controller     │
                    │  FSM / plan (SLA) + LLM judge │
                    │  Amdahl cut · budget · stop   │
                    └──────────────┬──────────────┘
           plugins via seams       │
     ┌────────────┬────────────────┼─────────────┬────────────┐
     ▼            ▼                ▼             ▼            ▼
  Session     Tool/LLM         Admit         Artifact      Serving
  log         adapters         stack         store         A/B
  (DSH)       (seams)          (T2)          (T3 freeze)   (T6)
                                   │
                    ┌──────────────▼──────────────┐
                    │   Compiler adapters (T1)     │
                    │  Triton · (yr2) Tile/HIP     │
                    │  optional Schedule-IR plugin │
                    │  (Cake-class, not required)  │
                    └──────────────┬──────────────┘
                                   ▼
                    classical lowering / libs
                    (Inductor · Triton · vendor)
                    Lintel never replaces this
```

**Invariant.** If the controller, the LLM, or a plugin dies, the last **admitted freeze** still serves. That is the commercial sentence.

## Four product objects (do these first)

These are the only objects year-1 code must make boring. Everything else is a plugin.

### 1. Admit record (the contract)

Versioned, hash-chained, customer-owned:

```text
{
  region_id, graph_hash, hw_id, compiler_ver,
  action[],            // enumerated — not free text
  oracles[],           // name, version, result, false-neg owner
  artifact_digest,
  F_delta,             // vs frozen baseline, on named traces
  policy_id, model_id,
  fallback             // last_good | classical
}
```

Natural language is optional commentary. If it is not in the record, it did not happen (DeepSeek Harness rule: **model-visible ⇒ logged**).

### 2. Artifact + cache key (freeze)

Content-addressed: `(IR/region hash, HW, compiler ver, agent policy) → artifact`.  
Golden **replay** when the model or compiler upgrades (survey T3 missing cell). If replay fails, **do not serve** the new proposal.

### 3. Seams (DeepSeek Harness idea, compiler-shaped)

Each capability is definition + provider + consumer:

| Seam | Year-1 provider | Swappable later without rewrite |
|---|---|---|
| `llm` | One frontier + one small specialist | Any OpenAI-class / local model |
| `tools` | `propose` / `verify` / `bench` / `profile` | MCP-class servers |
| `session` | Append-only event log + fork/resume | Same log, different store (sqlite → customer object store) |
| `sandbox` | Landlock / container for generated code | Customer air-gap runner |
| `adapter` | Triton (primary) | Tile, HIP, Helion, Cake-class schedule IR, Argus-class tags |
| `oracle` | Golden + numerical + shape-grid | Alive2, SMT, FlashInfer-Bench `apply()`, GEAK-style warm A/B |
| `serving` | One of SGLang **or** vLLM (pick in Q1, do not dual-path) | The other engine as a second provider |

**Do not** hard-code Cake IR or DSH packages. Implement *seams*. If DeepSeek Harness becomes the industry plugin ABI, Lintel mounts as a **bundle** (oracles + adapters) rather than competing on generic coding UX. If Cake IR (or Argus DSL, or Tile) wins a customer, it is an `adapter` provider.

### 4. Localized reject (Cake idea, portable)

Agents must not get a single bit. Every failed gate returns **where** (thread / op / schedule field / program point) and **which seam** failed. That is how the harness *evolves*: recurring failures become a new oracle plugin or a tighter action enum — test-gated on a corpus — not a prompt paragraph.

This is survey **T5-lite** (toolchain evolution). It is not job (d) silicon codesign.

## Controller: FSM first

Survey P22 / TritorX / GEAK v4: **deterministic orchestration + LLM judgment**. Year-1 controller is an explicit state machine:

```text
triage → propose → pre-compile gates → measure → F-admit → freeze | fallback
```

LLM may choose *among enumerated actions* and write rationales. It may not invent a new tool mid-flight on the SLA path. Lab/Creator mode (DSH-like) can be looser and is **not** the SKU.

## How this survives survey-driven change

| If this settles in 2027–28 | Lintel change |
|---|---|
| **C3-A** — free IR rewrite beats advisors on a public suite | Widen the action enum *behind admit*; do not drop oracles |
| **C3-B** holds (current lean) | Keep narrow actions; sell that as the safety story |
| **C4** — Tile / Cake IR / Argus fragment the surface | Ship another `adapter`; portable schema was the year-1 investment |
| **C2** — someone publishes default-path p50/p90 | Turn our private partner traces into the same report format; do not fake it earlier |
| **C5** — vendor release notes name ACF workflows | Integrate; we become the *cross-vendor* admit/freeze layer |
| **C6-A** — production default with no classical fallback | We **do not follow**. That is a different company and a rejected survey bet. |
| **C7** — compiler-oracle review becomes default in llvm-project | Optional year-2 job (c) plugin; not year-1 GA |
| Cake or Argus open-source | Provider, not a rewrite |
| DSH plugin ABI wins | Lintel oracles ship as `dsh-plugin`s |

The **portable admit schema + seams** are the only things that must be right in Q1. Wrong IR choice is recoverable. Wrong “we are the compiler” story is not.

## Explicit non-goals (architecture)

- One universal cost model for L1–L7 (survey §5.1.1: no).
- One mega-IR (survey A6/S6: no).
- Always-on frontier model at every customer compile (P23: no).
- Serving the proposal before \(F\)-admit.
