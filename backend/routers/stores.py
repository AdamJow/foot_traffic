from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import distinct
from database import get_db
from models import FootTraffic

router = APIRouter(prefix="/api", tags=["stores"])

@router.get("/stores")
def get_stores(db: Session = Depends(get_db)):
    results = (
        db.query(
            FootTraffic.store_id,
            FootTraffic.store_name
        )
        .distinct()
        .order_by(FootTraffic.store_name.asc())
        .all()
    )

    return [
        {
            "store_id": r.store_id,
            "store_name": r.store_name
        }
        for r in results
    ]
