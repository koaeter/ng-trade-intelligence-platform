from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="NG Trade Intelligence Platform API",
    version="0.1.0",
)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="ng-trade-intelligence-api",
        version="0.1.0",
    )
