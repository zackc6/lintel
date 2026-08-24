"""SLA-path controller. Lab/Creator mode may be looser; this FSM is the SKU."""

from __future__ import annotations

from enum import StrEnum


class State(StrEnum):
    TRIAGE = "triage"
    PROPOSE = "propose"
    PRECOMPILE_GATE = "precompile_gate"
    MEASURE = "measure"
    F_ADMIT = "f_admit"
    FREEZE = "freeze"
    FALLBACK = "fallback"


TRANSITIONS: dict[State, frozenset[State]] = {
    State.TRIAGE: frozenset({State.PROPOSE, State.FALLBACK}),
    State.PROPOSE: frozenset({State.PRECOMPILE_GATE, State.FALLBACK}),
    State.PRECOMPILE_GATE: frozenset({State.MEASURE, State.FALLBACK}),
    State.MEASURE: frozenset({State.F_ADMIT, State.FALLBACK}),
    State.F_ADMIT: frozenset({State.FREEZE, State.FALLBACK}),
    State.FREEZE: frozenset(),
    State.FALLBACK: frozenset(),
}


def allowed_transitions(state: State) -> frozenset[State]:
    return TRANSITIONS[state]


def can_transition(src: State, dst: State) -> bool:
    return dst in TRANSITIONS[src]
