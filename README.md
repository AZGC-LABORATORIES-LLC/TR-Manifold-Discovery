# Quantum Family 4.1

Production DSKM swarm: delay-stochastic Kuramoto, autopoietic K(t), invariant synthesis, ACE-Sentinel, FastAPI.

**Computational only. No biological interpretation.**

Originating Architect: Sai Genoa (Genoa Page) / ACGC Laboratories LLC

Public map node: https://github.com/Donald-1974/The-Quantum-Family-4.1  
This repo is the engine.

## Run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. uvicorn api.server:app --reload --host 0.0.0.0 --port 8000
```

- `GET /` health
- `POST /simulate` body: `{ "n": 48, "steps": 240 }`

## Layout

```
core/dsde_integrator.py
core/reactive_coupling.py
core/invariant_synthesis.py
core/ace_sentinel.py
api/server.py
api/models.py
```
