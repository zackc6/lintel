# L-010 — The session log cannot carry a Choreo `Finding` verbatim

**Gap.** `docs/POC.md` item 5: the session log is the walk, including `{where, seam, reason, hint}` plus the Choreo `Finding` JSON. `session-event.v0` has `where` and `reason` but no slot for the finding's `node` / `thread` / `element`, so a localized reject is flattened to a string.

**Carrier.** The bench's reject walks (`cases/reject/*`, one per `choreo/examples/fails`) replayed into `examples/session-log.jsonl` with the finding embedded unchanged.

**Change.** `session-event.v1`: `finding` is an opaque object validated by reference to Choreo's `Finding.as_dict` shape (Choreo owns it; Lintel stores it).

**Falsifier.** Choreo changes the finding shape and the event breaks silently (then the field must be versioned by `compiler_ver`). Survey item: P1 (structured traces), Choreo falsifier #2.

**Loop.** application

**Depends on.** L-002

**Status.** open
