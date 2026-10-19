from pydantic import BaseModel, Field


class SimulateRequest(BaseModel):
    n: int = Field(48, ge=4, le=400)
    steps: int = Field(240, ge=8, le=4000)
    p_edge: float = Field(0.12, gt=0.0, lt=1.0)
    k0: float = Field(1.2, ge=0.0, le=8.0)
    noise: float = Field(0.05, ge=0.0, le=1.0)
    tau_steps: int = Field(8, ge=1, le=64)
    double_angle: bool = False
    seed: int = 41


class StepLog(BaseModel):
    t: int
    R: float
    S: float
    K: float
    state: str
    explained: float


class SimulateResponse(BaseModel):
    architecture: str
    final_state: str
    final_R: float
    log: list[StepLog]
