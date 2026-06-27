from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from app.database import Base


class Cluster(Base):
    __tablename__ = "clusters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    environment = Column(String, nullable=False, default="dev")
    provider = Column(String, nullable=False, default="aks")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class HealthReport(Base):
    __tablename__ = "health_reports"

    id = Column(Integer, primary_key=True, index=True)
    cluster_id = Column(Integer, ForeignKey("clusters.id"), nullable=False, index=True)
    status = Column(String, nullable=False)          # healthy / degraded / down
    cpu_usage = Column(Float, nullable=False)         # percent, 0-100
    memory_usage = Column(Float, nullable=False)      # percent, 0-100
    pod_failures = Column(Integer, nullable=False, default=0)
    reported_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)