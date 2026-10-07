from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from collections import Counter
from datetime import datetime, timedelta
import models

Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/check-ins")
def create_check_in(feeling: str, note: str | None=None, db: Session=Depends(get_db)):
    check_in = models.CheckIn(feeling=feeling, note=note)

    db.add(check_in)
    db.commit()
    db.refresh(check_in)

    return check_in

@app.get("/check-ins")
def get_check_in(db: Session=Depends(get_db)):
    return db.query(models.CheckIn).order_by(
        models.CheckIn.created_at.desc()
    ).all()

@app.get("/check-ins/insights")
def get_checki_in(db:Session=Depends(get_db)):
    week_ago=datetime.now() - timedelta(days=7)

    recent_check_ins=(
        db.query(models.CheckIn).filter(models.CheckIn.created_at>=week_ago).order_by(models.CheckIn.created_at.desc()).all()
    )

    feelings=[check_in.feeling for check_in in recent_check_ins]

    most_common_feeling=None

    if feelings:
        most_common_feeling=Counter(feelings).most_common(1)[0][0]

    return {
        "check_in_count": len(recent_check_ins),
        "most_common_feeling": most_common_feeling
    }

@app.get("/")
def root():
    return {
        "message": "Hello from Asahi"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }