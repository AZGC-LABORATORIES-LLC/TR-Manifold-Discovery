"""Autopoietic K(t) from endogenous salience S = 1 - R."""

from __future__ import annotations


class ReactiveCoupling:
    def __init__(
        self,
        k0: float = 1.2,
        k_min: float = 0.15,
        k_max: float = 4.0,
        decay: float = 0.08,
        sensitivity: float = 2.4,
    ) -> None:
        self.k = float(k0)
        self.k_min = float(k_min)
        self.k_max = float(k_max)
        self.decay = float(decay)
        self.sensitivity = float(sensitivity)
        self._r_prev = 0.0

    def update(self, R: float, dt: float) -> dict:
        S = max(0.0, 1.0 - float(R))
        dR = float(R) - self._r_prev
        self._r_prev = float(R)
        dk = (-self.decay * self.k + self.sensitivity * S * (1.0 - dR)) * dt
        self.k = float(np_clip(self.k + dk, self.k_min, self.k_max))
        return {"K": self.k, "S": S, "dR": dR}


def np_clip(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else hi if x > hi else x
