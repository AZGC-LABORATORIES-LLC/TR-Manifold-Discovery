"""Shared structural logic across fractured phase clusters."""

from __future__ import annotations

import numpy as np


class InvariantSynthesis:
    def extract(self, theta: np.ndarray, speeds: np.ndarray | None = None) -> dict:
        x = np.stack([np.cos(theta), np.sin(theta)], axis=1)
        if speeds is not None:
            x = np.concatenate([x, speeds.reshape(-1, 1)], axis=1)
        x = x - x.mean(axis=0, keepdims=True)
        if x.shape[0] < 2:
            return {"rank": 0, "principal": [], "explained": 0.0}
        cov = np.cov(x, rowvar=False)
        vals, vecs = np.linalg.eigh(cov)
        order = np.argsort(vals)[::-1]
        vals = np.maximum(vals[order], 0.0)
        total = float(vals.sum()) or 1.0
        principal = vecs[:, order[0]].tolist()
        return {
            "rank": int((vals > 1e-9).sum()),
            "eigenvalues": [float(v) for v in vals],
            "principal": [float(p) for p in principal],
            "explained": float(vals[0] / total),
        }
