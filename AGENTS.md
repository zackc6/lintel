# Instructions for coding agents (ChatGPT/Codex, Claude, Cursor)

This file is the briefing for any agent working in this repository. Read it fully before editing. It is one of four repositories maintained together under the same protocol; the protocol below is identical in all four, the sections above it are specific to this one.

## What this repository is

**Lintel** is the control plane of the agentic compiler: the written contract (`schemas/`, `examples/`) and the design docs. It owns the *field names* of session events, admit records, cache keys, and adapter proposals. It has no code and emits no binaries.

**This repo owns:** schema field names and the control-plane design (three loops, kill switches, year-1 SKU).

**This repo does not own:** Kernel encoding and artifact kinds (Choreo owns those); the thesis and forecasts (the survey owns those); running the walk (agentic-compiler does that).

## Validation gate (must pass on the branch before a batch is argued)

```bash
python3 scripts/validate_contract.py
```

every schema is a valid JSON Schema 2020-12 and every example parses; see `scripts/validate_contract.py`. Run `python3 -m choreoir consume-check .` from a Choreo checkout when the batch touches anything Choreo consumes, and report the count in the thread.

## What a batch must say (the verdict comes first)

Every batch entry in the Review thread leads with: which survey section (`docs/SURVEY_MAP.md` / `SURVEY_MATCH.md` row) the change rests on; which schema fields change and whether that breaks Choreo's consume contract or agentic-compiler's walk; which kill switch in `docs/RISKS.md` it touches. A list of files changed without these is not a batch.

## The four repositories, and who owns what

| Repo | Role | Owns |
|---|---|---|
| [ai-compiler-survey](https://github.com/zackc6/ai-compiler-survey) | Referee. The thesis, evidence, and dated forecasts. | Whether the thesis still holds; what the evidence means. |
| [lintel](https://github.com/zackc6/lintel) | Control plane: written contract + design. | Schema field names, the three loops, kill switches. |
| [choreo](https://github.com/zackc6/choreo) | Data plane: kernel-schedule compiler. | Kernel encoding, admit findings, sinks, `compiler_ver`. |
| [agentic-compiler](https://github.com/zackc6/agentic-compiler) | Where the two run together. | The walk, the case corpus, drift report, performance table. |

The same two agents (Claude and ChatGPT/Codex) maintain all four under the same rule: **debate in the Review thread, agree, then squash-merge.** The maintainer (Zack) decides ties. Each agent's daily check covers all four `STATUS.md` files, not just the one it last edited.

Cross-repo rules:

1. **The survey is the referee, not an advocate.** Thesis and forecast changes happen only in the survey repo. A batch here that rests on a survey claim names the section. If work here produces evidence that bears on the thesis (a falsifier fired, a measured number), open a row in the **survey's** `STATUS.md` rather than arguing it here.
2. **A contract change starts in the owner repo.** Field names → Lintel. Kernel encoding, artifact kinds, `compiler_ver` → Choreo. It lands there by this protocol, then reaches agentic-compiler as a submodule-bump batch that updates `docs/DRIFT.md` and the drift tests in the same commit. Nobody edits a submodule's files from agentic-compiler.
3. **Three loops stay apart.** Application search (the walk) never edits the compiler; a compiler change is an IR-evolution commit on Choreo `main` with a `compiler_ver` bump; a controller change is a `policy_id` promotion with its own holdout. Say which loop a batch belongs to.
4. **Numbers keep their denominators.** A correctness-only result is not a speedup; a kernel speedup is not an application gain; a proxy labelled `measured: false` is not performance. Same evidence discipline as the survey.

## How the two agents work together (same as the survey)

1. **Claim before editing.** Add one row to the **Open batch** table at the top of `STATUS.md` (agent, scope, start date, status) and push it, or include it in your batch commit. If the other agent has an open row on overlapping scope, review its pushed work instead of editing the same files.
2. **Talk in the Review thread** in `STATUS.md`, newest entry first, one dated entry per reply, headed `**<YYYY-MM-DD HH:MM UTC> — <Agent>**` (ChatGPT headings must start `**<date> … ChatGPT` so the push detector fires). Each entry: verdict on the other agent's last batch (agree / object, naming file and line), open points, and what you will do next. Mark a point "resolved" with the commit hash. Do not argue in commit messages or in docs.
3. **Debate, then merge.** A content batch goes on a branch `claude/<topic>-<date>` or `chatgpt/<topic>-<date>`, **validated on that branch** (see "Validation gate" above). The author posts its argument in the Review thread on `main`: what changes, which owner-repo contract or survey section it rests on, the verdict items listed under "What a batch must say", and the proposed wording. The other agent replies agree / object per point with reasons. The branch is **squashed into one commit on `main`** (`git merge --squash`, never force-pushed, never a fast-forward or multi-parent merge for content) only after both agents have written "agree" on every disputed point or the maintainer has ruled. Review-thread entries, Open-batch rows, and pure fact fixes (a wrong number, a broken link, a failing build fixed) may go to `main` directly. If the other agent has not replied within two daily checks, ask the maintainer to rule; do not merge unilaterally.
4. **Merge rules.** On agreement: (a) squash with a `git log`-readable message — what changed, which contract or survey section it rests on, the loop it belongs to, the review rounds; (b) write a **"MERGE SUMMARY"** entry at the top of the Review thread (alignment with the survey and the owner contracts first, then changes, then agreement record, then commit hash) so the maintainer's merge-email watch can email it — a GitHub Action cannot send email, so record email as pending, never as sent; (c) delete the merged branch and any draft it superseded, and verify with `git ls-remote --heads origin`. Do not report deletion without checking.
5. **Sign commits** with your agent name (`Co-Authored-By: Claude` / `Co-Authored-By: ChatGPT`).
6. **Event-driven debate.** `.github/workflows/claude-reply.yml` runs Claude (`anthropics/claude-code-action/base-action@v1`, secret `ANTHROPIC_API_KEY`) when a push to `main` adds a ChatGPT-headed Review-thread entry or on a `chatgpt_replied` dispatch. `.github/workflows/codex-review.yml` runs a read-only Codex review (`openai/codex-action@v1`, secret `OPENAI_API_KEY`) when a `claude/*` branch is created or pushed, on manual dispatch, or on a `claude_replied` dispatch; it posts to `STATUS.md` and dispatches Claude. At most three rounds per side per branch; the loop stops when the branch is merged or deleted or a reply fails to publish. A workflow run is never approval: only the agreement procedure above authorizes a merge. Both secrets must be set on this repository for unattended runs.
7. **No PRs.** The debate replaces pull requests. Branches exist only to carry a batch to the thread; `main` is the only long-lived ref.

## What not to do

- Do not edit the other agent's stylistic choices; object in the thread, fix only facts, broken links, or failing builds.
- Do not change a contract field, a Kernel encoding, or `compiler_ver` outside the owner repo.
- Do not call a proxy a measurement, or a correctness result a speedup.
- Do not merge because a workflow passed. Green CI is a precondition, not agreement.
