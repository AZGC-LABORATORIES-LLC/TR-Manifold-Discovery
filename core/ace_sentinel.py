"""ACE-Sentinel — autonomic state machine over DSKM telemetry."""

from __future__ import annotations

from enum import Enum


class ACEState(str, Enum):
    ASYNCHRONOUS_DISCOVERY = "ASYNCHRONOUS_DISCOVERY"
    SALIENCE_BURST = "SALIENCE_BURST"
    SYNCHRONOUS_LOCK = "SYNCHRONOUS_LOCK"
    BIFURCATED_CLUSTER = "BIFURCATED_CLUSTER"
    INVARIANT_SYNTHESIS = "INVARIANT_SYNTHESIS"
    HUNTER_SHATTER = "HUNTER_SHATTER"


class ACESentinel:
    def __init__(self, lock: float = 0.82, fracture: float = 0.38, burst: float = 0.55) -> None:
        self.lock = lock
        self.fracture = fracture
        self.burst = burst
        self.state = ACEState.ASYNCHRONOUS_DISCOVERY
        self._hold = 0

    def evaluate(self, R: float, S: float, explained: float, mean_speed: float) -> ACEState:
        if mean_speed > 2.8 and R < 0.2:
            nxt = ACEState.HUNTER_SHATTER
        elif R >= self.lock:
            nxt = ACEState.SYNCHRONOUS_LOCK
        elif R < self.fracture and explained >= 0.55:
            nxt = ACEState.INVARIANT_SYNTHESIS
        elif R < self.fracture:
            nxt = ACEState.BIFURCATED_CLUSTER
        elif S >= self.burst:
            nxt = ACEState.SALIENCE_BURST
        else:
            nxt = ACEState.ASYNCHRONOUS_DISCOVERY
        if nxt == self.state:
            self._hold += 1
        else:
            self._hold = 0
            self.state = nxt
        return self.state
