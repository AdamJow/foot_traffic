from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from database import get_db
from models import FootTraffic

router = APIRouter(prefix="/api/traffic", tags=["traffic"])

@router.get("/timeseries")
def get_timeseries(
    store_ids: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(
        FootTraffic.timestamp,
        func.sum(FootTraffic.people_count).label("total")
    )

    if store_ids:
        store_list = [s.strip() for s in store_ids.split(",")]
        query = query.filter(FootTraffic.store_id.in_(store_list))

    results = (
        query
        .group_by(FootTraffic.timestamp)
        .order_by(FootTraffic.timestamp.asc())
        .all()
    )

    return [
        {
            "timestamp": r.timestamp.isoformat(),
            "people_count": r.total
        }
        for r in results
    ]
