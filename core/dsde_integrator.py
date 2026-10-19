"""Delay Stochastic Kuramoto Model — RK4 drift + Euler–Maruyama diffusion.

Computational only. No biological interpretation.
"""

from __future__ import annotations

import numpy as np


class DSKMIntegrator:
    def __init__(
        self,
        n: int,
        dt: float = 0.02,
        tau_steps: int = 8,
        omega_scale: float = 1.0,
        noise: float = 0.05,
        double_angle: bool = False,
        seed: int | None = 4,
    ) -> None:
        self.n = int(n)
        self.dt = float(dt)
        self.tau_steps = max(1, int(tau_steps))
        self.noise = float(noise)
        self.double_angle = bool(double_angle)
        rng = np.random.default_rng(seed)
        self.omega = rng.normal(0.0, omega_scale, size=self.n)
        self.theta = rng.uniform(-np.pi, np.pi, size=self.n)
        self.history = np.tile(self.theta, (self.tau_steps + 1, 1))

    @staticmethod
    def order_parameter(theta: np.ndarray) -> complex:
        return np.exp(1j * theta).mean()

    def _coupling(self, theta: np.ndarray, delayed: np.ndarray, k: float, adj: np.ndarray) -> np.ndarray:
        if self.double_angle:
            phase = 2.0 * (delayed[:, None] - theta[None, :])
        else:
            phase = delayed[:, None] - theta[None, :]
        s = adj * np.sin(phase)
        deg = np.maximum(adj.sum(axis=0), 1.0)
        return (k / deg) * s.sum(axis=0)

    def _drift(self, theta: np.ndarray, delayed: np.ndarray, k: float, adj: np.ndarray) -> np.ndarray:
        return self.omega + self._coupling(theta, delayed, k, adj)

    def step(self, k: float, adj: np.ndarray) -> dict:
        delayed = self.history[0]
        th = self.theta
        dt = self.dt
        k1 = self._drift(th, delayed, k, adj)
        k2 = self._drift(th + 0.5 * dt * k1, delayed, k, adj)
        k3 = self._drift(th + 0.5 * dt * k2, delayed, k, adj)
        k4 = self._drift(th + dt * k3, delayed, k, adj)
        drift = (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        diffusion = np.sqrt(2.0 * self.noise * dt) * np.random.normal(0.0, 1.0, size=self.n)
        self.theta = (th + dt * drift + diffusion + np.pi) % (2 * np.pi) - np.pi
        self.history = np.roll(self.history, -1, axis=0)
        self.history[-1] = self.theta
        z = self.order_parameter(self.theta)
        return {
            "R": float(np.abs(z)),
            "psi": float(np.angle(z)),
            "mean_speed": float(np.mean(np.abs(drift))),
            "theta": self.theta.copy(),
        }
