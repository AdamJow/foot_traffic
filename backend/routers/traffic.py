from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from database import get_db
from models import FootTraffic
from datetime import datetime
from fastapi import HTTPException

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

@router.get("/breakdown")
def get_breakdown(
    timestamp: str,
    store_ids: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        parsed_timestamp = datetime.fromisoformat(timestamp)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid timestamp format")

    query = db.query(
        FootTraffic.store_id,
        FootTraffic.store_name,
        FootTraffic.people_count
    ).filter(FootTraffic.timestamp == parsed_timestamp)

    if store_ids:
        store_list = [s.strip() for s in store_ids.split(",")]
        query = query.filter(FootTraffic.store_id.in_(store_list))

    results = (
        query
        .order_by(
            FootTraffic.people_count.desc(),
            FootTraffic.store_name.asc()
        )
        .all()
    )

    return [
        {
            "store_id": r.store_id,
            "store_name": r.store_name,
            "people_count": r.people_count
        }
        for r in results
    ]