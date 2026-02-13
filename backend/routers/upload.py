import csv
import io
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import FootTraffic
from database import get_db

router = APIRouter(prefix="/api", tags=["upload"])

REQUIRED_COLUMNS = {"timestamp", "store_id", "store_name", "people_count"}

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    contents = await file.read()

    try:
        decoded = contents.decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid file encoding")

    reader = csv.DictReader(io.StringIO(decoded))

    # Validate headers
    if not REQUIRED_COLUMNS.issubset(set(reader.fieldnames or [])):
        raise HTTPException(
            status_code=400,
            detail=f"CSV must contain columns: {REQUIRED_COLUMNS}"
        )

    rows_to_insert = []

    for i, row in enumerate(reader, start=1):
        try:
            timestamp = datetime.fromisoformat(row["timestamp"])
            store_id = row["store_id"]
            store_name = row["store_name"]
            people_count = int(row["people_count"])

            if people_count < 0:
                raise ValueError("people_count cannot be negative")

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid data at row {i}: {str(e)}"
            )

        rows_to_insert.append(
            FootTraffic(
                timestamp=timestamp,
                store_id=store_id,
                store_name=store_name,
                people_count=people_count,
            )
        )

    # Replace dataset
    try:
        db.query(FootTraffic).delete()
        db.bulk_save_objects(rows_to_insert)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

    return {
        "message": "Dataset uploaded successfully",
        "rows_inserted": len(rows_to_insert)
    }
