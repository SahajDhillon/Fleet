from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FleetIQ",
    description="Kubernetes fleet health & anomaly intelligence.",
    version="0.1.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/clusters", response_model=schemas.ClusterOut, status_code=201)
def register_cluster(cluster: schemas.ClusterCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Cluster).filter(models.Cluster.name == cluster.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Cluster already registered")
    new_cluster = models.Cluster(**cluster.model_dump())
    db.add(new_cluster)
    db.commit()
    db.refresh(new_cluster)
    return new_cluster


@app.get("/clusters", response_model=list[schemas.ClusterOut])
def list_clusters(db: Session = Depends(get_db)):
    return db.query(models.Cluster).all()


@app.post(
    "/clusters/{cluster_id}/health",
    response_model=schemas.HealthReportOut,
    status_code=201,
)
def report_health(
    cluster_id: int,
    report: schemas.HealthReportCreate,
    db: Session = Depends(get_db),
):
    cluster = db.query(models.Cluster).filter(models.Cluster.id == cluster_id).first()
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    new_report = models.HealthReport(cluster_id=cluster_id, **report.model_dump())
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report


@app.get(
    "/clusters/{cluster_id}/health",
    response_model=list[schemas.HealthReportOut],
)
def get_health_history(cluster_id: int, db: Session = Depends(get_db)):
    cluster = db.query(models.Cluster).filter(models.Cluster.id == cluster_id).first()
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    return (
        db.query(models.HealthReport)
        .filter(models.HealthReport.cluster_id == cluster_id)
        .order_by(models.HealthReport.reported_at.desc())
        .all()
    )


@app.get("/clusters/{cluster_id}/summary")
def cluster_summary(cluster_id: int, db: Session = Depends(get_db)):
    cluster = db.query(models.Cluster).filter(models.Cluster.id == cluster_id).first()
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")

    reports = (
        db.query(models.HealthReport)
        .filter(models.HealthReport.cluster_id == cluster_id)
        .order_by(models.HealthReport.reported_at.desc())
        .all()
    )

    if not reports:
        return {
            "cluster": cluster.name,
            "environment": cluster.environment,
            "report_count": 0,
            "latest_status": None,
        }

    count = len(reports)
    return {
        "cluster": cluster.name,
        "environment": cluster.environment,
        "latest_status": reports[0].status,
        "latest_reported_at": reports[0].reported_at,
        "report_count": count,
        "avg_cpu_usage": round(sum(r.cpu_usage for r in reports) / count, 1),
        "avg_memory_usage": round(sum(r.memory_usage for r in reports) / count, 1),
        "total_pod_failures": sum(r.pod_failures for r in reports),
    }