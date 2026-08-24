from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from lintel.fsm import State, can_transition
from lintel.schema import ReplayError, assert_replay, cache_key, validate_admit_record, validate_session_event
from lintel.seams import SEAMS, YEAR1_PROVIDERS

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


def test_example_admit_record_validates() -> None:
    record = json.loads((EXAMPLES / "admit-record.json").read_text(encoding="utf-8"))
    validate_admit_record(record)
    assert cache_key(record).startswith("sha256:")


def test_example_session_log_validates() -> None:
    lines = (EXAMPLES / "session-log.jsonl").read_text(encoding="utf-8").splitlines()
    kinds = []
    for line in lines:
        event = json.loads(line)
        validate_session_event(event)
        kinds.append(event["kind"])
    assert kinds[0] == "session.start"
    assert "freeze" in kinds


def test_failed_gate_requires_localized_reject() -> None:
    event = {
        "schema_version": "session-event.v0",
        "event_id": "evt_x",
        "seq": 3,
        "ts": "2026-09-15T11:59:21Z",
        "session_id": "ses_q1_001",
        "parent_session_id": None,
        "kind": "gate",
        "payload": {"seam": "adapter", "passed": False},
    }
    with pytest.raises(ValueError, match="localized reject"):
        validate_session_event(event)
    event["payload"]["reject"] = {"where": "schedule.num_warps", "reason": "not_in_enum"}
    validate_session_event(event)


def test_replay_same_key_cannot_silently_change_decision() -> None:
    record = json.loads((EXAMPLES / "admit-record.json").read_text(encoding="utf-8"))
    other = copy.deepcopy(record)
    other["decision"] = "fallback"
    with pytest.raises(ReplayError):
        assert_replay(record, other)

    # Model swap, same policy: cache key unchanged. Same decision required; mismatch is a hard fail.
    swapped = copy.deepcopy(record)
    swapped["pins"] = {**record["pins"], "model_id": "other.model"}
    assert_replay(record, swapped)
    swapped["decision"] = "fallback"
    with pytest.raises(ReplayError):
        assert_replay(record, swapped)

    # Compiler bump: new key, so a new decision is allowed (must re-admit).
    bumped = copy.deepcopy(record)
    bumped["decision"] = "fallback"
    bumped["pins"] = {**record["pins"], "compiler_ver": "triton==9.9.9"}
    assert_replay(record, bumped)


def test_free_text_action_rejected() -> None:
    record = json.loads((EXAMPLES / "admit-record.json").read_text(encoding="utf-8"))
    record["actions"] = [{"kind": "paste_cuda", "enum_id": "void kernel() {}"}]
    with pytest.raises(Exception):
        validate_admit_record(record)


def test_fsm_sla_path_is_linear_with_fallback() -> None:
    path = [
        State.TRIAGE,
        State.PROPOSE,
        State.PRECOMPILE_GATE,
        State.MEASURE,
        State.F_ADMIT,
        State.FREEZE,
    ]
    for src, dst in zip(path, path[1:]):
        assert can_transition(src, dst)
    assert can_transition(State.MEASURE, State.FALLBACK)
    assert not can_transition(State.FREEZE, State.PROPOSE)


def test_year1_seams_are_named() -> None:
    assert SEAMS == ("llm", "tools", "session", "sandbox", "adapter", "oracle", "serving")
    assert set(YEAR1_PROVIDERS) == set(SEAMS)
