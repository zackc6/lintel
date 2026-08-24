"""Lintel year-1 contract: typed admit, freeze, replay.

This package is the product kernel a 10-person team starts from — not a compiler.
Adapters, oracles, and serving engines plug in behind seams.
"""

from lintel.fsm import State, allowed_transitions
from lintel.schema import ReplayError, cache_key, validate_admit_record, validate_session_event
from lintel.seams import SEAMS

__all__ = [
    "ReplayError",
    "SEAMS",
    "State",
    "allowed_transitions",
    "cache_key",
    "validate_admit_record",
    "validate_session_event",
]
