from __future__ import annotations

import networkx as nx
import numpy as np
from fastapi import FastAPI

from api.models import SimulateRequest, SimulateResponse, StepLog
from core.ace_sentinel import ACESentinel
from core.dsde_integrator import DSKMIntegrator
from core.invariant_synthesis import InvariantSynthesis
from core.reactive_coupling import ReactiveCoupling

ARCHITECTURE = "Quantum Family 4.1 / DSKM + ACE-Sentinel / ACGC Laboratories LLC"

app = FastAPI(title="Quantum Family 4.1", version="4.1.0")


@app.get("/")
def health() -> dict:
    return {"ok": True, "architecture": ARCHITECTURE}


@app.post("/simulate", response_model=SimulateResponse)
def simulate(req: SimulateRequest) -> SimulateResponse:
    rng = np.random.default_rng(req.seed)
    g = nx.erdos_renyi_graph(req.n, req.p_edge, seed=req.seed)
    adj = nx.to_numpy_array(g, dtype=float)
    eng = DSKMIntegrator(
        n=req.n,
        noise=req.noise,
        tau_steps=req.tau_steps,
        double_angle=req.double_angle,
        seed=req.seed,
    )
    couple = ReactiveCoupling(k0=req.k0)
    inv = InvariantSynthesis()
    ace = ACESentinel()
    log: list[StepLog] = []
    last = {"R": 0.0, "S": 1.0, "explained": 0.0}
    state = ace.state.value
    for t in range(req.steps):
        tel = eng.step(couple.k, adj)
        rc = couple.update(tel["R"], eng.dt)
        synth = inv.extract(tel["theta"], rng.normal(tel["mean_speed"], 0.01, size=req.n))
        state = ace.evaluate(tel["R"], rc["S"], synth["explained"], tel["mean_speed"]).value
        last = {"R": tel["R"], "S": rc["S"], "explained": synth["explained"]}
        if t % max(1, req.steps // 80) == 0 or t == req.steps - 1:
            log.append(
                StepLog(
                    t=t,
                    R=tel["R"],
                    S=rc["S"],
                    K=rc["K"],
                    state=state,
                    explained=synth["explained"],
                )
            )
    return SimulateResponse(
        architecture=ARCHITECTURE,
        final_state=state,
        final_R=float(last["R"]),
        log=log,
    )
