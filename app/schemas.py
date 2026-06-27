from datetime import datetime

from pydantic import BaseModel


class ClusterCreate(BaseModel):
    name: str
    environment: str = "dev"
    provider: str = "aks"


class ClusterOut(BaseModel):
    id: int
    name: str
    environment: str
    provider: str
    created_at: datetime

    class Config:
        from_attributes = True

class HealthReportCreate(BaseModel):
    status: str
    cpu_usage: float
    memory_usage: float
    pod_failures: int = 0


class HealthReportOut(HealthReportCreate):
    id: int
    cluster_id: int
    reported_at: datetime

    class Config:
        from_attributes = True